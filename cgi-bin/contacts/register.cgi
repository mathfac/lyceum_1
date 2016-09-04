#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;

$CGI::POST_MAX = 1024 * 50;
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
                                         Text::CSV_XS::IV()];   #10)info_status  (integer)

$test=param();
if (defined($test)) {
    register();
} else {
		print $q->header(-charset => "windows-1251");    
    js_functions();
    register_form();
}

$dbh->disconnect;

sub register {
    if (param("name"))      { push @values,  $name     = param("name");      push @column, "name";     }
    if (param("password1")) { push @values,  $password = param("password1"); push @column, "password"; }
    if (param("vypusk"))    { push @values,  $vypusk   = param("vypusk");    push @column, "vypusk";   }
    if (param("e_mail"))    { push @values,  $e_mail   = param("e_mail");    push @column, "e_mail";   }
    if (param("icq"))       { push @values,  $icq      = param("icq");       push @column, "icq";      }
    if (param("tel_home"))  { push @values,  $tel_home = param("tel_home");  push @column, "tel_home"; }
    if (param("tel_work"))  { push @values,  $tel_work = param("tel_work");  push @column, "tel_work"; }
    if (param("tel_mob"))   { push @values,  $tel_mob  = param("tel_mob");   push @column, "tel_mob";  }
    if (param("info"))      { 							 $info     = param("info");      push @col_inf, "info";    }
    if (param("file"))      {                $file     = param("file");      push @col_inf, "pic";     }

    
    if (param("info")) {
	    $info =~ s/\s+/ /g;
	    push @val_inf, $info;
		}    
    
    $sth = $dbh->selectall_arrayref("select id
                                     from contact
                                     where name = '$name' and vypusk = '$vypusk'");
#                                       AND (password = '$password' OR password = '')
    $name_id = $sth->[0][0];
#    $password = $sth->[0][1];
#    $cookie = $q->cookie("register");
#     $cook = "no";
#    if ($cookie eq "yes" and $name_id == 0) {
#        require "contact.cgi";
#        print qq~<SCRIPT language="JavaScript"> alert("З цього комп’ютера вже зареєструвалися! $name_id") </SCRIPT>~;
#     if ($password ne param("password1") and $password ne '') {
#        require "contact.cgi";
#        print qq~<SCRIPT language="JavaScript"> alert("Не вірний пароль!") </SCRIPT>~;
#    } else {




#		}
		if (defined($name_id)) {
        require "contact.cgi";
        print qq~<SCRIPT language="JavaScript"> alert("Таке ім’я вже існує!") </SCRIPT>~;

		} else {
#        if (defined($name_id) and ($password ne "" or $password eq param("password1"))) {
#             $dbh->do("delete
#                       from contact
#                       where id = '$name_id'");
#             $dbh->do("delete
#                       from info
#                       where id = '$name_id'");
#             $id = $name_id;
#        } else {
    $id = get_max_id($dbh, 'contact');
    $id++;
#        }

    if ($info or $file) {
        $info_status = 1;
        if ($file) {
#            $file =~ m/.*\.(.*)$/g;
#						$pref = $1;	
            $pref = $file;
						$pref =~ s/.*\.(.*)$/\1/g;
            $file_name = 0 x (6 - length($id));
            $file_name .= $id . "." . $pref;
#            open TEST, ">test.tst";
#							print TEST $file;
#							print TEST "\n";
#							print TEST $pref;
#							print TEST "\n";
#							print TEST $1;
#            close TEST;
            
            chdir "..";
            chdir "..";
            chdir "contacts";			
            chdir "user_pic";
            open FILE, ">$file_name" or die "Can't open photo file: $!";
                binmode FILE;
                while(<$file>) { print FILE; }
            close FILE;
            chdir ".."; 
            chdir ".."; 
            chdir "cgi-bin";
            chdir "contacts";	
#            open TEST, ">test.tst";
#							print TEST $file_name;
#            close TEST;

            push @val_inf, $file_name;
        }
        push @col_inf, "id";
        push @val_inf, "$id";
        $col_inf = join ", ", @col_inf;
        $val_inf = "'" . join ("','", @val_inf) . "'";
        $dbh->do("insert into
                  info ($col_inf)
                  values ($val_inf)");
    } else { $info_status = 0; }

    push @column,  "info_status";
    push @column,  "id";
    push @values,  "$info_status";
    push @values,  "$id";

    $column = join ", ", @column;
    $values = "'" . join ("','", @values) . "'";

    $dbh->do("insert into
              contact ($column)
              values  ($values)");
		print $q->redirect("contact.cgi");
#    require "contact.cgi";
    }
}

sub get_max_id {
  my $dbh = shift;
  my $table = shift;
  my $max = 0;
  my $id = 0;
  my $sql = "select id from $table";
  my $sth = $dbh->prepare($sql);
  $sth->execute();
  
  ($max) = $sth->fetchrow_array;
  while (($id) = $sth->fetchrow_array) {
    if ($id > $max)  { $max = $id; }
  }
  
  return $max;  
}


sub register_form {
$form = "background-color: #f6f7f2; border-color: #284a82; border-width: 1px; FONT-FAMILY: arial, sans-serif; FONT-SIZE: 10pt; font-width: normal;";

 for ($i = 1; $i <= 
###Attention!!!! Max number of 'vypusk'!!!Change Here!
 13
###Attention!!!!
 ; $i++) { 

	$year = 1991+$i;
	$vypusk{$i} = "$i-й випуск ($year)"; 
}

print $q->br(), $q->br(), $q->br(),
      $q->start_form(-name => "register", -method => "post", action => "register.cgi", -enctype => "multipart/form-data", -OnSubmit => "return CheckForm()"),
      $q->table({ -width => "55%", -border => 0, -align => "center"},
      $q->Tr([ $q->td([ "Імя",                     $q->textfield(     -name => "name",      -style => $form) ]),
               $q->td([ "Пароль",                  $q->password_field(-name => "password1", -style => $form) ]),
               $q->td([ "Підтвердження пароля",    $q->password_field(-name => "password2", -style => $form) ]),
               $q->td([ "Випуск",                  $q->popup_menu(    -name => "vypusk",    -style => $form, -values => [ "Выберите выпуск...", sort {$a <=> $b} keys %vypusk ], -default => "Виберіть випуск...", -labels => { %vypusk }) ]),
               $q->td([ "E-mail",                  $q->textfield(     -name => "e_mail",    -style => $form) ]),
               $q->td([ "ICQ",                     $q->textfield(     -name => "icq",       -style => $form) ]),
               $q->td([ "Домашній телефон",        $q->textfield(     -name => "tel_home",  -style => $form) ]),
               $q->td([ "Рабочий телефон",         $q->textfield(     -name => "tel_work",  -style => $form) ]),
               $q->td([ "Мобільний телефон",       $q->textfield(     -name => "tel_mob",   -style => $form) ]),
               $q->td([ "Коротко про себе",          $q->textarea(      -name => "info",      -style => $form, -cols => 34, -rows => 5) ]),
               $q->td([ "Фотографія",              $q->filefield(     -name => "file",      -style => $form) ]),
               $q->td({ -align => "center"}, [ $q->br() . $q->submit(-value => "Зареєструватися", -style => $form), $q->br() . $q->reset(-value => " Очистити ", -style => $form) ])
            ]) ),
      $q->end_form(),
      $q->br(), $q->br();
}

sub js_functions {
print qq~
    <SCRIPT language="JavaScript">
    function getCookie(name) {
        var prefix = name + "=";
        var start = document.cookie.indexOf(prefix);
        if (start == -1) return null;
        var end = document.cookie.indexOf(";", start+prefix.length);
        if (end == -1) end = document.cookie.length;
        var value = document.cookie.substring(start+prefix.length, end);
        return  unescape(value);
    }
    
    function setCookie(name, value) {
        var expires = new Date("May 15, 2012");
        var newCookie = name + "=" + escape(value)+
        ((expires)?";expires="+expires.toGMTString():"")+";path=/";
        document.cookie = newCookie;
    }

    function CheckForm() {
        with (document.register) {
            if (name.value == '') {
                alert("Ім’я не вказано!!!");
                return false
            } else if (password1.value != password2.value || password1.value == '') {
                if (password1.value == '') alert("Пароль не вказано!!!");
                    else alert("Пароль не відповідає його підтвердженню!!!");
                return false
            } else if (vypusk.value == 'Виберіть випуск...') {
                alert("Випуск не вказано!!!");
                return false
            } else {
                setCookie('register', 'yes');
                return true
            }
        }
    }
    </SCRIPT>
    ~;
}
