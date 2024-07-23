ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
    apk add --no-cache \
        py3-pip \
        python3 \
    && pip3 install \
        aiiohttp \
    \
# Set working directory
WORKDIR /
# Copy data for add-on
COPY rootfs /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
