def set_options(parser):
    parser.add_argument('--driver', default='openstack')
    parser.add_argument('--inventory', action='append')
    o = parser.add_argument_group(title='OpenStack',
                                  description='Only when --driver=openstack')
    o.add_argument(
        '--cloud',
        default='production',
        help='Name of the cloud in which resources are provisionned')

    o.add_argument(
        '--provider',
        default='ovh',
        choices=('fuga', 'ovh'),
        help='Name of the OpenStack provider')
    return parser
