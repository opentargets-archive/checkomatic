FROM python:2.7-alpine
LABEL maintainer="ops@opentargets.org"

RUN apk update && \
    apk add --virtual build-deps gcc python-dev 
	
RUN pip install certifi opentargets-checkomatic

# point to the entrypoint script
ENTRYPOINT [ "opentargets_checkomatic" ]
