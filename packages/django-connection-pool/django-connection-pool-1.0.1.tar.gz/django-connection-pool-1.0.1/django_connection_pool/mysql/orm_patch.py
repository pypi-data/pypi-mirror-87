"""
Django ORM 补丁, 执行完查询后立即释放连接
"""

from django.db.models.sql import compiler
from django.db.models.sql.constants import MULTI, GET_ITERATOR_CHUNK_SIZE


def install_django_orm_patch():
    execute_sql = compiler.SQLCompiler.execute_sql

    # Django 1.11
    def patched_execute_sql(self, result_type=MULTI, chunked_fetch=False, chunk_size=GET_ITERATOR_CHUNK_SIZE):
        try:
            result = execute_sql(self, result_type, chunked_fetch, chunk_size)
        finally:
            if not self.connection.in_atomic_block:
                self.connection.close()  # return connection to pool by db_pool_patch
        return result

    compiler.SQLCompiler.execute_sql = patched_execute_sql

    insert_execute_sql = compiler.SQLInsertCompiler.execute_sql

    def patched_insert_execute_sql(self, return_id=False):
        try:
            result = insert_execute_sql(self, return_id)
        finally:
            if not self.connection.in_atomic_block:
                self.connection.close()  # return connection to pool by db_pool_patch
        return result

    compiler.SQLInsertCompiler.execute_sql = patched_insert_execute_sql
