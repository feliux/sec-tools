## Pillaging a filesystem

Walks a user-supplied filesystem path recursively, matching against a list of interesting filenames that you would deem useful as part of a post-exploitation exercise. These files may contain, among other things, personally identifiable information, user names, passwords, system logins, and password database files.

The utility looks specifically at filenames rather than file contents, and the script is made much simpler by the fact that Go contains standard functionality in its path/filepath package that you can use to easily walk a directory structure.

### Usage

```go
$ go run pillaging.go ./somepath
```
