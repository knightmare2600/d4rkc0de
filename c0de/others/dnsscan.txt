#!/bin/bash

( echo "|)|\|s(an(dnscan) For solaris 2.5"; echo ) >&2

### Define global constants

TMPDIR=.
LOCKFILE=$TMPDIR/dnscan.lock

### Print usage information

usage()

{
cat << end-of-text

Usage: dnscan [-file <filename>] [-domain <domain>] [-sub <subdomain>]

-file		Usages <filename> as a list of subdomains and servers to scan.
-domain		Lists all servers in a first level domain like edu, com or net.
-subdomain	Lists all servers in a domain.

The -domain mode will first create a file called 'domain.<domain>' with a
list of all subdomains and their name servers, and then use that file in
the -file mode.

The input file needs to have the following format:
<domain> <subdomain> [<dns>]

* To list all servers in Japan, do "dnscan -domain jp".
* To list all servers in the netcom domain, do "dnscan -sub netcom.com".

end-of-text
}

### Strip away all unwanted lines from the output of the 'ls -d'

clean_serverlist()

{
	sed -n " {
		/^.*\. /d
		/127.0.0.1$/d
		/ A     /s/^ /$SUBDOMAIN    /p
		/ HINFO /s/^ /$SUBDOMAIN    /p
	} " | sort -u
}

### List all the name servers handling the selected subdomain

list_subdomain_dns()
 
{
	echo "$SUBDOMAIN" | nslookup -querytype=ns | \
		sed -n 's/.*nameserver = //p'
}

### Print a formated list of all servers (recordtype A) in a subdomain

list_subdomain()

{
	[ -z "$DNS" ] && DNS=`list_subdomain_dns | sed -n 1p`

	echo "ls -d $SUBDOMAIN" | nslookup - $DNS | clean_serverlist
}

### Scan all subdomains listed in a file

from_file()

{
	while read domain subdomain DNS; do
		SUBDOMAIN=$subdomain.$domain

		if [ $POS ]; then
			[ $SUBDOMAIN != $POS ] && continue
			unset POS
		fi

		echo "Scanning $SUBDOMAIN" >&2
		echo "$INFILE $SUBDOMAIN" > $LOCKFILE

		list_subdomain

		echo
	done < $INFILE
}

### Strip away all but the NS lines from the output of the 'ls -d'

clean_dnslist()

{
	sed -n " {
		/^.*\. /d
		s/^ /$DOMAIN    /
		s/ NS   / /p
	} " | sort -u +1 -2
}

### List all the name servers handling the selected domain

list_domain_dns()

{
	(	echo root
		echo $DOMAIN
	) | nslookup -querytype=ns -domain=$DOMAIN | \
		sed -n 's/.*nameserver = //p'
}

### List all name servers in the selected domain

list_domain()

{
	DOMAINFILE=domain.$DOMAIN

	domain_dns=`list_domain_dns | sed -n 1p`

	echo "Using domain name server $domain_dns for *.$DOMAIN" >&2

	echo "ls -d $DOMAIN" | nslookup - $domain_dns | clean_dnslist > \
		$DOMAINFILE

	MODE=file
	INFILE=$DOMAINFILE

	from_file
}

### Parse flags

while [ -n "$1" ]; do
	case "$1" in
		-file)		MODE=file
				INFILE=$2
				shift
				break
				;;
		-domain)	MODE=domain
				DOMAIN=$2
				shift
				break
				;;
		-sub)		MODE=subdomain
				SUBDOMAIN=$2
				shift
				break
				;;
		*)		usage
				exit
				;;
	esac

	shift
done

### Look for previously interrupted scan

if [ -f $LOCKFILE ]; then
        echo "Continue previously interrupted scan [n]? \c" >&2
        read r

        if [ `echo x$r | grep -i "^xy"` ]; then
                read INFILE POS < $LOCKFILE
                [ $POS ] && MODE=file
        fi
 
        echo >&2
fi

### Select mode

case $MODE in
	file)		from_file
			;;
	domain)		list_domain
			;;
	subdomain)	list_subdomain
			;;
esac

### Clean up temporary files we have created

rm $LOCKFILE 2>/dev/null

