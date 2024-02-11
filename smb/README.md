## SMB

### Password guessing with SMB

The first SMB case we’ll examine is a fairly common one for attackers and pen testers: online password guessing over SMB. You’ll try to authenticate to a domain by providing commonly used usernames and passwords.

### Reusing passwords with pass-the-hash technique

The pass-the-hash technique allows an attacker to perform SMB authentication by using a password’s NTLM hash, even if the attacker doesn’t have the cleartext password. This section walks you through the concept and shows you an implementation of it.

Pass-the-hash is a shortcut to a typical Active Directory domain compromise, a type of attack in which attackers gain an initial foothold, elevate their privileges, and move laterally throughout the network until they have the access levels they need to achieve their end goal. Active Directory domain compromises generally follow the roadmap presented in this list, assuming they take place through an exploit rather than something like password guessing:

1. The attacker exploits the vulnerability and gains a foothold on the network.

2. The attacker elevates privileges on the compromised system.

3. The attacker extracts hashed or cleartext credentials from LSASS.

4. The attacker attempts to recover the local administrator password via offline cracking.

5. The attacker attempts to authenticate to other machines by using the administrator credentials, looking for reuse of the password.

6. The attacker rinses and repeats until the domain administrator or other target has been compromised.

With NTLMSSP authentication, however, even if you fail to recover the cleartext password during step 3 or 4, you can proceed to use the password’s NTLM hash for SMB authentication during step 5 (in other words, passing the hash). Pass-the-hash works because it separates the hash calculation from the challenge-response token calculation. To see why this is, let’s look at the following two functions, defined by the NTLMSSP specification, pertaining to the cryptographic and security mechanisms used for authentication.

- **NTOWFv2**: A cryptographic function that creates an MD5 HMAC by using the username, domain, and password values. It generates the NTLM hash value.

- **ComputeResponse**: A function that uses the NTLM hash in combination with the message’s client and server challenges, timestamp, and target server name to produce a GSS-API security token that can be sent for authentication.

### Recovering NTLM passwords

In some instances, having only the password hash will be inadequate for your overall attack chain. For example, many services (such as Remote
Desktop, Outlook Web Access, and others) don’t allow hash-based authentication, because it either isn’t supported or isn’t a default configuration.
If your attack chain requires access to one of these services, you’ll need a cleartext password.
