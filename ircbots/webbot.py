#!/usr/bin/env python
#Prints the webserver using...
#Args: !webbot <host> <port>
#d3hydr8[at]gmail[dot]com

import sys, socket, string, httplib, time

if len(sys.argv) != 5:
	print "Usage: ./webbot.py <host> <port> <nick> <channel>"
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

def servgrab(host, port):
	host = host.replace("http://","")
	try:# make a http HEAD request
		h = httplib.HTTP(host)
		h.putrequest("HEAD", "/")
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
		return status, reason, headers.get("Server")
	except(UnboundLocalError, socket.timeout, socket.error): 
		print "\tTimeout Error: Slow"
		pass

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		print line
		try:
			if line[3] == ":!"+NICK:
				try:
					status, reason, headers = servgrab(line[4], int(line[5]))
					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Server: ",headers))	
				except(socket.gaierror, socket.timeout, socket.error), msg:
					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Error: ",msg))			
		except(IndexError):
			pass

        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
