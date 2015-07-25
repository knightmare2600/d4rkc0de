#!/usr/bin/ruby 
# 
# This script is available under the GPLv3 License. 
# USE COMPLETELY ON YOUR OWN RISK. 
# written by slac3dork & tested on Linux 
# http://snippet.c0de.me 
 
require 'open-uri' 
 
if ARGV.size < 1 
puts '[-] Usage ./domainchecker.rb <domain_name>' 
exit 1 
end 
 
puts '-----------------------------------------------' 
puts '[+] Domain Checker tool' 
puts '[+] domainchecker.rb' 
puts '[+] Coded by slac3dork' 
puts "-----------------------------------------------\n\n" 
 
begin 
	domain_name = ARGV[0] 
	open("http://www.who.is/whois/#{domain_name}") {|page| 
	    page.each_line {|line| 
		    if (line =~ /Invalid Domain or IP/) 
			    puts '[-] ERROR! Please check your domain name' 
			    exit 1 
		    end 
 
		    if (line =~ /Registry Whois Information/) 
			    puts "[-] #{domain_name} is not available" 
		    end 
 
		    if (line =~ /Available for Registration/) 
			    puts "[+] #{line.slice(/([a-z]+[\.]{1}[a-z]{2,})( is Available for Registration)/)}" 
		    end 
 
		    if (line =~ /./) 
			    avail_domain = line.slice(/domain=[a-z]+[\.]{1}[a-z]{2,}/).slice(/[a-z]+[\.]{1}[a-z]{2,}/) 
			    puts "[+] Available Domain:  #{avail_domain}" 
		    end 
		} 
	   } 
rescue 
	puts '[-] Error while executing Domain Checker script. Check you internet connection' 
end
