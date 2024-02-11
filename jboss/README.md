## Exploiting JBoss

Java deserialization vulnerability released in 2015. The vulnerability, categorized under several CVEs, affects the deserialization of Java objects in common applications, servers, and libraries. This vulnerability is introduced by a deserialization library that doesn’t validate input prior to server-side execution (a com-
mon cause of vulnerabilities).

We’ll narrow our focus to exploiting JBoss (CVE-2015-4852), a popular Java Enterprise Edition application server.

You’ll find a Python script that contains logic to exploit the vulnerability in multiple applications [here](https://github.com/powned/serialator).
