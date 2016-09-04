#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;

$CGI::POST_MAX = 1024 * 50;
#$CGI_MAX = 1024 * 15;
$login = undef;
$password = undef;
%attr = (csv_sep_char => ";", csv_eol => "\n");
%vypusk = (99 => "Наші друзі",
           -1 => "Викладачі");
$q = new CGI;

$dbh = DBI->connect("DBI:CSV:", $login, $password, \%attr);
$dbh->{csv_table}->{contact}->{types} = [Text::CSV_XS::IV(),    #1) vypusk       (integer)
                                         Text::CSV_XS::IV(),    #2) id           (integer)
                                         Text::CSV_XS::PV(),    #3) name         (string)
                                         Text::CSV_XS::PV(),    #4) e-mail       (string)
                                         Text::CSV_XS::NV(),    #5) icq          (double)
                                         Text::CSV_XS::PV(),    #6) tel-home     (string)
                                         Text::CSV_XS::PV(),    #7) tel-work     (string)
                                         Text::CSV_XS::PV(),    #8) tel-mob      (string)
                                         Text::CSV_XS::PV(),    #9) password     (string)
                                         Text::CSV_XS::IV()];   #10)info_status  (string)



%param = init_parhash();
parse_param();
#@test = $q->param;
#login();
#

#$w = join " ", @test; 
#print $w;
#print "<br>";
#print $param{name};
#print $param{password};
#init_password($param{name}, $param{password});

sub parse_param {

#print $q->header;


  
  if (!isparam()) {
		print $q->header(-charset => "windows-1251");
    login();
  } elsif (exists $param{id}) {
    update();
  }  elsif (exists $param{login}) { # and defined $param{password}
		print $q->header(-charset => "windows-1251");
    update_form();

  } else {
		print $q->header(-charset => "windows-1251");
    print error_mes('Заповніть всі поля!');
    login();

  }
}

sub login {
$form = "background-color: #f6f7f2; border-color: #284a82; border-width: 1px; FONT-FAMILY: arial, sans-serif; FONT-SIZE: 10pt; font-width: normal;";
print $q->br(), $q->br(), $q->br(),
      $q->start_form(-name => "login", -method => "get", action => "update.cgi"),
      $q->table({ -width => "55%", -border => 0, -align => "center"},
      $q->Tr([ $q->td([ "Ім’я",                     $q->textfield(     -name => "name",      -style => $form) ]),
               $q->td([ "Пароль",                  $q->password_field(-name => "password",  -style => $form) ]),
               $q->td({ -align => "center"}, [ $q->br() . $q->submit(-value => "Ввійти", -name => "login", -style => $form), $q->br() . $q->reset(-value => " Очистити ", -style => $form) ])
            ]) ),
      $q->end_form(),
      $q->br(), $q->br();
}

sub update {

  my $info_status;
#  my $file;
  if ($param{info} or $param{file}) {
    $info_status = 1;
    if ($param{file}) {
#      $param{file} =~ m/.*\.(.*?)$/g;
#      my $pref = $1;
#      my $file_name = 0 x (6 - length($param{id})) . "$param{id}\.$pref";
#      $file = param("file");
      $pref = $param{file};
			$pref =~ s/.*\.(.*)$/\1/g;
      $file_name = 0 x (6 - length($param{id}));
      $file_name .= $param{id} . "." . $pref;

            chdir "..";
            chdir "..";
            chdir "contacts";			
            chdir "user_pic";
      unlink $file_name;
      open FILE, ">$file_name" or die "Can't open photo file: $!";
#        binmode FILE;
#				$space = 0;
        while (read($param{file}, $buffer, 1024)) { 
#        	$space+=1024;
#        	if ($space >= $CGI_MAX) {
#        		print "Big Size!!!!";

#        	}
        	print FILE $buffer; 
        }
      
      close FILE;
            chdir ".."; 
            chdir ".."; 
            chdir "cgi-bin";
            chdir "contacts";	
      $file = $file_name;
    } else {
      my $sth = $dbh->prepare("select pic from info where id='$param{id}'");
      $sth->execute();
      my $href = $sth->fetchrow_hashref();
      $file = $href->{pic};
    }
  } else { 
    $info_status = 0; 
  }
  
  $dbh->do("delete from contact where id='$param{id}'");
  $dbh->do("delete from info where id='$param{id}'");
  
  my @column_contact = qw(vypusk id name e_mail icq tel_home tel_work tel_mob password info_status);
  my @values_contact = ($param{vypusk}, $param{id}, $param{name}, $param{e_mail}, $param{icq}, $param{tel_home}, $param{tel_work}, $param{tel_mob}, $param{password}, $info_status);

  my %contact = get_exists_hesh(@column_contact, @values_contact);
  my $column_contact = join ", ", (keys %contact);
  my $values_contact = "'" . join ("','", (values %contact)) . "'";
  $dbh->do("insert into contact ($column_contact) values ($values_contact)");

  if ($info_status) {
    $param{info} =~ s/\s+/ /g;
    my @column_info = qw(id pic info);
    my @values_info = ($param{id}, $file, $param{info});
  
    my %info = get_exists_hesh(@column_info, @values_info);
    my $column_info = join ", ", (keys %info);
    my $values_info = "'" . join ("','", (values %info)) . "'";
  
    $dbh->do("insert into info ($column_info) values ($values_info)");
  }

  print $q->redirect("contact.cgi");
}




