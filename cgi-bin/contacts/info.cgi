#!/usr/bin/perl

use CGI qw(:standard);
#use CGI::Carp qw(fatalsToBrowser);
use DBI;

$login = undef;
$password = undef;
%attr = (csv_sep_char => ';', csv_eol => "\n");
$q = new CGI;

$dbh = DBI->connect("DBI:CSV:", $login, $password, \%attr);
$dbh->{csv_table}->{info}->{types} = [Text::CSV_XS::IV(),    #1) id           (integer)
                                      Text::CSV_XS::PV(),    #2) pic          (string)
                                      Text::CSV_XS::PV()];   #3) info         (string)

$id = param("id");
$info_array = $dbh->selectall_arrayref("SELECT pic, info
                                        FROM info
                                        WHERE id = $id");

($pic, $info) = ($info_array->[0][0], $info_array->[0][1]);

print $q->header(-charset => "windows-1251"),
      $q->start_html(-title   => "Особиста інформація",
                     -bgcolor => "#F6F7F2" );
    
if ($pic) {
    print $q->img({-src    => "/contacts/user_pic/$pic",
                   -hspace => 5,
                   -vspace => 5,
                   -border => 0,
                   -align  => "left",
                   -alt    => "photo"});
}

print $info;
print $q->end_html();
$dbh->disconnect;
