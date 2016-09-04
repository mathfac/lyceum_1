#!/usr/bin/perl
#countershow.cgi

use CGI;
$q = new CGI;
print $q->header(-charset => "windows-1251");

open FILE, "counter.txt";
  $counter = <FILE>;
close FILE;
print $counter;
