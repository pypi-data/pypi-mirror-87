FROM debian:buster
ARG USER_NAME
ENV USER_NAME ${USER_NAME:-root}
ARG DOCKER_GID
ENV DOCKER_GID ${DOCKER_GID:-999}
ARG USER_ID
ENV USER_ID ${USER_ID:-0}

RUN apt-get update && \
    apt-get install --quiet -y curl virtualenv python3 gcc libffi-dev libssl-dev python3-dev make git rsync \
                               systemd systemd-sysv sudo openvpn \
			       openssh-server
RUN groupadd --gid $DOCKER_GID docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
RUN curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

RUN if test $USER_NAME != root ; then useradd --no-create-home --home-dir /tmp --uid $USER_ID --groups $DOCKER_GID $USER_NAME && echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers ; fi
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs

WORKDIR /opt
RUN virtualenv --python=python3 venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip3 install pipenv
