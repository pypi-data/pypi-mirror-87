#!/usr/bin/env bash
export OS_AUTH_URL={{ clouds[openstack_cloud].auth.auth_url }}
export OS_IDENTITY_API_VERSION=3
export OS_PROJECT_NAME={{ clouds[openstack_cloud].auth.project_name }}
export OS_PROJECT_ID={{ clouds[openstack_cloud].auth.project_id }}
export OS_USER_DOMAIN_NAME={{ clouds[openstack_cloud].auth.user_domain_name }}
export OS_USERNAME={{ clouds[openstack_cloud].auth.username }}
export OS_PASSWORD={{ clouds[openstack_cloud].auth.password }}
export OS_REGION_NAME={{ clouds[openstack_cloud].region_name }}
