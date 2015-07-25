#!/usr/bin/env python
#CGI Scans a site and posts OK Responses to the channel...
#Args: !cgibot <site>

#d3hydr8[at]gmail[dot]com
#www.darkc0de.com

import sys, socket, string, httplib, time

OK_RESP = [200, 202]

if len(sys.argv) != 6:
	print "Usage: ./cgibot.py <host> <port> <nick> <channel> <path_list>"
	sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]
CHAN = sys.argv[4]
readbuffer = ""

try:
	paths = open(sys.argv[5], "r").readlines()
except(IOError): 
 	print "\n[-] Error: Check your path_list location.\n" 
	print "[-] (http://www.darkc0de.com/scanners/bins.txt)\n"
	sys.exit(1)

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (NICK, NICK, NICK))
s.send("JOIN :%s\r\n" % CHAN)

print "[+] CGI-Bot Loaded"
s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] CGI-Bot Loaded"))	
print "[+] Loaded:", len(paths), "paths"
s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Loaded: ", len(paths), " paths"))
print "[+] Loaded:", len(OK_RESP), "responses"
s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Loaded: ", len(OK_RESP), " responses"))

def servgrab(host, path):
	print "Trying:", path
	h = httplib.HTTP(host)
	h.putrequest("HEAD", path)
	h.putheader("Host", host)
	h.endheaders()
	status, reason, headers = h.getreply()
	return status, reason, headers.get("Server")

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		socket.setdefaulttimeout(5)
		#print line
		try:
			if line[3] == ":!"+NICK:
				host = line[4].replace("http://","").rsplit("/",1)[0]
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Scanning: ", host))
				for path in paths:
					path = path.replace("\n","")
					if path[0] != "/":
						path = path+"/"
					try:
						resp, reason, headers = servgrab(host, path)
						if resp in OK_RESP:
							output = "[+] Found: "+str(resp)+" "+reason+" "+host+path
							s.send("PRIVMSG %s :%s\r\n" % (CHAN, output))	
					except(socket.gaierror, socket.timeout, socket.error), msg:
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[-] Error: ",msg))			
		except(IndexError):
			pass
        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
