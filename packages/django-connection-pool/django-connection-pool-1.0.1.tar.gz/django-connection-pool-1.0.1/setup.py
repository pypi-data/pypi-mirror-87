from setuptools import setup, find_packages

from django_connection_pool import version, name

setup(
    name=name,
    version=version,
    packages=find_packages(),
    install_requires=[
        "Django>=2.2.6",
        "sqlalchemy>=1.3.19",
        "six>=1.15.0"
    ],
    include_package_data=True,
    license='GNU General Public License v3.0',
    author='Lee',
    author_email='canyun@live.com',
    description='django connection pool',
)
