import logging
import os
import pytest
import sh
import time

from enough import settings
from enough.common import tcp
from enough.common.retry import retry
from enough.common.openstack import OpenStack

from tests import prepare_config_dir


@pytest.fixture(autouse=True, scope='session')
def debug_enough():
    logging.getLogger('enough').setLevel(logging.DEBUG)


@pytest.fixture
def tcp_port():
    return str(tcp.free_port())


def docker_conf():
    if 'DOCKER_HOST' in os.environ:
        return {
            'namespace': 'myaccount',
        }
    else:
        return {
            'port': tcp.free_port(),
        }


@pytest.fixture
def docker_args():
    return docker_conf()


@pytest.fixture
def docker_options():
    options = []
    for k, v in docker_conf().items():
        k = k.replace('_', '-')
        options.append('--' + k)
        options.append(v)
    return options


class DockerLeftovers(Exception):
    pass


@retry(DockerLeftovers, tries=7)
def docker_cleanup(prefix):
    leftovers = []
    for container in sh.docker.ps('--all', '--format', '{{ .Names }}', _iter=True):
        container = container.strip()
        if prefix in container:
            sh.docker.rm('-f', container, _ok_code=[0, 1])
            leftovers.append('container(' + container + ')')
    for network in sh.docker.network.ls('--format', '{{ .Name }}', _iter=True):
        network = network.strip()
        if prefix in network:
            sh.docker.network.rm(network, _ok_code=[0, 1])
            leftovers.append('network(' + network + ')')
    for image in sh.docker.images('--format', '{{ .Repository }}:{{ .Tag }}', _iter=True):
        image = image.strip()
        if image.startswith(prefix):
            sh.docker.rmi('--no-prune', image, _ok_code=[0, 1])
            leftovers.append('image(' + image + ')')
    if leftovers:
        raise DockerLeftovers('scheduled removal of ' + ' '.join(leftovers))


@pytest.fixture
def docker_name():
    prefix = 'enough_test_' + str(int(time.time()))
    yield prefix
    docker_cleanup(prefix)


@pytest.fixture
def openstack_name():
    prefix = 'enough_test_' + str(int(time.time()))
    yield prefix
    o = OpenStack('.')
    o.destroy_everything(prefix)


@pytest.fixture
def tmp_config_dir(monkeypatch, tmpdir):
    enough_dot_dir = str(tmpdir)
    domain = 'enough.community'
    monkeypatch.setenv('ENOUGH_DOT', enough_dot_dir)
    monkeypatch.setenv('ENOUGH_DOMAIN', domain)
    config_dir = prepare_config_dir(domain, enough_dot_dir)
    monkeypatch.setattr(settings, 'CONFIG_DIR', config_dir)


# Some tests mock os.path.exists using the mocker fixture, use trylast in
# order to avoid any interference
@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    assert os.path.isdir('.git')  # check cwd is the source repository
    assert os.path.isdir('inventory/group_vars/all')  # with the expected structure

    check_generated_files = [
        'inventory/group_vars/all/openstack-provider.yml',
        'inventory/group_vars/all/private-key.yml',
    ]
    if os.environ.get('GITLAB_CI'):
        # contributors are allowed to define such files, CI isn't
        check_generated_files.extend((
            'infrastructure_key',
            'infrastructure_key.pub',
        ))
    # first remove all these files in order to not interfere with the next
    # tests then fail
    found = []
    for path in check_generated_files:
        if os.path.exists(path):
            found.append(path)
            os.remove(path)
    assert not found
