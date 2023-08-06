import os
import yaml

from enough.common.dotenough import Hosts, DotEnough, DotEnoughOpenStack


#
# Hosts
#
def test_hosts_create_delete(tmpdir):
    config_dir = str(tmpdir)
    h = Hosts(config_dir)
    host = 'HOST'
    ip = '1.2.3.4'
    port = '22'
    assert h.create_or_update(host, ip, port) is True
    assert h.create_or_update(host, ip, port) is False
    assert os.path.exists(f'{config_dir}/inventory/hosts.yml')
    h = Hosts(config_dir)
    assert h.create_or_update(host, ip, port) is False
    assert h.hosts[host]['ansible_host'] == ip
    assert h.hosts[host]['ansible_port'] == port

    assert h.missings([host, 'MISSING']) == ['MISSING']

    h.delete(host)
    h = Hosts(config_dir)
    assert h.hosts == {}


def test_hosts_ensure(tmpdir):
    config_dir = str(tmpdir)
    h = Hosts(config_dir)
    host = 'HOST'
    assert h.ensure(host) is True
    assert h.ensure(host) is False
    assert os.path.exists(f'{config_dir}/inventory/hosts.yml')
    h = Hosts(config_dir)
    assert h.ensure(host) is False
    assert h.hosts[host] == {}


#
# DotEnough
#
def test_service_add_to_group(tmpdir):
    d = DotEnough(tmpdir, 'test.com')
    service = 'SERVICE'
    group = DotEnough.service2group(service)
    host = 'HOST'
    expected = {
        group: {
            'hosts': {
                host: None,
            }
        }
    }
    assert d.service_add_to_group(service, host) == expected
    assert d.service_add_to_group(service, host) == expected
    other_host = 'OTHER'
    expected[group]['hosts'][other_host] = None
    assert d.service_add_to_group(service, other_host) == expected
    os.system(f'cat {tmpdir}/services.yml')


def test_openstack_openrc2clouds(tmpdir):

    openrc_file = f'{tmpdir}/openrc.sh'
    clouds_file = f'{tmpdir}/clouds.yml'

    auth_url = 'https://auth.cloud.ovh.net/v3/'
    project_name = 'project_name'
    project_id = 'project_id'
    username = 'username'
    password = 'password'
    region_name = 'region_name'
    clone_region_name = 'DE1'

    auth = {
        'auth_url': auth_url,
        'project_name': project_name,
        'project_id': project_id,
        'user_domain_name': "Default",
        'username': username,
        'password': password,
    }
    expected = {
        'clouds': {
            'production': {
                'region_name': region_name,
                'auth': auth,
            },
            'clone': {
                'region_name': clone_region_name,
                'auth': auth,
            }
        }
    }

    openrc_1 = f"""
#!/bin/bash

# To use an Openstack cloud you need to authenticate against keystone, which
# returns a **Token** and **Service Catalog**. The catalog contains the
# endpoint for all services the user/tenant has access to - including nova,
# glance, keystone, swift.
#
export OS_AUTH_URL={auth_url}
export OS_IDENTITY_API_VERSION=3

export OS_USER_DOMAIN_NAME=$OS_USER_DOMAIN_NAME:-"Default"
export OS_PROJECT_DOMAIN_NAME=$OS_PROJECT_DOMAIN_NAME:-"Default"s


# With the addition of Keystone we have standardized on the term **tenant**
# as the entity that owns the resources.
export OS_TENANT_ID={project_id}
export OS_TENANT_NAME="{project_name}"

# In addition to the owning entity (tenant), openstack stores the entity
# performing the action as the **user**.
export OS_USERNAME="{username}"

# With Keystone you pass the keystone password.
#echo "Please enter your OpenStack Password: "
#read -sr OS_PASSWORD_INPUT
#export OS_PASSWORD=$OS_PASSWORD_INPUT
export OS_PASSWORD={password}

# If your configuration has multiple regions, we set that information here.
# OS_REGION_NAME is optional and only valid in certain environments.
export OS_REGION_NAME="{region_name}"
# Don't leave a blank variable, unset it if it was empty
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
    """
    open(openrc_file, 'w').write(openrc_1)

    assert DotEnoughOpenStack.openrc2clouds(
        openrc_file, clouds_file) == expected['clouds']['production']
    assert yaml.safe_load(open(clouds_file)) == expected
    os.unlink(openrc_file)
    os.unlink(clouds_file)

    openrc_2 = f"""
#!/usr/bin/env bash
# To use an OpenStack cloud you need to authenticate against the Identity
# service named keystone, which returns a **Token** and **Service Catalog**.
# The catalog contains the endpoints for all services the user/tenant has
# access to - such as Compute, Image Service, Identity, Object Storage, Block
# Storage, and Networking (code-named nova, glance, keystone, swift,
# cinder, and neutron).
#
# *NOTE*: Using the 3 *Identity API* does not necessarily mean any other
# OpenStack API is version 3. For example, your cloud provider may implement
# Image API v1.1, Block Storage API v2, and Compute API v2.0. OS_AUTH_URL is
# only for the Identity API served through keystone.
export OS_AUTH_URL={auth_url}
# With the addition of Keystone we have standardized on the term **project**
# as the entity that owns the resources.
export OS_PROJECT_ID={project_id}
export OS_PROJECT_NAME="{project_name}"
export OS_USER_DOMAIN_NAME="Default"
if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi
export OS_PROJECT_DOMAIN_ID="default"
if [ -z "$OS_PROJECT_DOMAIN_ID" ]; then unset OS_PROJECT_DOMAIN_ID; fi
# unset v2.0 items in case set
unset OS_TENANT_ID
unset OS_TENANT_NAME
# In addition to the owning entity (tenant), OpenStack stores the entity
# performing the action as the **user**.
export OS_USERNAME="{username}"
# With Keystone you pass the keystone password.
#echo "Please enter your OpenStack Password for project $OS_PROJECT_NAME as user $OS_USERNAME: "
#read -sr OS_PASSWORD_INPUT
export OS_PASSWORD={password}
# If your configuration has multiple regions, we set that information here.
# OS_REGION_NAME is optional and only valid in certain environments.
export OS_REGION_NAME="{region_name}"
# Don't leave a blank variable, unset it if it was empty
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
    """
    open(openrc_file, 'w').write(openrc_2)

    assert DotEnoughOpenStack.openrc2clouds(
        openrc_file, clouds_file) == expected['clouds']['production']
    assert yaml.safe_load(open(clouds_file)) == expected
    os.unlink(clouds_file)

    expected['clouds']['production']['auth']['password'] = 'PLACEHOLDER'
    openrc_3 = f"""
export OS_AUTH_URL={auth_url}
export OS_PROJECT_ID={project_id}
export OS_PROJECT_NAME="{project_name}"
export OS_USERNAME="{username}"
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
export OS_REGION_NAME="{region_name}"
    """
    open(openrc_file, 'w').write(openrc_3)

    assert DotEnoughOpenStack.openrc2clouds(
        openrc_file, clouds_file) == expected['clouds']['production']
    assert yaml.safe_load(open(clouds_file)) == expected
    os.unlink(clouds_file)

    assert DotEnoughOpenStack.set_missing_config_file_from_openrc(openrc_file, clouds_file) is True
    assert DotEnoughOpenStack.set_missing_config_file_from_openrc(openrc_file, clouds_file) is False
