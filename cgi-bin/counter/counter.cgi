#!/usr/bin/perl
#counter.cgi

use CGI;
$q = new CGI;
print $q->header(-charset => "windows-1251");

open FILE, "counter.txt";
  $counter = <FILE>;
close FILE;

$counter++;

open FILE, ">counter.txt";
  print FILE $counter;
close FILE;