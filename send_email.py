#!/usr/bin/python -tt

import smtplib
import re
import sys
import commands
from socket import error 

def smtp(header, port, sender, rcpt, server, bg):
  
  message = 'From: %s\nTo:%s\nSubject: SMTP e-mail test\n%s\n\nThis is a test e-mail message.' % (sender, rcpt, header)
  try: 
    smtpObj = smtplib.SMTP(server, port)
    smtpObj.sendmail(sender, rcpt, message)
  except error: 
    print 'Send failed for %s. Connection failed.' % bg
  except smtplib.SMTPException:
    print 'Send failed for %s. Error occurred.' % bg
  else:
    print 'Successfully sent email for %s.' % bg

def main():
  args = sys.argv[1:]
  if not args:
    print 'Usage: send_email.py --dub|--snc'
    sys.exit(1)
  for a in args:
    if a == '--snc':
      status, output = commands.getstatusoutput('hostname -f')
      while 'snc' in output: 
        rcpt = raw_input('Recipient addr: ')
        match = re.search(r'\S+@\S+\.\w+', rcpt)
        if not match: # rcpt addr not valid email address syntax
          print 'RCPT addr is not valid syntax!'
          continue # Continue to Prompt user for a valid rcpt input
        match = re.search(r'\S+@(\S+)', rcpt)
        domain = match.group(1)
        dig_cmd = 'dig mx %s +short' % domain
        status, mx = commands.getstatusoutput(dig_cmd)
        if not mx:
          print 'No MX record exists for domain %s. Please enter a valid domain.' % (domain)
          continue # Continue to Prompt user for a valid email addr 
        else:
          break # Break the loop and continue with the rest of code
      else:
        print 'This is not a snc host!'
        sys.exit(1)
    
    elif a == '--dub':
      status, output = commands.getstatusoutput("hostname -f")
      while 'dub' in output:
        rcpt = raw_input('Recipient addr: ')
        match = re.search(r'\S+@\S+\.\w+', rcpt)
        if not match: # rcpt addr not valid email address syntax
          print 'RCPT addr is not valid syntax!'
          continue # Continue to Prompt user for a valid rcpt input 
        match = re.search(r'\S+@(\S+)', rcpt)
        domain = match.group(1)
        dig_cmd = 'dig mx %s +short' % domain
        status, mx = commands.getstatusoutput(dig_cmd)
        if not mx:
          print 'No MX record exists for domain %s. Please enter a valid domain.' % (domain)
          continue # Continue to Prompt user for a valid email addr 
        else:
          break # Break the loop and continue with the rest of code
      else:
        print 'This is not a dub host!'
        sys.exit(1)
    else:
      print 'Usage: send_email.py --dub|--snc'
      sys.exit(1)
  
  snc_header_port_map = {}
  snc_header_port_map['x-virtual-mta: mx_commercial'] = [40132, 'noreply@r.grouponmail.com.mx', 'mx_commercial']
  snc_header_port_map['x-virtual-mta: co_commercial'] = [40130, 'noreply@r.grouponmail.com.co', 'co_commercial']
  snc_header_port_map['x-virtual-mta: cl_commercial'] = [40129, 'noreply@r.grouponmail.cl', 'cl_commercial'] 
  snc_header_port_map['x-virtual-mta: pe_commercial'] = [40131, 'noreply@r.grouponmail.com.pe', 'pe_commercial']
  snc_header_port_map['x-virtual-mta: transactional'] = [40121, 'noreply@r.groupon.com', 'transactional']
  snc_header_port_map['x-virtual-mta: unclean'] = [40122, 'noreply@r.groupon.com', 'unclean']
  snc_header_port_map['x-virtual-mta: ls_commercial'] = [40139, 'noreply@r.groupon.com', 'ls_commercial']
  snc_header_port_map['x-virtual-mta: ls_unclean'] = [40141, 'noreply@r.groupon.com', 'ls_unclean']
  snc_header_port_map['x-virtual-mta: ls_transactional'] = [40140, 'noreply@r.groupon.com', 'ls_transactional']

  dub_header_port_map = {}
  dub_header_port_map['x-virtual-mta: my_commercial'] = [40112, 'noreply@r.grouponmail.my', 'my_commercial']
  dub_header_port_map['x-virtual-mta: br_commercial'] = [40102, 'noreply@r.grouponmail.com.br', 'br_commercial']
  dub_header_port_map['x-virtual-mta: be_commercial'] = [40111, 'noreply@r.grouponmail.be', 'be_commercial']
  dub_header_port_map['x-virtual-mta: jp_commercial'] = [40136, 'noreply@r.grouponmail.jp', 'jp_commercial']
  dub_header_port_map['x-virtual-mta: au_commercial'] = [40110, 'noreply@r.grouponmail.com.au', 'au_commercial']
  dub_header_port_map['x-virtual-mta: ar_commercial'] = [40119, 'noreply@r.grouponmail.com.ar', 'ar_commercial']
  dub_header_port_map['x-virtual-mta: ae_commercial'] = [40113, 'noreply@r.grouponmail.ae', 'ae_commercial']
  dub_header_port_map['x-virtual-mta: de_commercial'] = [40116, 'noreply@r.grouponmail.de', 'de_commercial']
  dub_header_port_map['x-virtual-mta: sg_commercial'] = [40114, 'noreply@r.grouponmail.sg', 'sg_commercial']
  dub_header_port_map['x-virtual-mta: it_commercial'] = [40104, 'noreply@r.grouponmail.it', 'it_commercial']
  dub_header_port_map['x-virtual-mta: il_commercial'] = [40113, 'noreply@r.grouponmail.co.il', 'il_commercial']
  dub_header_port_map['x-virtual-mta: ie_commercial'] = [40120, 'noreply@r.grouponmail.ie', 'ie_commercial']
  dub_header_port_map['x-virtual-mta: fr_commercial'] = [40103, 'noreply@r.grouponmail.fr', 'fr_commercial']
  dub_header_port_map['x-virtual-mta: nz_commercial'] = [40114, 'noreply@r.grouponmail.co.nz', 'nz_commercial']
  dub_header_port_map['x-virtual-mta: nl_commercial'] = [40106, 'noreply@r.grouponmail.nl', 'nl_commercial']
  dub_header_port_map['x-virtual-mta: ca_commercial'] = [40123, 'noreply@r.grouponmail.ca', 'ca_commercial']
  dub_header_port_map['x-virtual-mta: uk_commercial'] = [40101, 'noreply@r.grouponmail.co.uk', 'uk_commercial']
  dub_header_port_map['x-virtual-mta: hk_commercial'] = [40117, 'noreply@r.grouponmail.hk', 'hk_commercial']
  dub_header_port_map['x-virtual-mta: pl_commercial'] = [40107, 'noreply@r.grouponmail.pl', 'pl_commercial']
  dub_header_port_map['x-virtual-mta: es_commercial'] = [40105, 'noreply@r.grouponmail.es', 'es_commercial']
  dub_header_port_map['x-virtual-mta: transactional2'] = [40125, 'noreply@r.groupon.com', 'transactional2']
  dub_header_port_map['x-virtual-mta: transactional1'] = [40124, 'noreply@r.groupon.com', 'transactional1']
  dub_header_port_map['x-virtual-mta: transactional'] = [40121, 'noreply@r.groupon.com', 'transactional']
  dub_header_port_map['x-virtual-mta: doi'] = [40126, 'noreply@r.groupon.com', 'doi']
  dub_header_port_map['x-virtual-mta: unclean'] = [40122, 'noreply@r.groupon.com', 'unclean']
  dub_header_port_map['x-virtual-mta: welcome'] = [40127, 'noreply@r.groupon.com', 'welcome']
  
  if '--snc' in args:
    for key in snc_header_port_map.keys():
      smtp(key, snc_header_port_map[key][0], snc_header_port_map[key][1], rcpt, 'localhost', snc_header_port_map[key][2]) 
  elif '--dub' in args:
    for key in sorted(dub_header_port_map.keys()):
      smtp(key, dub_header_port_map[key][0], dub_header_port_map[key][1], rcpt, 'localhost', dub_header_port_map[key][2])


if __name__ == '__main__':
  main()
