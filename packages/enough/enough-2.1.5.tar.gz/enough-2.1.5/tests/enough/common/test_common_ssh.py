import pytest

from enough.common.openstack import Heat, Stack
from enough.common.ssh import SSH

from tests import prepare_config_dir


@pytest.mark.openstack_integration
def test_ssh(openstack_name, openstack_provider, tmpdir):
    domain = 'enough.community'
    d = Heat.hostvars_to_stack(openstack_name, openstack_provider)
    config_dir = prepare_config_dir(domain, tmpdir)
    provider = openstack_provider['openstack_provider']
    ssh = SSH(config_dir, domain=domain, provider=provider)
    s = Stack(config_dir, d)
    s.set_public_key(f'{config_dir}/infrastructure_key.pub')
    s.create_or_update()
    r = ssh.ssh(openstack_name, ['uptime'], interactive=False)
    s.delete()
    assert r.returncode == 0
    assert 'load average' in r.stdout.decode('utf-8')
