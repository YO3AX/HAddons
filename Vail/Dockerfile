ARG BUILD_FROM
#FROM $BUILD_FROM
FROM python:3

ENV LANG C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install requirements for add-on
RUN apk add --no-cache python3 py3-pip
RUN pip install -r aiohttp==2.0.7

# Set working directory
WORKDIR /
# Copy data for add-on
COPY rootfs /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
