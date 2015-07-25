#!/usr/bin/env python
#Tests proxy and prints output to channel.
#Args: !proxybot <ip> <port>

#www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, string, time, urllib, httplib, socket

if len(sys.argv) != 5:
	print "Usage: ./proxybot.py <host> <port> <nick> <channel>"
	sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]
CHAN = sys.argv[4]
readbuffer = ""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (NICK, NICK, NICK))
s.send("JOIN :%s\r\n" % CHAN)

def proxtest(proxy):
	socket.setdefaulttimeout(5) #Set proxy timeout here
	proxies = {'http': "http://"+proxy}
	opener = urllib.FancyURLopener(proxies)
	opener.open("http://www.google.com")

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		try:
			if line[3] == ":!"+NICK:
				proxy = line[4].replace("http://","")+":"+line[5]
				print "[+] Testing:",proxy
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Testing: ",proxy))
				try:
					proxtest(proxy)
					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Alive: ",proxy))	
				except(IOError, socket.gaierror, socket.timeout, socket.error, httplib.InvalidURL), msg:
					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[-] Dead: ",msg))			
		except(IndexError):
			pass

        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
