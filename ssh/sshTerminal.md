**Starting an interactive shell**

By calling `session.Shell()` in [sshTerminal.go](sshTerminal.go), an interactive login shell is executed, loading whatever default shell the user has and loading the default profile (for example, .profile). The call to `session.RequestPty()` is optional, but the shell works much better when requesting a psuedoterminal. You can set the terminal name to xterm, vt100, linux, or something custom. 

If you have issues with jumbled output due to color values being output, try vt100, and if that still does not work, use a nonstandard terminal name or a terminal name you know does not support colors. Many programs will disable color output if they do not recognize the terminal name. Some programs will not work at all with an unknown terminal type, such as tmux.
More information about Go terminal mode constants is available at [here](https://godoc.org/golang.org/x/crypto/ssh#TerminalModes). Terminal mode flags are a POSIX standard and are defined in RFC 4254, Encoding of Terminal Modes (section 8), which you can find [here](https://tools.ietf.org/html/rfc4254#section-8).

The following example connects to an SSH server using key authentication, and then creates a new session with client.NewSession(). Instead of executing a command with session.Run() like the previous example, we will use session.RequestPty() to get an interactive shell. Standard input, output, and error streams from the remote session are all connected to the local Terminal, so you can interact with it in real time just like any other SSH client (for example, PuTTY).
