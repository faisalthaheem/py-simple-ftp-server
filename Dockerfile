FROM python:3.9-alpine
LABEL maintainer="faisal.ajmal@gmail.com"

RUN pip3 install pyftpdlib pyyaml

WORKDIR /app
COPY server/ /app/

EXPOSE 2121

ENTRYPOINT [ "python3","/app/ftp.service.py"]