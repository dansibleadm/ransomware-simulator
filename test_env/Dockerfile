FROM python:3.10-alpine
SHELL ["/bin/sh", "-c"]
WORKDIR /usr/src/app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
ADD . .

RUN pip3 install --no-cache-dir -r test_env/requirements.txt

RUN chmod +x test_env/autogen.sh && test_env/autogen.sh