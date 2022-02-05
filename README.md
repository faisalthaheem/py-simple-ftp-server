# py-simple-ftp-server
A simple FTP server written in python.

> Warning! This is an insecure server, the transfers are unencrypted and credentials are stored in plain-text in the config file. Use only if you understand the risks involved.

# Running using docker
It's straight forward to run the server, for instance the following command will start a docker container listening on port 2121 with the default username and password of backups/backups.
The only important thing to remember is to always run the container on host network as presently the app does not cater for NAT.

```bash
docker run --rm --net=host faisalthaheem/py-simple-ftp-server:main
```

It is also possible to pass custom configuration and mount a directory on the host to store all the data. The following assumes you have configured the config file as follows
```yaml
dev:
  server_port: 2121
  accounts:
    - username: "backups"
      password: "backups"
      upload-path: './storage-for-backups'

prod:
  server_port: 2121
  accounts:
    - username: "backups"
      password: "backups"
      upload-path: './storage-for-backups'
```

```bash
docker run --net=host -v $PWD/config:/app/config -v $PWD/external-storage:/app/storage-for-backups faisalthaheem/py-simple-ftp-server:main
```