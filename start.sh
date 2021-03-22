#!/bin/sh

mkdir -p ~/.ssh
cp /authorized_keys ~/.ssh/

/usr/sbin/sshd
/run.py
