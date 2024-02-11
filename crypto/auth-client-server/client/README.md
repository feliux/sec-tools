
```sh
$ openssl req -nodes -x509 -newkey rsa:4096 -keyout clientKey.pem -out clientCrt.pem -days 365 -subj "/C=US/ST=CA/O=Acme, Inc./CN=example.com"

$ curl -ik -X GET --cert clientCrt.pem --key clientKey.pem https://127.0.0.1:9443/hello
```
