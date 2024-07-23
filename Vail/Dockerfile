ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3\
    python3-pip \
    \
    && pip3 install --no-cache-dir -U \
        aiohttp \
# Set working directory
WORKDIR /
# Copy data for add-on
COPY rootfs /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
