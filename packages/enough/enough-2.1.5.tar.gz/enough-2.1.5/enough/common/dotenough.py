import copy
import os
import re
import sh
import shutil
import textwrap
import yaml


class Hosts(object):

    def __init__(self, config_dir):
        self.d = f'{config_dir}/inventory'
        self.f = f'{self.d}/hosts.yml'
        self.load()

    def load(self):
        if os.path.exists(self.f):
            self.hosts = yaml.safe_load(open(self.f).read())['all']['hosts']
        else:
            self.hosts = {}
        return self

    def get_ip(self, host):
        return self.hosts.get(host, {}).get('ansible_host')

    def get_port(self, host):
        return self.hosts.get(host, {}).get('ansible_port', '22')

    def save(self):
        if not os.path.exists(self.d):
            os.makedirs(self.d)
        content = yaml.dump(
            {
                'all': {
                    'hosts': self.hosts,
                },
            }
        )
        open(self.f, 'w').write(content)

    def missings(self, names):
        return [name for name in names if name not in self.hosts]

    def ensure(self, name):
        if name not in self.hosts:
            self.hosts[name] = {}
            self.save()
            return True
        else:
            return False

    def create_or_update(self, name, ipv4, port):
        if self.get_ip(name) != ipv4:
            self.hosts[name] = {'ansible_host': ipv4, 'ansible_port': port}
            self.save()
            return True
        else:
            return False

    def delete(self, name):
        if name in self.hosts:
            del self.hosts[name]
        self.save()


class DotEnough(object):

    def __init__(self, config_dir, domain):
        self.domain = domain
        self.config_dir = config_dir
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

    def ensure(self):
        self.ensure_ssh_key()

    def ensure_ssh_key(self):
        path = f'{self.config_dir}/infrastructure_key'
        if not os.path.exists(path):
            sh.ssh_keygen('-f', path, '-N', '', '-b', '4096', '-t', 'rsa')
        return path

    def public_key(self):
        return f'{self.ensure_ssh_key()}.pub'

    def private_key(self):
        return self.ensure_ssh_key()

    def populate_config(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

        if not os.path.exists(f'{d}/private-key.yml'):
            open(f'{d}/private-key.yml', 'w').write(textwrap.dedent(f"""\
            ---
            ansible_ssh_private_key_file: {self.config_dir}/infrastructure_key
            """))

        if not os.path.exists(f'{d}/domain.yml'):
            open(f'{d}/domain.yml', 'w').write(textwrap.dedent(f"""\
            ---
            domain: {self.domain}
            production_domain: {self.domain}
            """))

        if not os.path.exists(f'{d}/certificate.yml'):
            self.set_certificate(certificate_authority)

    @staticmethod
    def service2group(service):
        return f'{service}-service-group'

    def service_add_to_group(self, service, host):
        s = f'{self.config_dir}/inventory/services.yml'
        if os.path.exists(s):
            services = yaml.safe_load(open(s).read())
        else:
            services = {}
        group = self.service2group(service)
        if group not in services:
            services[group] = {'hosts': {}}
        if host not in services[group]['hosts']:
            services[group]['hosts'][host] = None
            open(s, 'w').write(yaml.dump(services, indent=4))
        return services

    def set_certificate(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        open(f'{d}/certificate.yml', 'w').write(textwrap.dedent(f"""\
        ---
        certificate_authority: {certificate_authority}
        """))


class DotEnoughOpenStack(DotEnough):

    def __init__(self, config_dir, domain, provider):
        super().__init__(config_dir, domain)
        self.clouds_file = f'{self.config_dir}/inventory/group_vars/all/clouds.yml'
        self.provider = provider

    def set_clouds_file(self, clouds_file):
        shutil.copy(clouds_file, self.clouds_file)

    def ensure(self):
        super().ensure()
        self.populate_config('letsencrypt')
        self.set_missing_config_file_from_openrc(f'{self.config_dir}/openrc.sh', self.clouds_file)

        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(f'{d}/openstack-provider.yml'):
            open(f'{d}/openstack-provider.yml', 'w').write(textwrap.dedent(f"""\
            ---
            openstack_provider: {self.provider}
            """))

    @staticmethod
    def set_missing_config_file_from_openrc(openrc, config_file):
        if os.path.exists(openrc) and not os.path.exists(config_file):
            DotEnoughOpenStack.openrc2clouds(openrc, config_file)
            return True
        else:
            return False

    @staticmethod
    def openrc2clouds(openrc, clouds):
        c = {
            'auth': {
                'user_domain_name': 'Default',
                'password': 'PLACEHOLDER',
            }
        }
        for line in open(openrc).readlines():
            r = re.search(r'export\s+(OS_\w+)="(.*)"', line)
            if not r:
                r = re.search(r'export\s+(OS_\w+)=(.*)\s*', line)
                if not r:
                    continue
            (k, v) = r.group(1, 2)
            if k == 'OS_REGION_NAME':
                c['region_name'] = v
            elif k == 'OS_AUTH_URL':
                c['auth']['auth_url'] = v
            elif k == 'OS_PROJECT_NAME' or k == 'OS_TENANT_NAME':
                c['auth']['project_name'] = v
            elif k == 'OS_PROJECT_ID' or k == 'OS_TENANT_ID':
                c['auth']['project_id'] = v
            elif k == 'OS_USERNAME':
                c['auth']['username'] = v
            elif k == 'OS_PASSWORD' and v != '$OS_PASSWORD_INPUT':
                c['auth']['password'] = v
        clone = copy.deepcopy(c)
        clone['region_name'] = 'DE1'
        open(clouds, 'w').write(yaml.dump({
            'clouds': {
                'production': c,
                'clone': clone,
            }
        }))
        return c


class DotEnoughDocker(DotEnough):

    def ensure(self):
        super().ensure()
        self.populate_config('ownca')
