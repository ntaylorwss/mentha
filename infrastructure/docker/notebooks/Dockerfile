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

# base linux packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential curl lsb-release

# docker config
WORKDIR /home/seluser/work
EXPOSE 8888
CMD ["/home/seluser/start"]

# set environment
ENV PATH "/home/seluser/.local/bin:${PATH}"

# add gcloud
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update -y && \
    apt-get install -y google-cloud-sdk

# install jupyterlab dependencies
RUN mkdir -p \
    /home/seluser/.jupyter/lab /home/seluser/.ipython/profile_default/startup \
    /home/seluser/work/personal /home/seluser/work/common && \
    chown -R seluser:seluser \
    /home/seluser/.jupyter /home/seluser/.ipython \
    /home/seluser/work/personal /home/seluser/work/common
RUN apt-get -y install dirmngr apt-transport-https ca-certificates && \
    curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs

USER seluser
# install jupyterlab and extensions
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user \
    pip==21.2.4 jupyter==1.0.0 jupyterlab==3.4.2 \
    jupyterlab_execute_time \
    jupyterlab-system-monitor

# add universal jupyter config
COPY --chown=seluser:seluser \
    infrastructure/docker/notebooks/start /home/seluser/start
COPY --chown=seluser:seluser \
    infrastructure/docker/notebooks/jupyter_lab_config.py \
    /home/seluser/.jupyter/jupyter_lab_config.py
COPY --chown=seluser:seluser \
    infrastructure/docker/notebooks/disable-warnings.py \
    /home/seluser/.ipython/profile_default/startup/disable-warnings.py

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
    services/scraper/requirements.txt /home/seluser/repo/services/scraper/requirements.txt
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --user -r /home/seluser/repo/services/scraper/requirements.txt

# install mentha packages
COPY --chown=seluser:seluser mentha /home/seluser/repo/mentha
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install --no-deps \
        -e /home/seluser/repo/mentha/scraping \
        -e /home/seluser/repo/mentha/api \
        -e /home/seluser/repo/mentha/globals

# install services
COPY --chown=seluser:seluser services /home/seluser/repo/services
RUN \
    --mount=type=cache,target=/home/seluser/.cache/pip,uid=1000,gid=1000 \
    pip install -e /home/seluser/repo/services/scraper
