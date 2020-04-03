## Dockerfile
## https://docker.github.io/engine/reference/builder/
FROM python:3.8-slim

ADD . /tmp/src/
RUN set -ex; \
    cd /tmp/src/ \
    && python3 -m pip install --no-cache-dir .[gunicorn] \
    && rm -rf /tmp/src
ADD entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
