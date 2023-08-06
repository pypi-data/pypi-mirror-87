from tests.icinga_helper import IcingaHelper


def pytest_configure(config):
    IcingaHelper.set_ansible_inventory(config.getoption("--ansible-inventory"))


def pytest_addoption(parser):
    parser.addoption(
        '--provider',
        choices=('fuga', 'ovh'),
        default='ovh',
        help='Name of the OpenStack provider used for the tests'
    )
