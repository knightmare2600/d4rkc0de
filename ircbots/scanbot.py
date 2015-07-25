#!/usr/bin/env python
#Randomly scans for servers using nmap and prints ip/server/port to channel.

#Run as root or change your nmap -sS flag

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, socket, string, time, commands, getopt, StringIO, re, os

if len(sys.argv) != 5:
	print "Usage: ./scanbot.py <host> <port> <nick> <channel>"
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

def servtest(ip, port):
	
	server = ""
	try:
		import httplib
		h = httplib.HTTP(ip+":"+str(port))
		h.putrequest("HEAD", "/")
		h.putheader("Host", ip)
		h.endheaders()
		status, reason, headers = h.getreply()
		server = headers.get("Server")
	except: pass
	
	if server != None and server != "":
		return server

def scan():
	
	resps = {}
	plist = [21,23,22,25,80,110,143]

	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -sS -iR 1 -p 21,23,22,25,80,110,143')[1]).readlines()

	for tmp in nmap:
		ip = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ip: ipaddr = ip[0]
			
	for tmp in nmap:
		for port in plist:
			if re.search(str(port)+"/tcp\s+(?=open)", tmp):
				port = int(port)
				if port == 80 or port == 143:
					server = servtest(ipaddr, port)
					resps[server] = port
				else:
					try:
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.settimeout(15)
						s.connect((ipaddr, port))
						time.sleep(4)
						s.send("\r\n")
						response = s.recvfrom(1024)[0]
						if response != "":
							resps[response] = port
						s.close()
					except(socket.error):
						s.close()
						pass
		
	if len(resps) >=1:
		return ipaddr, resps


pid = os.fork()
if pid:
	while 1:
		time.sleep(20)
		try:
			ipaddr, resps = scan()
			if len(resps) >=1:
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[ Found ]: ",ipaddr))
				for resp,port in resps.items():
					print resp, port
					if resp != None and resp != "":
						s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "Port:",port," Running: ",resp))
		except(TypeError):
			pass

else:
	while 1:
		readbuffer=readbuffer+s.recv(1024)
    		temp=string.split(readbuffer, "\n")
    		readbuffer=temp.pop( )

    		for line in temp:
			print line
        		line=string.rstrip(line)
        		line=string.split(line)		
	
        		if(line[0]=="PING"):
          			s.send("PONG %s\r\n" % line[1])
