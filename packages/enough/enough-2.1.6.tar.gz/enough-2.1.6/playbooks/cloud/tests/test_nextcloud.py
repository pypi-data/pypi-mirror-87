testinfra_hosts = ['ansible://cloud-host']


def test_nextcloud(host):
    cmd = host.run("""
    set -xe
    mount | grep /dev/mapper/spare
    curl --silent https://cloud.$(hostname -d)/login | \
         grep --quiet 'This application requires JavaScript'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc


def test_nextcloud_via_tor(host):
    cmd = host.run("""
    set -xe
    hostname=$(sudo cat /var/lib/tor/services/cloud/hostname)
    torsocks curl --silent http://$hostname/login | \
             grep --quiet 'This application requires JavaScript'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
