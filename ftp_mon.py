#!/usr/bin/python

import socket
import re
import sys
import smtplib
import dns.resolver
from socket import error
import time

address = '54.225.231.149'
port = 21
sender = 'alerts@sizmek.com'
rcpt = 'vineet.bhatia@sizmek.com'
subject = 'ftp connection failed on aws host 54.225.231.149'
body = 'ftp connection failed on aws host 54.225.231.149!!'

def smtp(sender, rcpt, subject, body, server):
    msg = 'From: %s\nTo: %s\nSubject: %s\n%s' % (sender, rcpt, subject, body)
    print msg
    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.sendmail(sender, rcpt, msg)
    except error:
        print 'Send failed'
    except smtplib.SMTPException:
        print 'Send failed'
    else:
        print 'Successfully sent email'

# 3 attempts before considering failure
attempts = 0
while attempts < 3:
    try:
        print 'Attempting to connect to %s on port %s' % (address, port)
        s = socket.socket()
        s.settimeout(5)
        s.connect((address, port))
        print "Connected to %s on port %s" % (address, port)
        s.close()
        break
    except socket.error, e:
        attempts += 1
        continue
else:
    print "Connection to %s on port %s failed 3 times!!: %s" % (address, port, e)
    search = re.search(r'.+@(.+)', rcpt)
    domain = search.group(1)
    answers = dns.resolver.query(domain, 'MX')
    mx_list = []
    for rdata in answers:
        mx_list.append(rdata)
    s = str(mx_list[1])
    my_list = s.split(' ')
    server = my_list[1]
    smtp(sender, rcpt, subject, body, server)
