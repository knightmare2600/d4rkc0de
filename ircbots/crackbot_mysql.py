#!/usr/bin/env python
#Cracks mysql hash using wordlist, also can add words to the list from channel
#generate hashes and can check wordlist length.

#Fill in the information below
#---------------------------------------
HOST = "irc1.netgarage.org"
PORT = "6667"
NICK = "crackb0t_mysql"
CHAN = "#darkc0de"
wordlist = "/home/d3hydr8/words.txt"
#---------------------------------------

#Args: 
#!crack <hash>
#!insert <word>
#!hash <word>
#!length 

import sys, socket, string, hashlib, re

def load_words():
	try:
  		words = open(wordlist, "r").readlines()
	except(IOError): 
  		print "[!] Error: Check your wordlist path\n"
  		sys.exit(1)
	global words

def mysql323(clear): 
    # Taken almost verbatim from mysql's source 
    nr = 1345345333 
    add = 7 
    nr2 = 0x12345671 
    retval = "" 
    for c in clear: 
	if c == ' ' or c == '\t': 
	    continue 
	tmp = ord(c) 
	nr ^= (((nr & 63) + add) * tmp) + (nr << 8) 
	nr2 += (nr2 << 8) ^ nr 
	add += tmp 
    res1 = nr & ((1 << 31) - 1) 
    res2 = nr2 & ((1 << 31) - 1) 
    return "%08lx%08lx" % (res1, res2) 

def mysqlv5(word):
	s = hashlib.sha1()
	s.update(word)
	s2 = hashlib.sha1()
	s2.update(s.digest())
	return s2.hexdigest()

def crack(pw):
	output = ""
	for word in words: 
		word = word.rstrip("\n") 
		if pw == mysql323(word): 
			output = word 
	return output

def crack1(pw):
	output = ""
	for word in words:
		word = word.rstrip("\n") 
		if pw == mysqlv5(word): 
			output = word
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
	
print "\n\t   d3hydr8[at]gmail[dot]com CrackBot MySQL v1.0"
print "\t--------------------------------------------------"

print "[+] CrackBot MySQL Loaded"

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
s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] CrackBot MySQL Loaded"))
s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] Wordlist Length: ",len(words)))

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
				if line[4] != "None" and len(re.findall("[g-z!@#$%^&^*()<>?]", line[4])) == 0 and int(len(line[4])) in [16,40]:
					print "[+] Cracking:",line[4]
					if len(line[4]) == 16:
						output = crack(line[4])
					elif len(line[4]) == 40:
						output = crack1(line[4])
					else:
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] Error Occurred"))
					print "[+] Output:",output
					if output != "":
						s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] cracked: ",output))
					else:
						s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] "+line[4]+" : Not Found"))
				else:
					s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[-] improper length"))
					
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
			
			if line[3] == ":!hash":
				output = mysqlv5(" ".join(line[4:]))
				s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "[+] mysqlv5: "," ".join(line[4:])," == ",output))
				print "[+]"," ".join(line[4:]),"==",output
				output = mysql323(" ".join(line[4:]))
				s.send("PRIVMSG %s :%s%s%s%s\r\n" % (CHAN, "[+] mysql323: "," ".join(line[4:])," == ",output))
				print "[+]"," ".join(line[4:]),"==",output
				
				
			if line[3] == ":!length":
				print "[+] Length:",len(words)
				s.send("PRIVMSG %s :%s%s\r\n" % (CHAN, "[+] wordlist length: ",len(words)))
					
			if line[3] == ":!help":
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "crackB0t options:"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !crack <hash> | crack hash"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !insert <word> | insert word into list"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !hash <word> | generate hash"))
				s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !length | check wordlist length"))
				
				
		except(IndexError):
			pass
		
        	if(line[0]=="PING"):
          		s.send("PONG %s\r\n" % line[1])

