import logging
import time
import testinfra

testinfra_hosts = ['ansible://psono-host']
logger = logging.getLogger(__name__)


def test_psono_send_mail(host):

    psono_host = host
    postfix_host = testinfra.host.Host.get_host(
        'ansible://postfix-host',
        ansible_inventory=host.backend.ansible_inventory)

    cmd = psono_host.run("""
    cd /srv/psono
    sudo docker-compose run server python3 \
        ./psono/manage.py sendtestemail loic-doomtofail@dachary.org
    """)
    logger.debug('stdout %s', cmd.stdout)
    logger.debug('stderr %s', cmd.stderr)
    assert 0 == cmd.rc

    check = ("grep -q 'connection established to spool.mail.gandi.net' "
             "/var/log/mail.log")
    for _ in range(300):
        print(check)
        cmd = postfix_host.run(check)
        if cmd.rc == 0:
            break
        time.sleep(1)
    assert 0 == postfix_host.run(check).rc
