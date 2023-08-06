from enough.common import host
from enough.common import tcp
from enough import settings


def test_docker_create_or_update(tmpdir, docker_name, tcp_port):
    h = host.HostDocker(str(tmpdir), settings.SHARE_DIR, **{
        'name': docker_name,
        'domain': docker_name,
        'port': tcp_port,
    })
    h.create_or_update()
    assert '"Status":"healthy"' in h.d.get_logs()
    h.d.down()


def test_docker_create_or_update_same_network(tmpdir, docker_name):
    name1 = f'{docker_name}1'
    port1 = tcp.free_port()
    host1 = host.HostDocker(f'{tmpdir}/1', settings.SHARE_DIR, **{
        'name': name1,
        'domain': docker_name,
        'port': port1,
    })
    host1.create_or_update()
    assert '"Status":"healthy"' in host1.d.get_logs()

    name2 = f'{docker_name}2'
    port2 = tcp.free_port()
    host2 = host.HostDocker(f'{tmpdir}/2', settings.SHARE_DIR, **{
        'name': name2,
        'domain': docker_name,
        'port': port2,
    })
    host2.create_or_update()
    assert '"Status":"healthy"' in host2.d.get_logs()

    assert host2.d.docker_compose.exec('-T', name2, 'ping', '-c1', name1)


def test_docker_delete(tmpdir, docker_name, tcp_port):
    domain = f'{docker_name}.domain'
    h = host.HostDocker(str(tmpdir), settings.SHARE_DIR, **{
        'name': docker_name,
        'domain': domain,
        'port': tcp_port,
    })

    def count():
        r = h.d.docker.ps('-q', '--format=json', '--filter', f'label=enough={domain}')
        o = r.stdout.strip().decode('utf8')
        if o:
            return len(o.split('\n'))
        else:
            return 0

    assert count() == 0
    h.create_or_update()
    assert '"Status":"healthy"' in h.d.get_logs()
    assert count() == 1

    related_container = f'extra_{docker_name}'
    h.d.docker.run('--name', related_container,
                   '--label', f'enough={domain}',
                   '--detach',
                   'debian:buster', 'sleep', '3600')
    assert count() == 2
    h.delete()
    assert count() == 0


def test_host_factory(request, tmpdir):
    h = host.host_factory(config_dir=tmpdir, driver='docker', domain='a.b')
    assert type(h).__name__ == 'HostDocker'
    h = host.host_factory(config_dir=tmpdir, driver='openstack', domain='a.b',
                          provider=request.config.option.provider)
    assert type(h).__name__ == 'HostOpenStack'
