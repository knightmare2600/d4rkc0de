#!/usr/bin/env python
#Cracks md5 using wordlist, also can add words to the list from channel
#generate md5s and can check wordlist length.

#Args: 
#!crack <password>
#!insert <word>
#!md5 <word>
#!length 

import sys, socket, string, md5

def load_words():
	try:
  		words = open(wordlist, "r").readlines()
	except(IOError): 
  		print "[!] Error: Check your wordlist path\n"
  		sys.exit(1)
	global words

def crack(pw):
	output = ""
	for word in words:
		hash = md5.new(word.replace("\n","")).hexdigest()
		if pw == hash: 
			output = word.replace("\n","")
	return output
		
def insert(word):
	add_list = open(wordlist, "a")
	if word not in words:
		add_list.writelines(word.replace("\n","")+"\n")
		add_list.close()
		load_words()
		return len(words)
	else:
		add_list.close()
		return "[-] word already present"

	words.close()
	

#Fill in the information below
#---------------------------------------
HOST = "irc.milw0rm.com"
PORT = "6667"
NICK = "crackb0t"
CHAN = "#darkc0de"
wordlist = "/home/d3hydr8/words.txt"
#---------------------------------------

print "\n\t   d3hydr8[at]gmail[dot]com CrackB0t v1.1"
print "\t-----------------------------------------------"

print "[+] CrackB0t Loaded"

load_words()
  
print "[+] Words Loaded:",len(words)

readbuffer = ""

s=socket.socket( )
s.connect((HOST, int(PORT)))
print "[+] Connected:",HOST+":"+PORT
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (NICK, NICK, NICK))
s.send("JOIN :%s\r\n" % CHAN)
print "[+] Joined:",CHAN,"\n"
s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[++] CrackB0t Loaded"))
s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Wordlist Length:",len(words)))

while 1:
	readbuffer=readbuffer+s.recv(1024)
    	temp=string.split(readbuffer, "\n")
    	readbuffer=temp.pop( )

    	for line in temp:
        	line=string.rstrip(line)
        	line=string.split(line)
		try:
			line[3] = line[3].lower()
			
			if line[3] == ":!crack":
				if len(line[4]) != 32:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] improper length"))
				else:
					output = crack(line[4])
					print "[+] Cracking:",line[4]
					print "[+] Output:",output
					if output != "":
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] cracked: ",output))
					else:
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] "+line[4]+" : Not Found"))
					
			if line[3] == ":!insert":
				if len(line[4]) <= 15:
					output = insert(line[4]+"\n")
					if output != "[-] word already present":
						print "[+] Insert:",line[4]
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] insert: ",line[4]))
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] new length: ",output))
					else:
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, output))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] word length to long"))
					s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[-] length:", len(line[4])))
			
			if line[3] == ":!md5":
				hash = md5.new(" ".join(line[4:])).hexdigest()
				print "[+]"," ".join(line[4:]),"==",hash
				s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "[+] "," ".join(line[4:])," == ",hash))
				
			if line[3] == ":!length":
				print "[+] Length:",len(words)
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] wordlist length:",len(words)))
					
			if line[3] == ":!help":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "crackB0t options:"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !crack <md5> | crack md5's"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !insert <word> | insert word into list"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !md5 <word> | generate md5"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !length | check wordlist length"))
				
				
		except(IndexError):
			pass
		
        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])
