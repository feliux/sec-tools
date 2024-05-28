## Dirty COW

The vulnerability, dubbed Dirty COW, pertains to a race condition within the Linux kernel’s memory subsystem. This flaw affected most, if not all, common Linux and Android distributions at the time of disclosure. The vulnerability has since been patched, so you’ll need to take some specific measures to reproduce the examples that follow. Specifically, you’ll need to configure a Linux system with a vulnerable kernel version. Setting this up is beyond the scope of the chapter; however, for reference, we use a 64-bit Ubuntu 14.04 LTS distribution with kernel version 3.13.1.

**C**

Several variations of the exploit are publicly available. You can find the one we intend to replicate at [exploit-db](https://www.exploit-db.com/exploits/40616).

The [exploit](40616.c) defines some malicious shellcode, in Executable and Linkable Format (ELF), that generates a Linux shell. It executes the code as a privileged user by creating multiple threads that call various system functions to write our shellcode to memory locations. Eventually, the shellcode exploits the vulnerability by overwriting the contents of a binary executable file that happens to have the SUID bit set and belongs to the root user. In this case, that binary is `/usr/bin/passwd`. Normally, a nonroot user wouldn’t be able to overwrite the file. However, because of the Dirty COW vulnerability, you achieve privilege escalation because you can write arbitrary contents to the file while preserving the file permissions.

**Go**

Go version of the Dirty COW Race Condition Privilege Escalation

```sh
alice@ubuntu $ go run dirty.go

# DirtyCow root privilege escalation
# Backing up /usr/bin/passwd.. to /tmp/bak
# Size of binary: 47032
# Racing, this may take a while...
# /usr/bin/passwd is overwritten
# Popping root shell
# procselfmem done
# Do not forget to restore /tmp/bak

root@ubuntu:/home/alice $ id
uid=0(root) gid=1000(alice) groups=0(root),4(adm),1000(alice)
```
