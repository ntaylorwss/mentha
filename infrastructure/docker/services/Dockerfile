FROM selenium/standalone-chrome@sha256:1d54694c0174dad86dec06e196918919eeef669d8e5b9a57bd09cb6f00c522d5

# make user
USER root
RUN mkdir -p \
        /home/seluser/work \
        /home/seluser/repo \
        /home/seluser/.cache && \
    chown -R seluser:seluser \
        /home/seluser/work \
        /home/seluser/repo \
        /home/seluser/.cache

# install python from image
# version: 3.10
COPY --from=python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4 \
    /usr/local/bin/python /usr/local/bin/python
COPY --from=python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4 \
    /usr/local/bin/pip /usr/local/bin/pip
COPY --from=python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4 \
    /usr/local/lib /usr/local/lib
COPY --from=python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4 \
    /usr/local/include/python3.10 /usr/local/include/python3.10
COPY --from=python@sha256:678346507112562ab8bbbfeb153535fade07f7e01281e3490a8a719104d19ec4 \
    /lib/x86_64-linux-gnu/libexpat.so.1 /lib/x86_64-linux-gnu/libexpat.so.1
RUN echo /usr/local/lib > /etc/ld.so.conf.d/python310.conf && ldconfig

# install gunicorn conf and start script
COPY --chown=paystone:paystone \
    infrastructure/docker/services/gunicorn_conf.py /home/seluser/gunicorn_conf.py
COPY --chown=paystone:paystone \
    infrastructure/docker/services/start /home/seluser/start

# base linux packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential curl lsb-release

# docker config
ARG SERVICE
ENV SERVICE ${SERVICE}
WORKDIR /home/seluser/repo
CMD /home/seluser/start ${SERVICE}

# set environment
ENV PATH "/home/seluser/.local/bin:${PATH}"

USER seluser
# install requirements for seluser packages
COPY --chown=seluser:seluser \
    mentha/scraping/requirements.txt /home/seluser/repo/mentha/scraping/requirements.txt
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/seluser/repo/mentha/scraping/requirements.txt

COPY --chown=seluser:seluser \
    mentha/api/requirements.txt /home/seluser/repo/mentha/api/requirements.txt
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/seluser/repo/mentha/api/requirements.txt

COPY --chown=seluser:seluser \
    mentha/globals/requirements.txt /home/seluser/repo/mentha/globals/requirements.txt
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/seluser/repo/mentha/globals/requirements.txt

# install requirements for services
COPY --chown=seluser:seluser \
    services/$SERVICE/requirements.txt /home/seluser/repo/services/$SERVICE/requirements.txt
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/seluser/repo/services/$SERVICE/requirements.txt

# install mentha packages
COPY --chown=seluser:seluser mentha /home/seluser/repo/mentha
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps \
        -e /home/seluser/repo/mentha/scraping \
        -e /home/seluser/repo/mentha/api \
        -e /home/seluser/repo/mentha/globals

# install service
COPY --chown=seluser:seluser services /home/seluser/repo/services
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install -e /home/seluser/repo/services/$SERVICE
