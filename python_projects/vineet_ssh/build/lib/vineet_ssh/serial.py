import paramiko, base64
from socket import gethostbyname, gaierror

def ssh_serial(host, cmd):
  failed_hosts = []
  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host)
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
      print line.strip('\n')
    for line in stderr:
      print line.strip('\n')
    print '\n'
    client.close()
  except gaierror:
    print '***********Check Host %s. It is either down, invalid, or authentication failed*************\n' % (host)
