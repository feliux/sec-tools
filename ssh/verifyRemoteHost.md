**Verifying remote host**

To verify the remote host, in `ssh.ClientConfig` from [verifyRemoteHost.go](verifyRemoteHost.go), set `HostKeyCallback` to `ssh.FixedHostKey()` and pass it the public key of the remote host. If you attempt to connect to the server and it provides a different public key, the connection will be aborted. This is important for ensuring that you are connecting to the expected server and not a malicious server. If DNS is compromised, or an attacker performs a successful ARP spoof, it's possible that your connection will be redirected or will be a victim of the man-in-the-middle attack, but an attacker will not be able to imitate the real server without the corresponding private key for the server. For testing purposes, you may choose to ignore the key provided by the remote host.

This example is the most secure way to connect. It uses a key to authenticate, as opposed to a password, and it verifies the public key of the remote server.

This method will use `ssh.ParseKnownHosts()`. This uses the standard `known_hosts` file. The `known_hosts` format is the standard for OpenSSH. The format is documented in the `sshd` manual page.

Note that Go's `ssh.ParseKnownHosts()` will only parse a single entry, so you should create a unique file with a single entry for the server or ensure that the desired entry is at the top of the file.

To obtain the remote server's public key for verification, use `ssh-keyscan`. This returns the server key in the `known_hosts` format that will be used in the following example. Remember, the Go `ssh.ParseKnownHosts` command only reads the first entry from a `known_hosts` file: `ssh-keyscan yourserver.com`

The `ssh-keyscan` program will return multiple key types unless a key type is specified with the -t flag. Make sure that you choose the one with the desired key algorithm and that `ssh.ClientConfig()` has `HostKeyAlgorithm` listed to match. This example includes every possible `ssh.KeyAlgo*` option. I recommend that you choose the highest-strength algorithm possible and only allow that option.
