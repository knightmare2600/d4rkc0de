#!/usr/bin/env python
#Will print md5,email or both to channel from link.
#Args: !dumpbot <option> <link>
#Args: !dumpbot help
#Options:
#	md5
#	email
#	both

import sys, socket, string, urllib, time, re, httplib

#How many lines to print in channel.
OUTPUT = 5

if len(sys.argv) != 5:
	print "Usage: ./dumpbot.py <host> <port> <nick> <channel>"
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

def getmd5s(site):
	md5s = {}
	num = 1
	for line in site:
		try:
			MD5 = re.findall("[a-f0-9]"*32,line)[0]
			md5s[MD5] = num
		except(IndexError):
			pass
		num +=1
	if len(md5s) >= 1:
		md5s = md5s.items()
		return md5s
	else:
		return None
			
		
def emails(site):
	emails = re.findall('\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}', str("".join(site)))
	if len(emails) != 0:
		return emails
	else:
		print None
		
def getsource(site):
	if site[:7] != "http://":
		site = "http://"+site
	try:
		site = urllib.urlopen(site).readlines()
		return site
	except(httplib.InvalidURL):
		site = []
		return site

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		#print line
		try:
			if line[3] == ":!"+NICK and line[4].lower() == "md5":
				response = getmd5s(getsource(line[5]))
				if response != None:
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Found:",len(response)," md5s"))
					for line in response[:OUTPUT]:
						s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "MD5: ",line[0]," Line: ",line[1]))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "No MD5's Found"))
					
			if line[3] == ":!"+NICK and line[4].lower() == "email":
				response = emails(getsource(line[5]))
				if response != None:
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Found:",len(response)," emails"))
					for e in response[:OUTPUT]:
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Email: ",e))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "No Emails Found"))
			
			if line[3] == ":!"+NICK and line[4].lower() == "both":
				site = getsource(line[5])
				md5s = getmd5s(site)
				email = emails(site)
				if md5s != None:
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Found:",len(md5s)," md5s"))
					for line in md5s[:OUTPUT]:
						s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "MD5: ",line[0]," Line: ",line[1]))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "No MD5's Found"))
				if email != None:
					s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Found:",len(email)," emails"))
					for e in email[:OUTPUT]:
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "Email: ",e))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "No Emails Found"))
			
			if line[3] == ":!"+NICK and line[4].lower() == "help":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[ "+NICK+" md5 <site>    #Collects MD5's ]"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[ "+NICK+" email <site>    #Collects Emails ]"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[ "+NICK+" both <site>    #Collects both ]"))
				
		except(IndexError):
			pass

        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
