import paramiko
from paramiko import RSAKey

PARAMIKO_LOG = "paramiko.log"
SS_PRIVATE_KEY = "/home/user/.ssh/id_rsa"
HOST = "127.0.0.1"
USERNAME = "user"
PASSWORD = "changeme"

client = paramiko.SSHClient()

try:
	paramiko.util.log_to_file(PARAMIKO_LOG)
	rsa_key = paramiko.RSAKey.from_private_key_file(SS_PRIVATE_KEY, password=PASSWORD)
	#client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(HOST, pkey=rsa_key, username=USERNAME, password=PASSWORD)
	sftp = client.open_sftp()
	dirlist = sftp.listdir(".")
	for directory in dirlist:
		print(directory)
	try:
		sftp.mkdir("demo")
	except IOError:
		print("IOError, the file already exists!")
		sftp.rmdir("demo")
		sftp.mkdir("demo")		
		print("Directory recreated.")
	client.close()
except Exception, e:
	print("Exception: ", str(e))
	try:
		client.close()
	except:
		pass
