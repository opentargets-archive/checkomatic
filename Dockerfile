FROM python:2.7-slim
LABEL maintainer="ops@opentargets.org"

#need make gcc etc for requirements later
#need git to pip install from git
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl
	
RUN pip install certifi opentargets-checkomatic

# point to the entrypoint script
ENTRYPOINT [ "opentargets_checkomatic" ]
