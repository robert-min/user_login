FROM ubuntu:20.04

ARG EXPOSE_PORT=11211
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

USER root
RUN apt-get update -y && apt-get upgrade -y && \
apt-get install -y --no-install-recommends && \
apt-get install -y tzdata && \
apt install -y memcached libmemcached-tools systemd

EXPOSE ${EXPOSE_PORT}

USER memcache
CMD ["memcached", "-u", "memcache", "-m", "64", "-p", "11211", "-l", "0.0.0.0"]