sub update_form {
  my $id = init_password($param{name}, $param{password});
  if ($id != 0) {
  my $sql_cont = "select vypusk, name, e_mail, icq, tel_home, tel_work, tel_mob, password, info_status from contact where id=$id";
  my $sth = $dbh->prepare($sql_cont);
  $sth->execute();
  my $cont_ref = $sth->fetchrow_hashref();
  my $info_ref;

  if ($cont_ref->{info_status}) {
    my $sql_info = "select pic, info from info where id=$id";
    my $sth = $dbh->prepare($sql_info);
    $sth->execute();
    $info_ref = $sth->fetchrow_hashref();
    if ($info_ref->{pic}) {
      $info_ref->{pic} = $q->img({-src => "/user_pic/$info_ref->{pic}", -hspace => 5, -vspace => 5, -border => 0, -align => "left", -alt => "photo"});
    }
  }
  
  $form = "background-color: #f6f7f2; border-color: #284a82; border-width: 1px; FONT-FAMILY: arial, sans-serif; FONT-SIZE: 10pt; font-width: normal;";
  for ($i = 1; $i <= 11; $i++) { 
    $year = 1991+$i;
    $vypusk{$i} = "$i-й випуск ($year)"; 
  }

  print $q->br(), $q->br(), $q->br(),
        $q->start_form(-name => "register", -method => "post", action => "update.cgi", -enctype => "multipart/form-data"),
        $q->hidden(-name => "id", -default => $id),
        $q->table({ -width => "55%", -border => 0, -align => "center"},
        $q->Tr([ $q->td([ "Ім’я",                     $q->textfield(     -name => "name",      -default => $cont_ref->{name},     -style => $form) ]),
                 $q->td([ "Пароль",                  $q->password_field(-name => "password",  -default => $cont_ref->{password}, -style => $form) ]),
                 $q->td([ "Підтвердження пароля",    $q->password_field(-name => "password1", -default => $cont_ref->{password}, -style => $form) ]),
                 $q->td([ "Випуск",                  $q->popup_menu(    -name => "vypusk",    -default => $cont_ref->{vypusk},   -style => $form, -values => [ "Виберіть випуск...", sort {$a <=> $b} keys %vypusk ], -labels => { %vypusk }) ]),
                 $q->td([ "E-mail",                  $q->textfield(     -name => "e_mail",    -default => $cont_ref->{e_mail},   -style => $form) ]),
                 $q->td([ "ICQ",                     $q->textfield(     -name => "icq",       -default => $cont_ref->{icq},      -style => $form) ]),
                 $q->td([ "Домашній телефон",        $q->textfield(     -name => "tel_home",  -default => $cont_ref->{tel_home}, -style => $form) ]),
                 $q->td([ "Рабочий телефон",         $q->textfield(     -name => "tel_work",  -default => $cont_ref->{tel_work}, -style => $form) ]),
                 $q->td([ "Мобільний телефон",       $q->textfield(     -name => "tel_mob",   -default => $cont_ref->{tel_mob},  -style => $form) ]),
                 $q->td([ "Коротко про себе",          $q->textarea(      -name => "info",      -style => $form, -cols => 34, -rows => 5, -default => $info_ref->{info}) ]),
                 $q->td([ "Фотографія",              $q->filefield(     -name => "file",      -style => $form) ]),
#                 $q->td([ "Удалить фото" . "<input type='checkbox' name='delphoto' style='$form'>",                  $info_ref->{pic} ]),
                 $q->td([ "&nbsp",                  $info_ref->{pic} ]),
                 $q->td({ -align => "center"}, [ $q->br() . $q->submit(-value => "Зберегти", -name => "update", -style => $form), $q->br() . $q->reset(-value => " Очистити ", -style => $form) ])
              ]) ),
        $q->end_form(),
        $q->br(), $q->br();

  } else {
    print error_mes('Не вірне ім’я чи пароль!');
    login();
  }
}

sub init_password {
  my $name = shift;
  my $pas = shift;
  my $sth = $dbh->prepare("select id from contact where name=? and password=?");
  $sth->execute($name, $pas);
  my $href=$sth->fetchrow_hashref();
  if (defined $href->{id}) {
    return $href->{id};
  } else {
    return 0;
  }
}

sub init_parhash {
  my $hash;
  my @names = $q->param;
  foreach (@names) {
    if ($q->param($_)) {
      $hash{$_} = $q->param($_);
    } 
  }
  return %hash;
}

sub isparam {
	my $num_pair = %param;
  if ($num_pair > 0) {
    return 1;
  } else {
    return 0;
  }
#  return length($ENV{QUERY_STRING});
}

sub error_mes {
  my $string = shift;
  $string = "<br><div align='center' color='#FF0000'>" . $string . "</div>";
  return $string;
}

sub get_exists_hesh {
  my @key = @_[0..@_/2-1];
  my @value = @_[@_/2..@_-1];
  my ($i, %ins);
  for ($i = 0; $i < @value; $i++) {
    if (defined $value[$i]) {
      $ins{$key[$i]} = $value[$i];
    }
  }
  return %ins;
}
