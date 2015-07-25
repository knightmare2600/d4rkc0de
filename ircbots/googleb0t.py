#!/usr/bin/env python
#Googlebot, will print the first 3 sites found my google.
#args:
#      !googbot <query>
#
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, socket, string, urllib2, re

if len(sys.argv) != 5:
	print "Usage: ./googlebot.py <host> <port> <nick> <channel>"
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

def StripTags(text):
	finished = 0
	while not finished:
		finished  =1
		start =  text.find("<")
		if start >= 0:
			stop = text[start:].find(">")
			if stop >= 0:
				text = text[:start] + text[start+stop+1:]
				finished = 0
	return text

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		try:
			if line[3] == ":!"+NICK:
				query = line[4:]
				query = " ".join(query)
				query = re.sub("\s","%20",query)
				results_web = 'http://www.google.com/search?hl=en&q='+line[4]+'&hl=en&lr=&start=20&sa=N'
				request_web = urllib2.Request(results_web)
				request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
				opener_web = urllib2.build_opener()                           
        			text = opener_web.open(request_web).read()
				hit = re.findall(('\w+\.\w+.\w+\.\w+'),StripTags(text))
				if len(hit) >=3:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "Searching Google:"))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "\thttp://"+hit[6]))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "\thttp://"+hit[7]))
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "\thttp://"+hit[8]))
				
		except(IndexError):
			pass
		if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
