ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache pjsua python3 py3-pip

# for debugging, add SSH
RUN apk add openssh
RUN passwd -d root
RUN ssh-keygen -A
COPY authorized_keys /

COPY requirements.txt /
RUN pip3 install -r /requirements.txt && rm -f /requirements.txt

COPY start.sh /
RUN chmod a+x /start.sh

COPY run.py testfile.wav /
RUN chmod a+x /run.py

WORKDIR /data

EXPOSE 80 22

CMD [ "/start.sh" ]
