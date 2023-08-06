import os
import threading
from typing import Union, Callable

import six
from six.moves import range
from sqlalchemy.pool import QueuePool
from sqlalchemy.util import queue


def __evaluate__(_callable_or_value):
    _cv = _callable_or_value
    return _cv() if callable(_cv) else _cv


class HashableDict(dict):

    def __hash__(self):
        return hash(frozenset(six.iteritems(self)))


class IntervalTimer(threading.Thread):

    def __init__(self, interval, func, args=None, kwargs=None):
        """
        :type interval: float or Callable
        :type func: Callable
        :type args: list or tuple
        :type kwargs: dict
        """
        threading.Thread.__init__(self)
        self.interval = interval  # type: Union[float, Callable[[], float]]
        self.function = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        while True:
            interval = __evaluate__(self.interval)
            if self.finished.wait(interval):
                break
            self.function(*self.args, **self.kwargs)
        self.finished.set()


class DjangoQueuePool(QueuePool):
    logger = None

    def __init__(
            self,
            creator,
            core_pool_size=None,
            unload_timeout=None,
            retire_interval=None,
            retire_quantity=None,
            show_status_interval=None,
            **kwargs
    ):
        """
        :type creator: Callable
        :type core_pool_size: int or Callable
        :type unload_timeout: int or float or Callable
        :type retire_interval: int or float or Callable
        :type retire_quantity: int or float or Callable
        :type kwargs: dict
        """
        super(DjangoQueuePool, self).__init__(creator, **kwargs)

        self._core_pool_size = core_pool_size  # type: Union[int, Callable[[], int]]
        if self._core_pool_size is None:
            self._core_pool_size = kwargs['pool_size']

        self._unload_timeout = unload_timeout  # type: Union[float, Callable[[], float]]

        self._retire_timer = None
        self._retire_interval = retire_interval  # type: Union[float, Callable[[], float]]
        self._retire_quantity = retire_quantity or 1  # type: Union[int, Callable[[], int]]

        if self._retire_interval is not None:
            self._retire_timer = IntervalTimer(self._retire_interval, self._do_retire)
            self._retire_timer.daemon = True
            self._retire_timer.start()

        self._show_status_timer = None
        self._show_status_interval = show_status_interval

        if self._show_status_interval is not None:
            self._show_status_timer = IntervalTimer(self._show_status_interval, self.status)
            self._show_status_timer.daemon = True
            self._show_status_timer.start()

    def _is_overload(self):
        return self.checkedout() >= __evaluate__(self._core_pool_size)

    def _do_get(self):

        if (
                self._is_overload() and
                self._unload_timeout is not None
        ):
            try:  # wait before overflow
                return self._pool.get(
                    True, __evaluate__(self._unload_timeout))
            except queue.Empty:
                pass

        return super(DjangoQueuePool, self)._do_get()

    # noinspection PyBroadException
    def do_retire_conn(self):
        try:
            conn = self._do_get()
            if conn is not None:
                try:
                    conn.close()
                finally:
                    self._dec_overflow()
        except Exception:
            pass

    # noinspection PyBroadException
    def _do_retire(self):
        try:
            for _ in range(__evaluate__(self._retire_quantity)):
                self.do_retire_conn()
        except Exception:
            pass

    def recreate(self):

        return self.__class__(

            self._creator,

            core_pool_size=self._core_pool_size,
            unload_timeout=self._unload_timeout,
            retire_interval=self._retire_interval,
            retire_quantity=self._retire_quantity,

            pool_size=self._pool.maxsize,
            max_overflow=self._max_overflow,
            timeout=self._timeout,
            recycle=self._recycle,
            dialect=self._dialect,
            pre_ping=self._pre_ping,
            use_threadlocal=self._use_threadlocal,
            reset_on_return=self._reset_on_return,
            echo=self.echo,
            logging_name=self._orig_logging_name,
            _dispatch=getattr(self, 'dispatch', None),
        )

    def core_size(self):
        return self._core_pool_size

    def status(self):
        pid = os.getpid()
        status = (
                "Mysql Connection Pool of %d "
                "Pool size: %d  Connections in pool: %d "
                "Current Overflow: %d Current Checked out "
                "connections: %d"
                % (
                    pid,
                    self.size(),
                    self.checkedin(),
                    self.overflow(),
                    self.checkedout(),
                )
        )
        # self.logger.info(InfoLog(status))
        return status
