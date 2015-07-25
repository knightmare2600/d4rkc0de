#!/usr/bin/env ruby
# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# This is a  quick n dirty pma scanner in ruby
# so that ppl can use a open source tool, 
# and not a precompiled executeable like pmafind!
# This script produces some false positives too,
# so dont worry, just hand check em after scan
# (this version has a timout = 30 so kids dont use it)
# 
# Author: naxxatoe
# Version: 1.0 Beta
# Copyright (c) 2007 Nice Name Crew
# Web: http://www.nicenamecrew.com/
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Nice Name crew is not responsible for any damage done
# by users of this program.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # #
require 'net/http'

#Set the Range that you want to scan
range	= ARGV[0].to_i
sub0	= ARGV[1].to_i
sub1	= ARGV[2].to_i
sub2	= ARGV[3].to_i
range2  = ARGV[5].to_i
sub00   = ARGV[6].to_i
sub01   = ARGV[7].to_i
sub02   = ARGV[8].to_i

#specify pma dir
path	= "/phpmyadmin/"
file    = "print.css"

#do not change anyting below unless you know what you are doing
if ARGV[4] == "-"
	pmapath = path + file
	scan_done= 0       
	while scan_done  < 1
		scanip   = range.to_s + "." + sub0.to_s + "." + sub1.to_s + "." + sub2.to_s
		scanhost = "http://" + scanip + "/phpmyadmin/index.php" 
		if range2 == range
			if sub00 == sub0
				if sub01 == sub1
					if sub02 == sub2
						break
					end
				end
			end
		end
		begin
			res = Net::HTTP.get_response(scanip, pmapath, 80)
			begin
                		if res.code.to_i == 200
					puts "Phpmyadmin found: " + scanhost
                       			pma_found   = File.open("found.txt", "a")
                        		pma_found.write "Found: " + scanhost + "\r\n"
                        		pma_found.close
				else
					puts "Webserver found: " + scanip
					web_servers = File.open("webservers.txt", "a")
					web_servers.write scanip + "\r\n"
					web_servers.close
				end                               
                	rescue
        		end
		rescue
       			puts "Clean: " + scanip
		rescue Timeout::Error
			puts "Timeout: "+scanip
		end
	
		if sub2 == 255
			sub2  = 1
			sub1 += 1
		end
		if sub1 == 255
			sub1  = 1
			sub0 += 1
		end
		if sub0 == 255
			sub0   = 1
			range += 1
		end
		sub2 += 1	
	end
	puts "Scan - Done!"
else
	puts "Wrong Scan command!"
end

