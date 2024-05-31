**Signing a certificate request**

When generating a self-signed certificate, we already demonstrated the process for creating a signed certificate. In the self-signed example, we just used the same certificate template as the signee and the signer. For this reason, there is not a separate code example. The only difference is that the parent certificate doing the signing or the template to be signed should be swapped out to a different certificate.

This is the function definition for `x509.CreateCertificate()`:

```go
func CreateCertificate(rand io.Reader, template, parent *Certificate, pub, priv interface{}) (cert []byte, err error)
```

In the self-signed example, the template and parent certificates were the same object. To sign a certificate request, create a new certificate object and populate the fields with the information from the signing request. Pass the new certificate as the template, and use the signer's certificate as the parent. The pub parameter is the signee's public key and the priv parameter is the signer's private key. The signer is the certificate authority and the signee is the requester.
