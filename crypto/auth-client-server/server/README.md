
```sh
$ openssl req -nodes -x509 -newkey rsa:4096 -keyout serverKey.pem -out serverCrt.pem -days 365 -subj "/C=ES/ST=LP/O=Acme, Inc./CN=test.com" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```
