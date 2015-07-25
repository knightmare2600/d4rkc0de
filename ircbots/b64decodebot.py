#!/usr/bin/env python
#Base64 decoder
#Args: !b64decodebot <string to be encoded>
#d3hydr8[at]gmail[dot]com

import sys, socket, string, base64

if len(sys.argv) != 5:
	print "Usage: ./b64decodebot.py <host> <port> <nick> <channel>"
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

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
		print line
        	line=string.rstrip(line)
        	line=string.split(line)
		try:
			if line[3] == ":!b64decodebot":
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "b64decoded: ", base64.b64decode(line[4])))
		except(IndexError):
			pass
		
        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
