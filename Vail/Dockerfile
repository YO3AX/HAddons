ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install requirements for add-on
RUN \
     apk add --no-cache \
          python3 \
          py3-pip \
      \
      && pip3 install aiohttp==3.9.5

# Set working directory
WORKDIR /
# Copy data for add-on
COPY rootfs /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
