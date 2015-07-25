#!/usr/bin/env python
#SPammer Bot
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com


import sys, socket, os, string, re, time, sets

def sender(chan):
	if chan != "#":
		time.sleep(5)  #Time to wait till join
		print "\n[+] Joining:",chan
		s.send("JOIN :%s\r\n" % chan)
		time.sleep(10)  #Time to wait till sending message
		print "[!] Sending MSG:",sys.argv[4]
		s.send("PRIVMSG %s :%s\r\n" % (chan, sys.argv[4] ))
		#print "[!] Sending MSG:",sys.argv[4]          ///Send second message
		#s.send("PRIVMSG %s :%s\r\n" % (chan, sys.argv[4] ))

if len(sys.argv) != 5:
	print "Usage: ./spambot.py <host> <port> <nick> <message>"
	sys.exit(1)
	
print "\n\t   d3hydr8[at]gmail[dot]com SpamBot v1.0"
print "\t-------------------------------------------\n"

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]
readbuffer = ""
chans = []

print "\n[+] Connecting:",HOST+":"+str(PORT)
s=socket.socket( )
s.connect((HOST, PORT))
print "[+] Authenticating:",NICK
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (NICK, NICK, NICK))
time.sleep(10)
print "[+] Collecting Channels"
s.send("LIST \r\n")
time.sleep(120) #waiting 2 min to collect list
readbuffer=readbuffer+s.recv(8192)
for line in readbuffer:
	rooms = re.findall("#[\w\.\-/]*", readbuffer)
	if len(rooms) >=1:
		for room in rooms:
			if room != "#":
				chans.append(room)
chans = list(sets.Set(chans))
print "[+] Found Channels:",len(chans)
for chan in chans:
	sender(chan)
s.send("QUIT \r\n")
s.close()
			

	
