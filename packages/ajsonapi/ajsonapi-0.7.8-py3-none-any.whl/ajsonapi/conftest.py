# Copyright © 2018-2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Fixtures for dealing with SQL databases."""

import subprocess
from os import environ
from re import search as re_search
from time import sleep

import pytest
from docker import from_env as docker_from_env

from ajsonapi.application import Application

NETWORK_NAME = 'test-network'
CONTAINER_NAME = 'test-container'

POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'password'
POSTGRES_PORT = 9900
POSTGRES_DB = 'db'
POSTGRES_LOCAL_DIR = '/tmp/pgdata/ajsonapi'

if 'PYTEST_XDIST_WORKER' in environ:  # pragma: no cover
    WORKER = environ['PYTEST_XDIST_WORKER']
    NETWORK_NAME += f'-{WORKER}'
    CONTAINER_NAME += f'-{WORKER}'
    POSTGRES_PORT += int(re_search(r'\d+$', WORKER).group())
    POSTGRES_LOCAL_DIR += f'_{WORKER}'
    del WORKER

docker = docker_from_env(version='auto')  # pylint: disable=invalid-name


def create_postgres_network(name):
    """Create a docker Postgres network for the functional tests."""
    return docker.networks.create(name, driver='bridge')


def create_postgres_container(name, network):
    """Create a docker Postgres container for the functional tests."""
    kwargs = {
        'name': name,
        'environment': {
            'POSTGRES_USER': POSTGRES_USER,
            'POSTGRES_PASSWORD': POSTGRES_PASSWORD,
            'POSTGRES_DB': POSTGRES_DB,
        },
        'volumes': {
            POSTGRES_LOCAL_DIR: {
                'bind': '/var/lib/postgresql/data',
                'mode': 'rw',
            },
        },
        'network': network.name,
        'ports': {
            '5432/tcp': POSTGRES_PORT,
        },
        'detach': True,
        'ipc_mode': 'shareable',
    }
    return docker.containers.create('postgres', **kwargs)


@pytest.fixture(scope='session')
def postgres_container():
    """Pytest fixture for creating a Docker Postgres container."""

    network = create_postgres_network(NETWORK_NAME)
    container = create_postgres_container(CONTAINER_NAME, network)
    container.start()

    proc = subprocess.run('docker network ls --format "{{.Name}}"',
                          shell=True,
                          check=True,
                          capture_output=True)
    names = ' '.join(proc.stdout.decode().strip().split('\n'))
    proc = subprocess.run(f'docker network inspect {names}',
                          shell=True,
                          check=False,
                          capture_output=True)
    print(proc.stdout.decode().strip())
    proc = subprocess.run(f'docker container inspect {CONTAINER_NAME}',
                          shell=True,
                          check=True,
                          capture_output=True)
    print(proc.stdout.decode().strip())

    yield container
    container.stop()
    container.remove()
    network.remove()


@pytest.fixture()
def postgres_database(request, postgres_container):
    """Pytest fixture for creating a database in a Docker Postgres container.
    """
    # pylint: disable=redefined-outer-name

    # pylint: disable=protected-access
    database_name = request._pyfuncitem.name
    if database_name.startswith('test_'):
        database_name = database_name[5:]
    if database_name.endswith('[pyloop]'):
        database_name = database_name[:-8]
    kwargs = {
        'stdin': True,
        'tty': True,
    }

    result = postgres_container.exec_run(
        f'psql -U {POSTGRES_USER} -d {POSTGRES_DB} '
        f'-c "CREATE DATABASE {database_name}"', **kwargs)
    okay = (result.exit_code == 0)
    while not okay:  # pragma: no cover
        sleep(.1)
        result = postgres_container.exec_run(
            f'psql -U {POSTGRES_USER} -d {POSTGRES_DB} '
            f'-c "CREATE DATABASE {database_name}"', **kwargs)
        okay = (result.exit_code == 0)
    # Gitlab CI/CD runs tests within a container so we will have to find
    # the internal Postgres URI (instead of the external one
    # (localhost:{POSTGRES_PORT}) for the development machine).
    proc = subprocess.run(
        'docker inspect --format '
        "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "
        f'{CONTAINER_NAME}',
        shell=True,
        check=True,
        capture_output=True)
    internal_ip_address = proc.stdout.decode().strip()
    yield (f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
           f'{internal_ip_address}:5432/{database_name}')
    postgres_container.exec_run((f'psql -U {POSTGRES_USER} -d {POSTGRES_DB} '
                                 f'-c "DROP DATABASE {database_name}"'),
                                **kwargs)


@pytest.fixture()
async def app(postgres_database):
    """Pytest fixture for creating the JSON API application."""
    # pylint: disable=redefined-outer-name

    app = Application()
    app.verify_model()
    await app.connect_database(postgres_database)
    await app.create_tables()
    app.add_event_socket_route()
    app.add_json_api_routes()
    yield app
    await app.disconnect_database()


@pytest.fixture()
def client(loop, app, aiohttp_client):
    """Pytest fixture for creating a JSON API test client."""
    # pylint: disable=redefined-outer-name

    return loop.run_until_complete(aiohttp_client(app.app))
