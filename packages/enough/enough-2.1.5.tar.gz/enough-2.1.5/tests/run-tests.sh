#!/bin/bash

# ENOUGH_API_TOKEN=abc tests/run-tests.sh tox -e openvpn -- --enough-no-create --enough-no-tests playbooks/openvpn/tests

set -e

function prepare_environment() {
    if test $(id -u) != 0 ; then
        SUDO=sudo
    fi
    if test "$(dpkg-query -W -f='${db:Status-Abbrev}' git)" != "ii " ; then
        $SUDO apt-get update
        $SUDO apt-get install -y git
    fi
    if test -d ~/.ansible && test "$(find ~/.ansible ! -user $(id -u) -print -quit)" ; then
        $SUDO chown -R $(id -u) ~/.ansible
    fi
}

function prepare_repository() {
    git submodule update --init --recursive
    if test -f infrastructure_key ; then
        chmod 600 infrastructure_key
    fi
}

function prepare_inventory() {
    if ! test -f inventory/group_vars/all/clouds.yml ; then
        if test -z "$OS_AUTH_URL" ; then
            echo OS_AUTH_URL is not set, source openrc.sh
            exit 1
        fi
        cat > tests/clouds.yml <<EOF
---
clouds:
  production:
    auth: &os_auth
      auth_url: "$OS_AUTH_URL"
      project_name: "${OS_PROJECT_NAME:-$OS_TENANT_NAME}"
      project_id: "${OS_PROJECT_ID:-$OS_TENANT_ID}"
      user_domain_name: "$OS_USER_DOMAIN_NAME"
      username: "$OS_USERNAME"
      password: "$OS_PASSWORD"
    region_name: "$OS_REGION_NAME"
  clone:
    auth:
      <<: *os_auth
    region_name: "DE1"
EOF
        cp tests/clouds.yml inventory/group_vars/all/clouds.yml
    else
        cat inventory/group_vars/all/clouds.yml > tests/clouds.yml
    fi

    if ! test -f inventory/group_vars/all/domain.yml ; then
        cat > tests/domain.yml <<EOF
---
domain: enough.community
EOF
        cp tests/domain.yml inventory/group_vars/all/domain.yml
    else
        cat inventory/group_vars/all/domain.yml > tests/domain.yml
    fi
}

function image_name() {
    if test "$GITLAB_CI" ; then
        echo enough-tox-$(date +%s)
        trap "docker rm -f $name >& /dev/null || true ; docker rmi --no-prune $name >& /dev/null || true"  EXIT
    else
        echo enough-tox-$(pwd | md5sum | cut -f1 -d' ')
    fi
}

function build_image() {
    local name="$1"
    local max_execution_time="$2"

    (
        cat enough/common/data/base.dockerfile
        cat tests/tox.dockerfile
        if test "$GITLAB_CI" ; then
            cat tests/copy-to-opt.dockerfile
        fi
    ) | timeout $max_execution_time docker build --build-arg=USER_ID="$(id -u)" --build-arg=DOCKER_GID="$(getent group docker | cut -d: -f3)" --build-arg=USER_NAME="${USER:-root}" --tag $name -f - .
}

function run_tests_on_ref() {
    local ref="$1"
    local name="$2"
    local toplevel="$3"
    local service="$4"

    local basedir=$(dirname $toplevel)
    local refdir="$basedir/infrastructure-versions/$ref"
    mkdir -p $refdir
    if ! test -d $refdir/infrastructure ; then
        git clone --reference . . $refdir/infrastructure
    fi

    (
        cd $refdir/infrastructure

        rm -f .tox/*/.pytest_cache/d/dotenough/*.test/inventory/hosts.yml
        run_tests $name $refdir/infrastructure tox -e $service -- --enough-no-destroy playbooks/$service/tests

        local c=.tox/$service/.pytest_cache/d
        mkdir -p $toplevel/$c
        rsync -av --delete $c/ $toplevel/$c/
    )
}

function run_tests() {
    local name="$1"
    shift
    local d="$1"
    shift

    prepare_inventory
    prepare_repository

    find $d \( -name '*.pyc' -o -name '*.pyo' -o -name __pycache__ \) -delete
    if test "$GITLAB_CI" ; then
        args="--workdir /opt"
        : ${PYTEST_ADDOPTS=-m \"not openstack_integration\"}
        PASS_GITLAB_CI="-e GITLAB_CI=${GITLAB_CI}"
    else
        args="--volume ${d}:${d} --workdir ${d} --volume $HOME/.enough:$HOME/.enough --volume $HOME/.ansible:$HOME/.ansible -e HOME=$HOME"
        # handle git worktree
        git_dir="$(git rev-parse --absolute-git-dir)"
        if [ "${git_dir}" != "${d}/.git" ]; then
            git_common_dir="$(git rev-parse --git-common-dir)"
            args="$args --volume ${git_common_dir}:${git_common_dir}"
        fi
        PASS_GITLAB_CI=""
	local interactive=-ti
    fi
    docker run $interactive --rm --device=/dev/net/tun --name $name --user "${USER:-root}" -e PYTEST_ADDOPTS="${PYTEST_ADDOPTS-}" -e ENOUGH_API_TOKEN=$ENOUGH_API_TOKEN ${PASS_GITLAB_CI} --cap-add=NET_ADMIN $args --volume /var/run/docker.sock:/var/run/docker.sock $name "${@:-tox}"
}

function main() {
    prepare_environment
    prepare_inventory

    local name=$(image_name "$@")
    echo -n Creating or refreshing the docker image to run the tests...
    build_image $name 15 < /dev/null > /dev/null 2>&1 || build_image $name 7200
    echo done!
    local toplevel=$(git rev-parse --show-toplevel)
    if test "$1" = "--upgrade" ; then
        shift
        local ref="$1"
        local service="$2"
        run_tests_on_ref $ref $name $toplevel $service
        run_tests $name $toplevel tox -e $service
    else
        run_tests $name $toplevel "$@"
    fi
}

main "$@"
