#!/bin/sh

# test.txt
mkdir /home/test
base64 < /dev/urandom | head -c 1404 > /home/test/test.txt && cp /home/test/test.txt /etc/test.txt

# new_test.txt
base64 < /dev/urandom | head -c 4000 > /new_test.txt

# flag.txt
base64 < /dev/urandom | head -c 666 > /tmp/flag.txt && cp /tmp/flag.txt /usr/flag.txt