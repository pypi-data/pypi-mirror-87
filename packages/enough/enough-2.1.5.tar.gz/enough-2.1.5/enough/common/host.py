import os
from abc import ABC, abstractmethod
import shutil
import tempfile

from enough import settings
from enough.common import openstack
from enough.common import docker
from enough.common import dotenough
from enough.common import tcp


class Host(ABC):

    def __init__(self, config_dir, share_dir, **kwargs):
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.args = kwargs

    @abstractmethod
    def create_or_update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class HostDocker(Host):

    class DockerInfrastructure(docker.Docker):

        def __init__(self, config_dir, **kwargs):
            self.config_dir = config_dir
            super().__init__(**kwargs)

        def create_image(self):
            name = super().create_image()
            dockerfile = os.path.join(self.root, 'internal/data/infrastructure.dockerfile')
            with tempfile.TemporaryDirectory() as d:
                shutil.copy(f'{self.config_dir}/infrastructure_key.pub', d)
                return self._create_image(None,
                                          '--build-arg', f'IMAGE_NAME={name}',
                                          '-f', dockerfile, d)

        def get_compose_content(self):
            f = os.path.join(self.root, 'internal/data/infrastructure-docker-compose.yml')
            return self.replace_content(open(f).read())

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughDocker(config_dir, self.args['domain'])
        self.dotenough.ensure()
        self.d = HostDocker.DockerInfrastructure(config_dir, **self.args)

    def create_or_update(self):
        self.d.create_network(self.args['domain'])
        self.d.name = self.args['name']
        port = self.d.get_public_port('22')
        if not port:
            port = tcp.free_port()
            self.args['port'] = port
            self.d = HostDocker.DockerInfrastructure(self.config_dir, **self.args)
            self.d.create_or_update()
        return {
            'ipv4': self.d.get_ip(),
            'port': '22',
        }

    def delete(self):
        domain = self.args['domain']
        for id in self.d.docker.ps('--filter', f'label=enough={domain}', '-q', _iter=True):
            self.d.docker.rm('-f', id.strip())


class HostOpenStack(Host):

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'],
                                                      self.args['provider'])
        self.dotenough.ensure()

    def create_or_update(self):
        dotenough.Hosts(self.config_dir).ensure(self.args['name'])
        h = openstack.Heat(self.config_dir, **self.args)
        s = openstack.Stack(self.config_dir, h.get_stack_definition(self.args['name']), **self.args)
        s.set_public_key(f'{self.config_dir}/infrastructure_key.pub')
        return s.create_or_update()

    def delete(self):
        self.delete_hosts(self.args['name'])

    def delete_hosts(self, names):
        h = openstack.Heat(self.config_dir, **self.args)
        complete_deletion = []
        for name in names:
            s = openstack.Stack(self.config_dir, h.get_stack_definition(name), **self.args)
            if s.delete_no_wait():
                complete_deletion.append(name)
        for name in complete_deletion:
            s = openstack.Stack(self.config_dir, h.get_stack_definition(name), **self.args)
            s.delete_wait()


def host_factory(config_dir=settings.CONFIG_DIR, share_dir=settings.SHARE_DIR, **kwargs):
    if kwargs['driver'] == 'openstack':
        return HostOpenStack(config_dir, share_dir, **kwargs)
    else:
        return HostDocker(config_dir, share_dir, **kwargs)
