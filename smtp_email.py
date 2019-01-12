#!/Users/vineetbhatia/ENV/bin/python -tt

import sys
import smtplib
import dns.resolver
from socket import error
import re

def smtp(sender, rcpt, server, subject, body):
    print server
    msg = 'From: {}\nTo:{}\nSubject: {}\n{}'.format(sender, rcpt, subject, body)
    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.sendmail(sender, rcpt, msg)
    except error:
        print 'send failed' 
    except smtplib.SMTPException as e:
        print str(e) 
    else:
        print 'Successfully sent email' 


def main():
    args = sys.argv[1:]
    email_addr = raw_input('Enter email addresses seperated by commas: ')
    email_sender = raw_input('Enter sender: ')
    email_sub = raw_input('Enter subject: ') 
    email_body = raw_input('Enter body: ') 

    search = re.search(r'.+@(.+)', email_addr)
    domain = search.group(1)
    #email_addr_list = email_addr.split(',')
    answers = dns.resolver.query(domain, 'MX')
    mx_list = []
    for rdata in answers:
        mx_list.append(rdata)
    mx = str(mx_list[0])
    mx_list = mx.split(' ') 
    mx = mx_list[1] 
    

    smtp(email_sender, email_addr, mx, email_sub, email_body)


if __name__ == '__main__':
  main()



