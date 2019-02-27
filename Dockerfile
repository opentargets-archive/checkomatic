FROM python:2.7-alpine
LABEL maintainer="ops@opentargets.org"

RUN pip install certifi opentarget-checkomatic

# point to the entrypoint script
ENTRYPOINT [ "opentargets_checkomatic" ]
