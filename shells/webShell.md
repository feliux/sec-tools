**Creating web shells*`*

A web shell is similar to a bind shell, but, instead of listening as a raw TCP socket, it listens and communicates as an HTTP server. It is a useful method of creating persistent access to a machine.

One reason a web shell may be necessary, is because of firewalls or other network restrictions. HTTP traffic may be treated differently than other traffic. Sometimes the 80 and 443 ports are the only ports allowed through a firewall. Some networks may inspect the traffic to ensure that only HTTP formatted requests are allowed through.

Keep in mind that using plain HTTP means the traffic can be logged in plaintext. HTTPS can be used to encrypt the traffic, but the SSL certificate and key are going to reside on the server so that a server admin will have access to it. All you need to do to make this example use SSL is to change http.ListenAndServe() to http.ListenAndServeTLS(). An example of this is provided in Chapter 9, Web Applications.

The convenient thing about a web shell is that you can use any web browser and command-line tools, such as curl or wget. You could even use netcat and manually craft an HTTP request. The drawback is that you don't have a truly interactive shell, and you can send only one command at a time. You can run multiple commands with one string if you separate multiple commands with a semicolon.

You can manually craft an HTTP request in netcat or a custom TCP client like this:

`GET /?cmd=whoami HTTP/1.0\n\n`

This would be similar to the request that is created by a web browser. For example, if you ran webshell localhost:8080, you could access the URL on port 8080, and run a command with http://localhost:8080/?cmd=df.

Note that the `/bin/sh` shell command is for Linux and Mac. Windows uses the `cmd.exe` Command Prompt. In Windows, you can enable Windows Subsystem for Linux and install Ubuntu from the Windows store to run all of these Linux examples in a Linux environment without installing a virtual machine.

In this next example, the web shell creates a simple web server that listens for requests over HTTP. When it receives a request, it looks for the GET query named cmd. It will execute a shell, run the command provided, and return the results as an HTTP response.
