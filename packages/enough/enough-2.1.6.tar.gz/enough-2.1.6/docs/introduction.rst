Introduction
============

Enough is a platform for journalists, sources and human rights
defenders to communicate privately and securely. It provides the
following services:

* `Nextcloud <https://nextcloud.com/>`__, a suite of client-server
  software for creating and using file hosting services.
* `Discourse <https://www.discourse.org/>`__, a discussion platform
  built for the next decade of the Internet. Use it as a mailing list,
  discussion forum, long-form chat room, and more!
* `Mattermost <https://mattermost.com/>`__, a flexible messaging
  platform that enables secure team collaboration.
* `Hugo <https://gohugo.io/>`__, a static web site generator.
* `Weblate <https://weblate.org/>`__, a libre web-based translation
  tool with tight version control integration. It provides two user
  interfaces, propagation of translations across components, quality
  checks and automatic linking to source files.
* `Wekan <https://wekan.github.io/>`__, a kanban board which allows a
  card-based task and to-do management.
* `Etherpad <https://etherpad.org/>`__, a highly customizable online
  editor providing collaborative editing in really real-time.
* `GitLab <https://gitlab.com/>`__, a web-based DevOps lifecycle tool
  that provides a Git-repository manager providing wiki,
  issue-tracking and continuous integration/continuous deployment
  pipeline features.
* `OpenVPN <https://openvpn.net/>`__, that implements virtual private
  network (VPN) techniques to create secure point-to-point or
  site-to-site connections in routed or bridged configurations and
  remote access facilities

The `enough` CLI controls an OpenStack based infrastructure and the
services that run on top of it, with Ansible.

Requirements
------------

* The ``openrc.sh`` credentials for a ``Public cloud`` project at `OVH
  <https://www.ovh.com/manager/public-cloud/>`__. No other OpenStack
  provider is supported.

* The ``Public cloud`` project has a `Private network
  <https://www.ovh.com/world/solutions/vrack/>`__.

Quick start
-----------

* `Install Docker <http://docs.docker.com/engine/installation/>`__.

* Copy ``openrc.sh`` in ``~/.enough/myname.d.enough.community/openrc.sh`` and edit
  to replace ``$OS_PASSWORD_INPUT`` with the actual password.

* Add the ``enough`` CLI to ``~/.bashrc``:
  ::

     eval "$(docker run --rm enoughcommunity/enough:latest install)"

* Create the ``Nextcloud`` service with:
  ::

     $ enough --domain myname.d.enough.community service create cloud

..  note::
    If the command fails, because of a network failure or any other reason,
    it is safe to run it again. It is idempotent.

* Login ``https://cloud.myname.d.enough.community`` with user ``admin`` password ``mynextcloud``
