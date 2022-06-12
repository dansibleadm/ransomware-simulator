FROM python:3.10-alpine
SHELL ["/bin/sh", "-c"]
WORKDIR /usr/src/app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
ADD . .

RUN pip3 install --no-cache-dir -r test_env/requirements.txt

RUN base64 < /dev/urandom | head -c 1000 > /test_1.txt \
	&& base64 < /dev/urandom | head -c 100 > /tmp/test_2.txt \
	&& base64 < /dev/urandom | head -c 1001 > /home/test_3.txt \
	&& base64 < /dev/urandom | head -c 1005 > /opt/test_1.txt