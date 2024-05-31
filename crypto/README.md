**OpenPGP**

PGP stands for Pretty Good Privacy, and OpenPGP is standard RFC 4880. PGP is a convenient suite for encrypting text, files, directories, and disks. All the principles are the same as discussed in the previous section with SSL and TLS key/certificates. The encrypting, signing, and verification are all the same. Go provides an OpenPGP package. Read more about it at https://godoc.org/golang.org/x/crypto/openpgp.

**Off The Record (OTR) messaging**

Off The Record or OTR messaging is a form of end-to-end encryption for users to encrypt their communication over whatever message medium is being used. It is convenient because you can implement an encrypted layer over any protocol even if the protocol itself is unencrypted. For example, OTR messaging works over XMPP, IRC, and many other chat protocols. Many chat clients such as Pidgin, Adium, and Xabber have support for OTR either natively or via plugin. Go provides a package for implementing OTR messaging. Read more about Go's OTR support at https://godoc.org/golang.org/x/crypto/otr/.
