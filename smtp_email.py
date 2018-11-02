#!/usr/bin/python

import sys
import smtplib
import dns.resolver
from socket import error

def smtp(sender, rcpt, server, subject, body):
    msg = 'From: {}\nTo:{}\nSubject: {}\n{}'.format(sender, rcpt, subject, body)
    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.sendmail(sender, rcpt, message)
    except error:
        print 'Send failed'
    except smtplib.SMTPException:
        print 'Send failed'
    else:
        print 'Successfully sent email for %s.' % bg


def main():
    args = sys.argv[1:]
    email_addr = raw_input('Enter email addresses seperated by commas: ')
    search = re.search(r'.+@(.+)', email_addr)
    domain = search.group(1)
    #email_addr_list = email_addr.split(',')
    email_sender = args[1]
    email_sub = args[3]
    email_body = args[5]
    
    answers = dns.resolver.query(domain, 'MX')
    mx_list = []
    for rdata in answers:
        mx_list.append(x)
    mx = mx_list[0]

    smtp(email_sender, email_addr, mx, email_sub, email_body)


if __name__ == '__main__':
  main()



