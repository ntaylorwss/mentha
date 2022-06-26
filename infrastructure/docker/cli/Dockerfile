# syntax=docker/dockerfile:experimental

# python:3.10-slim
FROM python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4

# linux packages
RUN apt-get update && apt-get install -y gcc build-essential curl openssh-client git sudo

# make user
# add user to sudoers group without password so that we can install linux packages for experiments
RUN useradd -ms /bin/bash mentha && usermod -aG sudo mentha && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# docker config
WORKDIR /home/mentha/repo

# set environment
ENV PATH "/home/mentha/.local/bin:${PATH}"
ENV PYTHONPATH "/home/mentha/local-site-packages:${PYTHONPATH}"
RUN mkdir -p \
        /home/mentha/.cache/pip \
        /home/mentha/local-site-packages \
        /home/mentha/repo \
        /home/mentha/repo/.git && \
    chown -R mentha:mentha \
        /home/mentha/.cache/pip \
        /home/mentha/local-site-packages \
        /home/mentha/repo

# install pip
RUN apt-get update && apt-get install -y curl
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py

USER mentha

# install requirements from mentha packages
COPY --chown=mentha:mentha \
    mentha/scraping/requirements.txt /home/mentha/repo/mentha/scraping/requirements.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/mentha/scraping/requirements.txt

COPY --chown=mentha:mentha \
    mentha/api/requirements.txt /home/mentha/repo/mentha/api/requirements.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/mentha/api/requirements.txt

COPY --chown=mentha:mentha \
    mentha/globals/requirements.txt /home/mentha/repo/mentha/globals/requirements.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/mentha/globals/requirements.txt

# install requirements from cli
COPY --chown=mentha:mentha \
    cli/requirements/base.txt /home/mentha/repo/cli/requirements/base.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/cli/requirements/base.txt

COPY --chown=mentha:mentha \
    cli/requirements/dev.txt /home/mentha/repo/cli/requirements/dev.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/cli/requirements/dev.txt

COPY --chown=mentha:mentha \
    cli/requirements/typing.txt /home/mentha/repo/cli/requirements/typing.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/mentha/repo/cli/requirements/typing.txt

# install dependencies from services for typing
COPY --chown=mentha:mentha \
    services/scraper/requirements.txt /home/mentha/repo/services/scraper/requirements.txt
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --user --no-deps -r /home/mentha/repo/services/scraper/requirements.txt

# install mentha packages
COPY --chown=mentha:mentha mentha /home/mentha/repo/mentha
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps \
    -e /home/mentha/repo/mentha/scraping \
    -e /home/mentha/repo/mentha/api \
    -e /home/mentha/repo/mentha/globals

# install cli
COPY --chown=mentha:mentha \
    cli /home/mentha/repo/cli
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps -e /home/mentha/repo/cli

# install services
COPY --chown=mentha:mentha \
    services /home/mentha/repo/services
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps -e /home/mentha/repo/services/scraper
RUN \
    --mount=type=cache,target=/home/mentha/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps -e /home/mentha/repo/services/scraper

# insert infrastructure
COPY --chown=mentha:mentha \
    infrastructure /home/mentha/repo/infrastructure

# insert stubs
COPY --chown=mentha:mentha \
    .stubs /home/mentha/repo/.stubs

# insert pyproject.toml
COPY --chown=mentha:mentha \
    pyproject.toml /home/mentha/repo/pyproject.toml
