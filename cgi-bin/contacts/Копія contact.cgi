#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;


$CGI::POST_MAX = 1024 * 50;
$login = undef;
$password = undef;
%attr = (csv_sep_char => ";", csv_eol => "\n");
%vypusk = (99 => "Наши друзья",
           -1 => "Преподаватели");
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


&list();
&table();
&phone();

$dbh->disconnect;


sub list {
    $vypusk = $dbh->selectall_arrayref("select distinct vypusk
                                        from contact");

    $s = $q->p($q->a({ -href => '../../contacts/registration.shtml' }, "Зарегистрируетесь"), "на нашем сайте, или обновите",  $q->a({ -href => '../../contacts/update.shtml'}, "вашу информацию") );
    $s.= $q->p("На данный момент у нас зарегистрировались :");

    foreach (@$vypusk) {
        ($num_vypusk) = @$_;
        if ($num_vypusk < 0 or $num_vypusk == 99) {
            $list = $q->font({ -size => 4 }, $q->a({ -href => "#$num_vypusk" }, $vypusk{$num_vypusk}) );
        } else {
            $year = 1991+$num_vypusk;
            $list = $q->font({ -size => 4 }, $q->a({ -href => "#$num_vypusk" }, "$num_vypusk-й выпуск ($year)") );
        }
        $s .= $q->li([ $list ]);
    }
    print $q->ul( $s );
}


sub table {
    $table = $dbh->selectall_arrayref("select vypusk, id, name, e_mail, icq, tel_home, tel_work, tel_mob, info_status
                                       from contact
                                       order by vypusk");
    $s = $name_vypusk = $phone = "";
    $i = 0;
    foreach (@$table) {
        ($vypusk, $id, $name, $e_mail, $icq, $tel_home, $tel_work, $tel_mob, $info_status) = @$_;
        $js_array .= qq~phone[$id][0]='$tel_home'; phone[$id][1]='$tel_work'; phone[$id][2]='$tel_mob';~;

        if (($vypusk != $table->[$i-1][0]) or ($i == 0)) {
            if ($vypusk < 0 or $vypusk == 99) { $name_vypusk = $q->a({ -name => "$vypusk" }) . $vypusk{$vypusk}; }
                else { $name_vypusk = $q->a({ -name => "$vypusk" }) . "$vypusk-й выпуск"; }
            $s .= $q->Tr([ $q->th( {-colspan => 4, -bgColor => "#51a294" }, [ $q->font({ -color => "#ffffff"}, $name_vypusk) ] ) ]);
        }

        if ($info_status) { $name = $q->a({ -href => "javascript:ShowInfo($id)" }, $name); }

        if ($e_mail) { $e_mail = $q->a({ -href => "mailto:$e_mail" }, $e_mail); }
            else { $e_mail = "&nbsp"; }

        if ($icq) { $icq = $q->img({ -src => "http://wwp.icq.com/scripts/online.dll?icq=$icq&img=5", border => 0, height => 18, wigth => 18}, " $icq"); }
            else { $icq = "&nbsp"; }

        if (($tel_home) or ($tel_work) or ($tel_mob)) { $phone = $q->a({ -href => "javascript:ShowPhone($id)"}, $q->img({ -src => "/images/phone4.gif", border => 0, alt => "Телефон" }) ); }
            else { $phone = "&nbsp"; }

        $s .= $q->Tr([ $q->td([ $name, $e_mail, $icq ]) . $q->td({ -width => 24 }, [ $phone ]) ]);
        $i++;
    }
    $last_id = $i + 10;
    print $q->table({ -borderColor     => "#dddddd",
                      -cellspacing     => 1,
                      -borderColorDark => "#cccccc",
                      -background      => "/images/class2.jpg",
                      -border          => 1,
                      -align           => "center",
                      -width           => "95%" }, $s );
}


sub phone {
    print qq~
        <SCRIPT language="JavaScript">
        phone = new Array ($last_id);
        for (i = 0; i < phone.length; ++i)
            phone[i] = new Array ();
        $js_array;

        function ShowPhone(id) {
            var phone_string = "";
            if (phone[id][0] != '') phone_string += "Домашний телефон - " + phone[id][0] + " ";
            if (phone[id][1] != '') phone_string += "Рабочий телефон - " + phone[id][1] + " ";
            if (phone[id][2] != '') phone_string += "Мобильный телефон - " + phone[id][2];
            alert(phone_string);
        }
        </SCRIPT>
        ~;
}
