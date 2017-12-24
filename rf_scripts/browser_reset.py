#!/Users/vbhatia/ENV/bin/python -tt
import sys
from pssh import ParallelSSHClient
import paramiko, base64
import logging
from socket import gethostbyname, gaierror, timeout

def ssh_parallel(ips, cmds):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(ips, user='groundcontrol', password='SSME')
  for cmd in cmds:
    output = client.run_command(cmd, stop_on_errors=False)
    for host in output:
      if output[host]['exception'] != None:
        print '***********Check Host %s. It is either down, invalid, or authentication failed*************\n' % (host)

def ssh_serial(ip, cmd):
  failed_hosts = []
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(ip, username='groundcontrol', password='SSME', timeout=5)
  stdin, stdout, stderr = client.exec_command(cmd)
  for line in stdout:
    print line.strip('\n')
  for line in stderr:
    print line.strip('\n')
  print '\r'
  client.close()

def main():
  args = sys.argv[1:]
  usage = ('browser_reset.py [screen #]\n'
           'Example: browser_reset.py one')
  if not args or len(args) < 1:
    print usage
    sys.exit(1)
  cmd = 'pkill -a -i "Google Chrome";sleep 5;open -a Google\ Chrome --args --kiosk'
  cmds = ['pkill -a -i "Google Chrome"', 'sleep 5', 'open -a Google\ Chrome --args --kiosk']
  
  #####screen --> ip assignment###
  ip = None 
  ips = ['10.20.14.29', '10.20.14.30', '10.20.14.31', '10.20.14.32', '10.20.14.33', '10.20.14.34', '10.20.14.35', '10.20.14.36', '10.20.14.37', '10.20.14.38']
  if args[0] == '1':
    ip = ips[0]
  elif args[0] == '2':
    ip = ips[1]
  elif args[0] == '3':
    ip = ips[2] 
  elif args[0] == '4':
    ip = ips[3]
  elif args[0] == '5':
    ip = ips[4] 
  elif args[0] == '6':
    ip = ips[5] 
  elif args[0] == '7':
    ip = ips[6] 
  elif args[0] == '8':
    ip = ips[7]
  elif args[0] == '9':
    ip = ips[8] 
  elif args[0] == '10':
    ip = ips[9] 
  elif args[0] == 'all':
    ssh_parallel(ips, cmds)
  else:
    print usage
    sys.exit(1) 
  
  if ip != None:
    ssh_serial(ip, cmd)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
