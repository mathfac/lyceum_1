#!/usr/bin/perl
#example.cgi
#

#=============================================================
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use DBI;

#=============================================================
$q = new CGI;

$dbh = DBI->connect("DBI:CSV:", $login, $password, \%attr);
print $q->header(-charset => "windows-1251");



            open FILE, "..\..\main\index.shtml";
                $counter=<FILE>;
            close FILE;
                $counter++;
			 print$counter;			
