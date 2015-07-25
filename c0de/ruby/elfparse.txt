 #!/usr/bin/env ruby

$Verbose = true


target = open(ARGV[0],'r')

puts ""

ei_mag = target.read(4)
printf("magic number:                   ")
   case ei_mag
     when "\x7f\x45\x4c\x46" :printf("%s :  alright :)",ei_mag)
     else                     printf("%s :  upps no magic!!",ei_mag)
   end
puts ""

ei_class = target.read(1)
printf("file's class:                    ")
   case ei_class
     when "\x1"              :print("32bit")
     when "\x2"              :print("64bit")
     else                     print("invalid")
   end
puts ""

ei_data = target.read(1)
printf("data encoding:                   ")
   case ei_data
     when "\x1" :print("little endian")
     when "\x2" :print("big endian")
     else        print("invalid")
   end
puts ""

ei_version = target.read(1)
printf("elf header version:              ")
   case ei_version
     when "\x1" :print("current")
     else        print("invalid")
   end
puts ""


ei_osabi = target.read(1)
printf("OS/ABI:                          ")
   case ei_osabi
       when "\x0"   :print("UNIX System V ABI")
       when "\x1"   :print("HP-UX operating system")
       when "\x255" :print("Standalone(embedded)application")
   end
puts ""


ei_abiversion = target.read(1)
printf("ABI Version:                     ")
   case ei_abiversion
       when "\x0"   :print("0")
       else          print("seems not valid")
   end
puts ""

ei_pad = target.read(7)
  printf("number of padding bytes:         %d",ei_pad.length)
puts ""

e_type = target.read(2)
e_type.reverse! if ei_data == "\x1"
print("object file type:         ")
   case e_type
      when "\x0\x0"   :print("       No file type")
      when "\x0\x1"   :print("       Relocatable file")
      when "\x0\x2"   :print("       Executable file")
      when "\x0\x3"   :print("       Shared object file")
      when "\x0\x4"   :print("       Core file")
      when "\xff\x00" :print("       Processor-specific (LOPROC)")
      when "\xff\xff" :print("       Processor-specific (HIPROC)")
   end
puts ""

e_machine = target.read(2)
e_machine.reverse! if ei_data == "\x1"
print("architecture:                ")
   case e_machine
     when "\x0\x0"  :print("    No machine")
     when "\x0\x1"  :print("    AT&T WE 32100")
     when "\x0\x2"  :print("    SPARC")
     when "\x0\x3"  :print("    Intel 80386")
     when "\x0\x4"  :print("    Motorola 68000")
     when "\x0\x5"  :print("    Motorola 88000")
     when "\x0\x7"  :print("    Intel 80860")
     when "\x0\x8"  :print("    MIPS RS3000")
   end
puts ""

e_version = target.read(4)
e_version.reverse! if ei_data == "\x1"
printf("object file version:             ")
   case e_version
     when "\x0\x0\x0\x1" :print("current")
     else                 print("invalid")
   end
puts ""

e_entry = target.read(4)
e_entry.reverse! if ei_data == "\x1"
printf("entry point:                     ")
print e_entry.unpack('H8')
puts ""

e_phoff = target.read(4)
e_phoff.reverse! if ei_data == "\x1"
printf("program headers start:           ")
print e_phoff.unpack('N')
print (' (bytes into file)')
puts ""

e_shoff = target.read(4)
e_shoff.reverse! if ei_data == "\x1"
printf("section headers start:           ")
print e_shoff.unpack('NNN')
print (' (bytes into file)')
puts ""

e_flags = target.read(4)
e_flags.reverse! if ei_data == "\x1"
printf("flags:                           ")
print e_flags.unpack('H2H2H2H2')
puts ""

e_ehsize = target.read(2)
e_ehsize.reverse! if ei_data == "\x1"
printf("This headers size:               ")
print e_ehsize.unpack('n')
puts ""

e_phentsize = target.read(2)
e_phentsize.reverse! if ei_data == "\x1"
printf("program headers size:            ")
print e_phentsize.unpack('n')
puts ""

e_phnum = target.read(2)
e_phnum.reverse! if ei_data == "\x1"
printf("number of program headers:       ")
print e_phnum.unpack('n')
puts ""

e_shentsize = target.read(2)
e_shentsize.reverse! if ei_data == "\x1"
printf("section headers size:            ")
print e_shentsize.unpack('n')
puts ""

e_shnum = target.read(2)
e_shnum.reverse! if ei_data == "\x1"
printf("number of section headers:       ")
print e_shnum.unpack('n')
puts ""

e_shstrndx = target.read(2)
e_shstrndx.reverse! if ei_data == "\x1"
printf("shd string table index:          ")
print e_shstrndx.unpack('n')
puts ""
puts "" 