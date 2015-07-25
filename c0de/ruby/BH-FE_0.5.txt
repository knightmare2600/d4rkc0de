#!/usr/bin/ruby -w
#====================================================#
# BH-FE 0.5 (BH-Final Eraser Version 0.5)
# Programmed By: Br4v3-H34r7
# Contact: R00T[AT]Br4v3-H34r7[DOT]CoM
# Website: Br4v3-H34r7.CoM | BH2H.CoM
# License: GNU General Public License 3
#====================================================#
# BEGIN THE CODE

def about()
	print "\n\t+----------------------------+\n\t|    BH-Final Eraser  0.5    |\n\t| Programmed By: Br4v3-H34r7 |\n\t| Br4v3-H34r7.CoM - BH2H.CoM |\n\t+----------------------------+\n\n"
end

def usage()
	print "[*] USAGE:\truby #{$0} \"File path or directory\"\n"
	print "[+] EXAMPLE 1:\truby #{$0} \"/root/file.txt\"\n"
	print "[+] EXAMPLE 2:\truby #{$0} \"/root/files/\"\n\n"
end

def check()
	if ARGV.length == 1 then
		file = ARGV[0]
		if File.exist?(file) == true and File.writable?(file) == true
			if File.zero?(file) == true then
				File.delete(file)
				print "[!] File size equal ZERO.. Deleted.\n\n"
			elsif File.directory?(file) == true then
				files = Dir.entries(file)-["..","."]
				if files.empty? == true then
					Dir.delete(file)
					print "[!] The directory is empty.. Deleted.\n\n"
				else
					print "[*] There is #{files.length} files/folders in the directory.\n\n"
					for x in files do
						if File.directory?(file + "/" + x) == true then
							files_num = Dir.entries(file + "/" + x)-[".", ".."]
							if files_num.length != 0 then
								print "[*] The folder #{file + "/" + x} isn't empty.. Skipped.\n\n"
							else
								files.delete(file)
								Dir.delete(file + "/" + x)
								print "[*] The directory #{file + "/" + x} deleted successfully.\n\n"
							end
						else
							myfile = (file + "/" + x)
							file_size = File.size(myfile)
							erase(myfile, file_size)
						end
					end
					files_num = files_num = Dir.entries(file)-[".", ".."]
					if files_num.length != 0 then
						print "[*] The directory #{file} isn't empty.. Skipped.\n\n"
					else
						Dir.delete(file)
						print "[*] The directory #{file} deleted successfully.\n\n"
					end
				end
			else
				file_size = File.size(file)
				erase(file, file_size)
			end
		else
			print"[!] The file/folder isn't exist or it's not writeable.\n\n"
			usage()
		end
	else
		usage()
	end
end

def erase(file, file_size)
	print "[+] Erasing #{file}...\n"
	chars = ")(*&^=%+$-}#!|@{~>:<;/".split("") + ("0".."9").to_a + ("a".."z").to_a + ("A".."Z").to_a
	5.times do
		myfile = File.open(file, 'wb')
  		1.upto(file_size) do
			myfile.write(chars[rand(chars.length)])
		end
		myfile.close
	end
	File.delete(file)
	print "    The file deleted successfully.\n\n"
end

# Here We Go #
about()
check()

# END THE CODE
#====================================================#