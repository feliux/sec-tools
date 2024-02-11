import BaseHTTPServer
import SimpleHTTPServer
import os
import ssl
import sys

port = 443

iface = sys.argv[1]
ipv4 = os.popen("ip addr show " + iface).read().split("inet ")[1].split("/")[0]

cwd = os.getcwd()
certfile = cwd + "/cert.pem"
wwwdir = cwd + "/www"

os.chdir(wwwdir)

httpd = BaseHTTPServer.HTTPServer(
    (ipv4, port),
    SimpleHTTPServer.SimpleHTTPRequestHandler
)

httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile=certfile,
    server_side=True
)

httpd.serve_forever()
