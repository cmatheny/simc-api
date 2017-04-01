FROM cmatheny/simc:latest

RUN apk add --no-cache python3
RUN pip3 install -U pip
RUN pip3 install -U \
    eve \
    setuptools

EXPOSE 5000

RUN mkdir /api
COPY scripts /api

ENTRYPOINT [ "python3", "/api/run.py" ]
