import paramiko

PARAMIKO_LOG = "paramiko.log"
SS_PRIVATE_KEY = "/home/user/.ssh/id_rsa"
HOST = "127.0.0.1"
USERNAME = "user"
PASSWORD = "changeme"

paramiko.util.log_to_file(PARAMIKO_LOG)
client = paramiko.SSHClient()
rsa_key = paramiko.RSAKey.from_private_key_file(SS_PRIVATE_KEY, password=PASSWORD)
#client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, pkey=rsa_key, username=USERNAME, password=PASSWORD)
stdin, stdout, stderr = client.exec_command("uname -a; id")
for line in stdout.readlines():
	print(line)
client.close()
