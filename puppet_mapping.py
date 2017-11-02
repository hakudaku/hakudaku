#!/Users/vbhatia/ENV/bin/python -tt
import sys
import re
import os
from collections import defaultdict
import commands

def out(host, host_yml_path, my_regex, enforcer_path, puppet_search_module_path):
  service = defaultdict(list) 
  f = open(os.path.abspath(host_yml_path), 'r')
  match = re.findall(my_regex, f.read(), re.DOTALL)
  f.close()
  f = open('tmp.txt', 'w')
  for t in match:
    f.write(' '.join(str(s) for s in t) + '\n') # For each tuple in the list, you convert all of its elements into strings, join them by spaces to form the string, and write the string with a new line to the file. Then you close the file.
  f.close()  

  f = open('tmp.txt', 'r')
  service_match = re.findall(r'\s+-\s+(\S+)', f.read())
  print '%s has below services assigned in puppet:' % host
  for x in service_match:
    service['a'].append(x)
  for k, dk in service.iteritems():
    for x in dk:
      print x 
  
  for k, dk in service.iteritems():
    for x in dk:
      f = open(enforcer_path, 'r')
      my_class_reg = r'^.+\("%s"\).+?include\s+(.+?)\n' % x
      class_match = re.findall(my_class_reg, f.read(), re.DOTALL)
      print '\nService %s belongs to below classes:' % x
      for c in class_match:
        cmd = 'grep -R %s %s* | grep class' % (c, puppet_search_module_path)
        print c
        print '\nPuppet manifest file where %s is defined:' % c
        output = commands.getoutput(cmd)
        match = re.search(r'^(.+):class', output)
        print match.group(1)
    
def main():
  args = sys.argv[1:]
  usage = ('puppet_mapping.py [host]\n'
           'Example: puppet_mapping.py lsv-1484')
  if not args or len(args) < 1:
    print usage
    sys.exit(1)
  host = args[0]
  host_yml_path = os.path.expanduser('~') + '/git_repos/operations/puppet/modules/puppet/files/hostinfo/hosts.yaml'
  enforcer_path = os.path.expanduser('~') + '/git_repos/operations/puppet/modules/truth/manifests/enforcer.pp'
  puppet_search_module_path = os.path.expanduser('~') + '/git_repos/operations/puppet/modules/'
  my_regex = r'(%s).*?services:(.*?)memory' % host
  out(host, host_yml_path, my_regex, enforcer_path, puppet_search_module_path)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
