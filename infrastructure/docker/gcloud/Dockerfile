FROM google/cloud-sdk@sha256:f5575b1258033019c6c44329a8179abb8d91110431d3c5c540fdafc8a8f0b74e

ARG DOCKER_GROUP_ID

# make user
RUN deluser cloudsdk && \
    useradd -ms /bin/bash mentha && \
    groupadd -g $DOCKER_GROUP_ID docker && \
    usermod -aG docker mentha


# docker config
USER mentha
WORKDIR /home/mentha/mnt/repo
COPY --chown=mentha:mentha \
    infrastructure/docker/gcloud/config.json /home/mentha/.docker/config.json
