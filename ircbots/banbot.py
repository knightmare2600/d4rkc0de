#!/usr/bin/env python
#Prints banner.
#Args: !banbot <host> <port>

import sys, socket, string, hashlib, time

if len(sys.argv) != 5:
	print "Usage: ./banbot.py <host> <port> <nick> <channel>"
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

def bangrab(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(15)
		s.connect((host, port))
		time.sleep(4)
		s.send("\r\n")
		response = s.recvfrom(1024)[0]
		s.close()
	except (socket.error):
		s.close()
	try:
		return response
	except(UnboundLocalError): 
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
				response = bangrab(line[4], int(line[5]))
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Banner: ",response))				
		except(IndexError):
			pass

        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
