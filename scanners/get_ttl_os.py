import re
import sys
import subprocess

if len(sys.argv) != 2:
    print("[!] Usage: python3" + sys.argv[0] + " <targetIP>\n")
    sys.exit(1)


def get_ttl(ip):
    proc = subprocess.Popen(
        [f"/usr/bin/ping -c 1 {ip}", ""],
        stdout=subprocess.PIPE,
        shell=True
    )
    out, err = proc.communicate()
    out = out.split()
    out = out[12].decode("utf-8")
    ttl_value = re.findall(r"\d{1,3}", out)[0]
    return ttl_value


def get_os(ttl_value):
    ttl_value = int(ttl_value)
    if ttl_value == 0 and ttl_value <= 64:
        return "Linux"
    elif ttl_value >= 65 and ttl_value <= 128:
        return "Windows"
    else:
        return "Not OS found"


if __name__ == "__main__":
    ip = sys.argv[1]
    ttl = get_ttl(ip)
    os_name = get_os(ttl)
    print(f"\n{ip} ttl -> {ttl}: {os_name}")
