**SimpleHTTPSServer with letsencrypt certificate**

```sh
$ apt update
$ apt install software-properties-common
$ add-apt-repository ppa:certbot/certbot
$ apt update
$ mkdir webserver
$ cd webserver
$ apt install certbot
$ mkdir www
$ certbot certonly --webroot -w $PWD/www -d mydomain.org -d www.mydomain.org
$ cp /etc/letsencrypt/live/mydomain.org/privkey.pem .
$ cp /etc/letsencrypt/live/mydomain.org/fullchain.pem .
$ cat privkey.pem fullchain.pem > cert.pem
$ cat https_server.py
$ python https_server.py eth0
```
