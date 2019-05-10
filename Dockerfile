FROM ubuntu:xenial
MAINTAINER ops @opentargets <ops@opentargets.org>

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python-software-properties \
    build-essential \
    python-dev \
    python \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
	
RUN pip install certifi opentargets-checkomatic

# point to the entrypoint script
ENTRYPOINT [ "opentargets_checkomatic" ]
