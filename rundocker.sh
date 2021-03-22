#!/bin/bash

set -e

touch authorized_keys
docker build . --build-arg BUILD_FROM=alpine:latest -t hass-voip-addon
mkdir -p data
cp options.json data/
ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[localhost]:8022"
docker run -p 8022:22 -p 8000:80 -v "$(pwd)"/data:/data -it hass-voip-addon
