import pytest
import requests
from tests.infrastructure import get_driver
import yaml

testinfra_hosts = ['ansible://icinga-host']


def get_address(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return 'icinga.' + yaml.safe_load(
        open(vars_dir + '/domain.yml'))['domain']


def test_icingaweb2_login_screen(host, pytestconfig):
    if get_driver() == 'docker':
        pytest.skip("no letsencrypt when running docker")
    address = get_address(pytestconfig.getoption("--ansible-inventory"))
    s = requests.Session()
    r = s.get(f'http://{address}/icingaweb2/authentication/login',
              timeout=5, allow_redirects=False)
    assert r.status_code == 301
    r = s.get(f'https://{address}/icingaweb2/authentication/login',
              timeout=5, verify='certs')
    cookies = dict(r.cookies)
    r = s.get(f'https://{address}/icingaweb2/authentication/login?_checkCookie=1',
              cookies=cookies, timeout=5, verify='certs')
    r.raise_for_status()
    assert 'Icinga Web 2 Login' in r.text
