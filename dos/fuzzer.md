**Fuzzing a network service**

Fuzzing is when you send intentionally malformed, excessive, or random data to an application in an attempt to make it misbehave, crash, or reveal sensitive information. You can identify buffer overflow vulnerabilities, which can result in remote code execution. If you cause an application to crash or stop responding after you send it data of a certain size, it may be due to a buffer overflow.

Sometimes, you will just cause a denial of service by causing a service to use too much memory or tie up all the processing power. Regular expressions are notoriously slow and can be abused in the URL routing mechanisms of web applications to consume all the CPU with few requests.

Nonrandom, but malformed, data can be just as dangerous, if not more so. A properly malformed video file can cause VLC to crash and expose code execution. A properly malformed packet, with 1 byte altered, can lead to sensitive data being exposed, as in the Heartbleed OpenSSL vulnerability.

The following example will demonstrate a very basic TCP fuzzer. It sends random bytes of increasing length to a server. It starts with 1 byte and grows exponentially by a power of 2. First, it sends 1 byte, then 2, 4, 8, 16, continuing until it returns an error or reaches the maximum configured limit.

Tweak maxFuzzBytes to set the maximum size of data you want to send to the service. Be aware that it launches all the threads at once, so be careful about the load on the server. Look for anomalies in the responses or for a total crash from the server.
