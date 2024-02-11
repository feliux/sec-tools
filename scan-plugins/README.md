# Build go plugins

## Go plugin package

```sh
$ cd tomcat-plugin
$ go build -buildmode=plugin -o ../plugins-go/tomcat.so

$ cd ../cmd
$ go run mainGoPlugin.go
```

## Go lua package

Create lua scripts on `./plugins-lua` path. Then execute

```sh
$ cd cmd
$ go run mainLuaPlugin.go
```

## ToDo

1. Create a plug-in to check for a different vulnerability.

2. Add the ability to dynamically supply a list of hosts and their open ports for more extensive tests.

3. Enhance the code to call only applicable plug-ins. Currently, the code will call all plug-ins for the given host and port. This isn’t ideal. For example, you wouldn’t want to call the Tomcat checker if the target port isn’t HTTP or HTTPS.

4. Convert your plug-in system to run on Windows, using DLLs as the plug-in type.
