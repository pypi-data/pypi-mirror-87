import time
import testinfra

testinfra_hosts = ['ansible://postfix-host']


def test_sendmail(host):
    domain = host.run("hostname -d").stdout.strip()

    postfix_host = host
    postfix_client_host = testinfra.host.Host.get_host(
        'ansible://bind-host',
        ansible_inventory=host.backend.ansible_inventory)

    cmd = postfix_client_host.run("""
    ( echo 'To: loic+boundtofail@dachary.org' ; echo POSTFIX TEST ) |
    /usr/sbin/sendmail -v -F 'NO REPLY' -f 'noreply@{}' -t
    """.format(domain))
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc

    check = ("grep -q 'TLS connection established to postfix-host' "
             "/var/log/syslog")
    for _ in range(300):
        print(check)
        cmd = postfix_client_host.run(check)
        if cmd.rc == 0:
            break
        time.sleep(1)

    check = ("grep -q 'connection established to spool.mail.gandi.net' "
             "/var/log/mail.log")
    for _ in range(300):
        print(check)
        cmd = postfix_host.run(check)
        if cmd.rc == 0:
            break
        time.sleep(1)
    assert 0 == postfix_host.run(check).rc


def test_encryption(host):
    cmd = host.run("""
    set -ex
    ( echo Subject: encrypted ; echo ; echo ENCRYPTED CONTENT ) | \
      mail -r debian@localhost debian@localhost
    for d in 0 1 2 4 8 16 32 ; do
       sleep $d
       test -e /var/spool/mail/debian || continue
       grep -q 'PGP MESSAGE' /var/spool/mail/debian || continue
       grep -q 'ENCRYPTED CONTENT' /var/spool/mail/debian && exit 1
       sudo -u zeyple gpg --homedir /var/lib/zeyple/keys --decrypt < /var/spool/mail/debian | \
          grep -q 'ENCRYPTED CONTENT' || continue
       break
    done
    > /var/spool/mail/debian
    ( echo Subject: encrypted ; echo ; echo CLEAR TEXT ) | \
      mail -r debian@localhost debian+notencrypted@localhost
    for d in 0 1 2 4 8 16 32 ; do
       sleep $d
       grep -q 'CLEAR TEXT' /var/spool/mail/debian && break
    done
    > /var/spool/mail/debian
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
