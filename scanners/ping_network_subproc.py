# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

for ip in range(1, 255):
	ipAddress = "192.168.1." + str(ip)
	print("Pinging %s " %(ipAddress))
	subprocess = Popen(["/bin/ping", "-c 1 ", ipAddress], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr= subprocess.communicate(input=None)
	if "bytes from " in stdout.decode("utf-8"):
		print("The Ip Address %s has responded with a ECHO_REPLY!" %(stdout.decode("utf-8").split()[1]))
		with open("ips.txt", "a") as myfile:
			myfile.write(stdout.decode("utf-8").split()[1] + "\n")
