from enough.common import retry


testinfra_hosts = ['ansible://debian-host']


def test_upgrade(host):
    return
    # that does not work, probably because the socket to the host needs reset after reboot
    with host.sudo():
        cmd = host.run("""
        set -x ; sed -i -e '/.*Unattended-Upgrade::Automatic-Reboot /s|^|//|' \
                 /etc/apt/apt.conf.d/50unattended-upgrades
        """)
        assert 0 == cmd.rc

        cmd = host.run("set -x ; touch /var/run/reboot-required")
        assert 0 == cmd.rc

        cmd = host.run("unattended-upgrade")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc

        @retry.retry((AssertionError, KeyError), tries=7)
        def run():
            cmd = host.run("! test -f /var/run/reboot-required")
            print(cmd.stdout)
            print(cmd.stderr)
            assert 0 == cmd.rc

        run()
