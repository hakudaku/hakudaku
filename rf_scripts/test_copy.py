#!/Users/vineetbhatia/ENV/bin/python -tt
import sys
import re
import os

def out(host, host_yml_path, my_regex, enforcer_path):
  service = {} 
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
    service['a'] = x
  print service
  for key in service.keys():
    print service[key]
  
  f = open(enforcer_path, 'r')
  for key in service.keys():
    my_class_reg = r'^.+\("%s"\).+?include\s+(.+?)}' % service[key] 
    class_match = re.findall(my_class_reg, f.read(), re.DOTALL)
    print 'Service %s belongs to below classes:' % service[key]
    for c in class_match:
      print c 
    #print class_match
    
def main():
  args = sys.argv[1:]
  host = args[0]
  host_yml_path = '/Users/vbhatia/git_repos/operations/puppet/modules/puppet/files/hostinfo/hosts.yaml'
  enforcer_path = '/Users/vbhatia/git_repos/operations/puppet/modules/truth/manifests/enforcer.pp'
  my_regex = r'(%s).*?services:(.*?)memory' % host
  out(host, host_yml_path, my_regex, enforcer_path)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
