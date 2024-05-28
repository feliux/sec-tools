# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

PING_FILE = "ping_results.txt"

for ip in range(1, 255):
	ipAddress = "192.168.1." + str(ip)
	print("Pinging %s " %(ipAddress))
	subprocess = Popen(["/bin/ping", "-c 1 ", ipAddress], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr= subprocess.communicate(input=None)
	if "bytes from " in stdout.decode("utf-8"):
		print("The Ip Address %s has responded with a ECHO_REPLY!" %(stdout.decode("utf-8").split()[1]))
		with open(f"{PING_FILE}", "a") as myfile:
			print(f"Writing ping result to {PING_FILE}")
			myfile.write(stdout.decode("utf-8").split()[1] + "\n")
