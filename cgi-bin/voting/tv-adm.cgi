#!/usr/bin/perl
#tv-adm.cgi

#=============================================================

$password="lyceum1"; # пароль доступу до адміністрування
# можна змінити його по мірі потреби

#=============================================================

use CGI::Carp qw(fatalsToBrowser);
require "vars.txt";

#=============================================================


$body="<HTML><HEAD><TITLE>Голосування на ліцейському сайті - адміністрування</TITLE><link REL=STYLESHEET TYPE=text/css HREF=../../style.css></HEAD><BODY><center>";
$tag="<font face=arial size=2><b>";


if ($ENV{'REQUEST_METHOD'} eq 'GET'){$query=$ENV{'QUERY_STRING'};}
else {if ($ENV{'REQUEST_METHOD'} eq 'POST'){read(STDIN, $query, $ENV{'CONTENT_LENGTH'});}
else {exit;}
}

$query=~tr/;'`\|*~<>()[]{}$\n\r//d;
chomp($query);

@pairs=split /&/,$query;
foreach $pair (@pairs){
($name,$value)=split /=/,$pair;
$name=~tr/+/ /;
$name=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value=~tr/+/ /;
$value=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
if ($name eq "del-row"){$del_row[$value]=1}
if ($name eq "row"){push(@row,$value)}
if ($name eq "number"){push(@number,$value)}
if ($name eq "del_file"){push(@del_file,$value)}
$FORM{$name}=$value;
}
$action=$FORM{'action'};
$page=$FORM{'page'};
if ($page eq ""){$page=0}
$page=int($page);

$FORM{'file'}=~tr/\.\/\\//d;

$user_logged=0;

if ($action eq "login"){goto LOGIN}
if ($action eq 'logging'){goto LOGGING}
if ($action eq 'exit'){
print "Content-type: text/html\n";
print "Set-Cookie: tvadm-pass=; path=/;\n";
print "Location: tv-adm.cgi\n\n";
exit;
}

unless (check_cookie()){
print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=login\n\n";
exit;
}
if ($query eq ''){print "Content-type: text/html\n\n$body\n\n$tag\n\n";goto START}


if ($action eq "make_vote"){goto MAKE_VOTE}
if ($action eq "make_shell"){goto MAKE_SHELL}
if ($action eq "add"){goto ADD}
if ($action eq "edit_data"){goto EDIT_DATA}
if ($action eq "edit_shell_data"){goto EDIT_SHELL_DATA}
if ($action eq "delete"){goto DELETE}
if ($action eq "delete_shell"){goto DELETE_SHELL}
if ($action eq "show_shell"){goto SHOW_SHELL}

print "Content-Type: text/html\n\n";
print "$body\n\n$tag\n\n";

if ($action eq "start"){goto START}
if ($action eq 'new_vote'){goto NEW_VOTE}
if ($action eq 'new_shell'){goto NEW_SHELL}
if ($action eq 'edit'){goto EDIT}
if ($action eq 'edit_shell'){goto EDIT_SHELL}
if ($action eq 'vote-on-page'){goto VOTE_ON_PAGE}
if ($action eq 'view'){goto VIEW}
if ($action eq 'viewlog'){goto VIEW_LOG}


print "Виклик скрипта з неправильним параметром!";

down();

exit;


###################################################
# форма вводу пароля                              #
###################################################
LOGIN:

if (check_cookie()){print "Content-type: text/html\n\n";goto ENTER}

print "Content-type: text/html\n";
print "Set-Cookie: tvadm-pass=; path=/;\n\n";

print "$body\n\n$tag\n\n";

menu();

print "<font size=4>\n";
print "Вхід\n";
print "</font><br><font size=3>\n";
print "</font>\n";
print "<hr width=300>\n";

LOGIN1:

print "<center>\n<form action=tv-adm.cgi method=post>\n";
print "<input type=hidden name=action value=logging>\n";
print "<table border=0>\n";
print "<tr><td>${tag}Пароль: </td><td>${tag}<input type=password size=20 name=user_password></td></tr>\n";
print "<tr><td colspan=2 align=center>$tag<input type=submit value=\"Ввійти\"></td></tr>\n";
print "</table>\n";
print "</form>\n\n";


unless (-d "$data_dir"){

print "<br>\n";
print "<font color=red>Помилка</font>: не знайдено локальний шлях до файлів з даними, заданий у змінній \$data_dir.<br>\n";
print "Поточне значення змінної \$data_dir: $data_dir<br>\n";
print "Правильний локальний шлях до корневого каталогу: $ENV{'DOCUMENT_ROOT'}<br>\n";
print "Виправте змінну \$data_dir у файлі vars.txt або створіть каталог $data_dir<br>\n";
print "<br>\n";

}


down();

exit;


###################################################
# прописування введеного пароля                   #
###################################################
LOGGING:

print "Content-type: text/html\n";
print "Set-Cookie: tvadm-pass=$FORM{'user_password'}; path=/;\n";

ENTER:

print "Location: tv-adm.cgi?action=start\n\n";

exit;



###################################################
# редагування, створення, видалення голосувань    #
###################################################
START:

print "<script language=\"JavaScript\">\n";
print "<!--\n";

print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n\n";

print "// -->\n";
print "</script>\n";

menu();

print "<br><a href=\"javascript:open_new_window('$help_url/edit_votes.html',500,520)\"><img src=$help_url/help.gif border=0></a>&nbsp;&nbsp;&nbsp;&nbsp;";
print "Створення, Редагування, Перегляд і Видалення голосувань\n<br><br>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?action=new_vote>Створити нове голосування</a>\n";
print "</td></tr></table>\n\n";

print "<br>\n\n";

print "<table border=1 cellspacing=0>\n";
print "<tr><td colspan=4 align=center>${tag}кольором відмічені файли:</td></tr>";
print "<tr><td colspan=2 align=center>${tag}редагування</td><td colspan=2 align=center>${tag}перегляд</td></tr>";
print "<tr><td bgcolor=\#bfbfff>$tag&nbsp;&nbsp;&nbsp;&nbsp;</td><td><font face=arial size=1><b>&nbsp;файл голосування&nbsp;&nbsp;</td>\n";
print "<td bgcolor=\#efefaf>$tag&nbsp;&nbsp;&nbsp;&nbsp;</td><td><font face=arial size=1><b>&nbsp;лог-файл&nbsp;&nbsp;</td></tr>\n";
print "<tr><td bgcolor=\#ffefff>$tag&nbsp;&nbsp;&nbsp;&nbsp;</td><td><font face=arial size=1><b>&nbsp;шаблон для створення нових голосувань&nbsp;&nbsp;</td>\n";
print "<td bgcolor=\#bfbfcf>$tag&nbsp;&nbsp;&nbsp;&nbsp;</td><td><font face=arial size=1><b>&nbsp;список IP-адрес&nbsp;&nbsp;</td></tr>\n";
print "</table>\n";
print "<br>\n";

opendir (DIR, "$data_dir/vote");
@files=readdir (DIR);
closedir (DIR);
shift(@files);shift(@files);
@files=sort(@files);


print "<form action=tv-adm.cgi method=post>\n";
print "<input type=hidden name=action value=delete>\n";

print "<table border=1 cellspacing=0>\n";
print "<tr><td colspan=3 align=center>$tag\n<input type=submit value=\"Знищити виділені файли\" onClick=\"return confirm('Ви дійсно хочете знищити файл(и)?')\";>\n</td></tr>\n";

print "<tr bgcolor=\#ffefff><td align=right colspan=2>${tag}<a href=tv-adm.cgi?action=edit&file=template>шаблон</a>&nbsp;";
print "<br><font size=1 color=\"#af3030\">(у шаблоні містяться дані для створення нових голосувань)</font></td><td>&nbsp;</td></tr>\n\n";

$oldname="";
@colors=("ffafbf","bfffcf");

for $i(0..$#files){
$files[$i]=~s/.txt//;
($name,$h)=split /-/,$files[$i];

if ($name eq 'template'){next}

if ($name ne $oldname){@colors[0,1]=@colors[1,0];$oldname=$name}

print "<tr bgcolor=\#$colors[0]><td align=right>\n";
if ($h){print "<input type=checkbox name=\"del_file\" value=\"$name-$h\"></td>\n"}
else {print "<input type=checkbox name=\"del_file\" value=\"$name\"></td>\n"}

print "<td align=right bgcolor=\#";

if ($h eq 'ip'){print "bfbfcf>$tag<a href=tv-adm.cgi?action=view&file=$name-$h>"}
elsif ($h eq 'log'){print "efefaf>$tag<a href=tv-adm.cgi?action=viewlog&file=$name-$h>"}
elsif ($h eq 'temp'){print "bfbfcf>$tag<a href=tv-adm.cgi?action=view&file=$name-$h>"}
else {print "bfbfff>$tag<a href=tv-adm.cgi?action=edit&file=$name>"}


print "$name";
if ($h){print "-$h"}
print "</a>&nbsp;\n</td><td>\n";

file_date();


sub file_date(){
# дата останньої зміни файлу

@months = ('01','02','03','04','05','06','07','08','09','10','11','12');
($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime((stat($data_dir."/vote/".$files[$i].".txt"))[9]);
$year-=100;
if($year < 10) { $year = "0$year"; }
if($hour < 10) { $hour = "0$hour"; }
if ($min < 10) { $min = "0$min"; }
if ($sec < 10) { $sec = "0$sec"; }

$mod_date = "$mday.$months[$mon].$year $hour:$min.$sec";
}


print "$tag<font size=1>&nbsp;$mod_date</td></tr>\n\n";

}

print "<tr><td colspan=3 align=center>$tag<input type=submit value=\"Знищити виділені файли\" onClick=\"return confirm('Ви дійсно хочете знищити файл(и)?')\";></td></tr>\n";
print "</table>\n";
print "</form>\n\n";



# html-оболонки

opendir (DIR, "$data_dir/shells");
@shells=readdir (DIR);
closedir (DIR);
shift(@shells);shift(@shells);
@shells=sort(@shells);


print "<br><a href=\"javascript:open_new_window('$help_url/edit_shells.html',500,520)\"><img src=$help_url/help.gif border=0></a>&nbsp;&nbsp;&nbsp;&nbsp;";
print "Створення, Редагування, Перегляд И Видалення html-оболонок\n<br><br>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?action=new_shell>Створити нову html-оболонку</a>\n";
print "</td></tr></table>\n\n";

print "<br>\n\n";

print "<form action=tv-adm.cgi method=post>\n";
print "<input type=hidden name=action value=delete_shell>\n";

print "<table border=1 cellspacing=0 bgcolor=\#bfbfcf>\n";
print "<tr><td colspan=2 align=center>$tag\n<input type=submit value=\"Видалити відмічені html-оболонки\" onClick=\"return confirm('Ви дійсно хочете видалити html-оболонки?')\";>\n</td></tr>\n";

unless (@shells){
print "<tr><td align=center colspan=3>\n";
print "html-оболонок нема.";
print "</td></tr>\n";
}

else {

for $i(0..$#shells){
$shells[$i]=~s/.txt//;

print "<tr><td align=right width=20>\n";
print "<input type=checkbox name=\"del_file\" value=\"$shells[$i]\"></td>\n";

print "<td align=right width=300>";

print "$tag<a href=tv-adm.cgi?action=edit_shell&file=$shells[$i]>";
print "$shells[$i]";
print "</a>&nbsp;\n</td></tr>\n";


}

}


print "<tr><td colspan=2 align=center>$tag<input type=submit value=\"Видалити відмічені html-оболонки\" onClick=\"return confirm('Ви дійсно хочете видалити html-оболонки?')\";></td></tr>\n";
print "</table>\n";
print "</form>\n\n";

######################


down();

exit;


###################################################
# форма створення нового голосування              #
###################################################
NEW_VOTE:

menu();

print "<form action=tv-adm.cgi method=post name=fileform>\n";
print "<input type=hidden name=action value=make_vote>\n";

print "Введіть ім’я файлу голосування:<br><br>\n";
print "<input type=text size=20 name=file value=\"$FORM{'file'}\">\n";
if ($error=~/fileexists/){print "<br><font color=red size=1>Голосування з таким іменем вже існує.</font>\n";}
if ($error=~/filename/){print "<br><font color=red size=1>Недоступні символи в імені голосування.<br>Використовуйте тільки прописні латинскі букви, цифри і знак \"_\".</font>\n";}
if ($error=~/filelength/){print "<br><font color=red size=1>Ім’я голосування не повинно перевищувати 20 символів.</font>\n";}

print "<br><br><input type=submit value=Створити><br><br>\n";
print "</form>\n\n";


down();

exit;



###################################################
# форма створення нової html-оболонки             #
###################################################
NEW_SHELL:

menu();

print "<form action=tv-adm.cgi method=post name=fileform>\n";
print "<input type=hidden name=action value=make_shell>\n";

print "Введіть ім’я файлу html-оболонки:<br><br>\n";
print "<input type=text size=20 name=file value=\"$FORM{'file'}\">\n";
if ($error=~/fileexists/){print "<br><font color=red size=1>html-оболонка з таким іменем вже існує.</font>\n";}
if ($error=~/filename/){print "<br><font color=red size=1>Недоступні символи в імені html-оболонки.<br>Використовуйте тільки прописні латинскі букви, цифри і знак \"_\".</font>\n";}
if ($error=~/filelength/){print "<br><font color=red size=1>Ім’я html-оболонки не повинно перевищувати 20 символів.</font>\n";}

print "<br><br><input type=submit value=Створити><br><br>\n";
print "</form>\n\n";


down();

exit;



###################################################
# створення файлу нового голосування              #
###################################################
MAKE_VOTE:

$error="";

if (-e "$data_dir/vote/$FORM{'file'}.txt"){$error.="fileexists "}

unless ($FORM{'file'} =~ /^[a-z0-9_]+$/){$error.="filename "}
if (length($FORM{'file'})>20){$error.="filelength "}

if ($error){print "Content-type: text/html\n\n";print "$body\n\n$tag\n\n";goto NEW_VOTE}


if (&lock("$data_dir/vote/template.txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/template.txt";
@template=<FILE>;
close FILE;
if (&unlock("$data_dir/vote/template.txt"))
{print "$error_message";exit}


if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,">$data_dir/vote/$FORM{'file'}.txt";
print FILE @template;
close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}

chmod(0755,"$data_dir/vote/$FORM{'file'}.txt");

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=edit&file=$FORM{'file'}\n\n";

exit;


###################################################
# створення файлу нової html-оболонки             #
###################################################
MAKE_SHELL:

$error="";

if (-e "$data_dir/shells/$FORM{'file'}.txt"){$error.="fileexists "}

unless ($FORM{'file'} =~ /^[a-z0-9_]+$/){$error.="filename "}
if (length($FORM{'file'})>20){$error.="filelength "}

if ($error){print "Content-type: text/html\n\n";print "$body\n\n$tag\n\n";goto NEW_SHELL}


@shell="<HTML>
<HEAD>
<TITLE></TITLE>
</HEAD>
<BODY>


<!-- #voting# -->


</BODY>
</HTML>";


if (&lock("$data_dir/shells/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,">$data_dir/shells/$FORM{'file'}.txt";
print FILE @shell;
close FILE;
if (&unlock("$data_dir/shells/$FORM{'file'}.txt"))
{print "$error_message";exit}

chmod(0755,"$data_dir/shells/$FORM{'file'}.txt");

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=edit_shell&file=$FORM{'file'}\n\n";

exit;


###################################################
# форма редагування голосування                   #
###################################################
EDIT:

if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$FORM{'file'}.txt";
@fil=<FILE>;
close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
chomp (@fil);

for $i(10..$#fil){
($row[$i-10],$number[$i-10])=split /\|`\|/,$fil[$i]
}


EDIT_1:

for $i(0..$#fil){
$fil[$i]=~s/\"/&quot;/g;
$fil[$i]=~s/\</&lt;/g;
$fil[$i]=~s/\>/&gt;/g;
}

for $i(0..$#row){
$row[$i]=~s/\"/&quot;/g;
$row[$i]=~s/\</&lt;/g;
$row[$i]=~s/\>/&gt;/g;
}

($tag_title_open,$tag_title_close,$tag_system_open,$tag_system_close)=split/\|`\|/,$fil[0];
($tag_question_open,$tag_question_close)=split/\|`\|/,$fil[1];
($close_ip,$close_ip_time)=split/\|`\|/,$fil[5];
($show_result,$sys_lang,$sort,$url_button,$shell,$shell_on_form,$shell_on_submit,$shell_on_result)=split/\|`\|/,$fil[6];

menu();



print "<script language=\"JavaScript\">\n";
print "<!--\n";

print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n\n";


if ($FORM{'file'} eq "template"){
print "function templateDefault(){\n";
print "document.edit_form.tag_system_open.value='<font face=\"arial\" size=\"2\"><b>';\n";
print "document.edit_form.tag_system_close.value='</b></font>';\n";
print "document.edit_form.tag_title_open.value='<font face=\"arial\" size=\"2\"><b>';\n";
print "document.edit_form.tag_title_close.value='</b></font>';\n";
print "document.edit_form.tag_question_open.value='<font face=\"arial\" size=\"1\"><b>';\n";
print "document.edit_form.tag_question_close.value='</b></font>';\n";
print "document.edit_form.width.value='150';\n";
print "document.edit_form.height.value='10';\n";
print "document.edit_form.url_button.value='';\n";
print "document.edit_form.submit_text.value='Ответить';\n";
print "document.edit_form.close_ip[0].click();\n";
print "document.edit_form.show_result[0].click();\n";
print "document.edit_form.sys_lang[0].click();\n";
print "document.edit_form.sort[1].click();\n";
print "document.edit_form.shell[0].click();\n";
print "document.edit_form.close_ip_time.value='0';\n";
print "document.edit_form.url_to_image.value='http://www.lyceum1.cv.ua/tmp/tigvote/img/\n";
print "document.edit_form.tag_body.value='<BODY background=\"\" bgcolor=\"#ffffff\" text=\"#000000\" link=\"#0000ff\" vlink=\"#800080\" alink=\"#ff0000\"><center>';\n";
print "}\n\n";
}

print "// -->\n";
print "</script>\n";




print "$tag<font size=3>Редагування ";
if ($FORM{'file'} eq "template"){print "шаблону"}
else {print "голосування '$FORM{'file'}'&nbsp;&nbsp;&nbsp;<a href=\"javascript:open_new_window('$help_url/edit_vote.html',500,400)\"><img src=$help_url/help.gif border=0></a>"}
print "</font><br><br>\n";

if ($FORM{'file'} ne "template"){
print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=form_check&file=$FORM{'file'}',550,400)\">голосування</A> &lt;&lt; Зовнішній вигляд &gt;&gt; <a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=jresult&file=$FORM{'file'}',550,400)\">результатів</A>\n";
print " | <a href=tv-adm.cgi?action=vote-on-page&file=$FORM{'file'}>Як помістити голосування '$FORM{'file'}' на сторінку</a>";
print "</td></tr></table>\n\n";
}


#построение формы
print "<form action=tv-adm.cgi method=POST name=\"edit_form\">\n";
print "<input type=hidden name=action value=edit_data>\n";
print "<input type=hidden name=file value=$FORM{'file'}>\n";

if ($FORM{'save'} eq "ok"){print "<font color=red>зміни збережені</font>\n"}


print "<table border=1 cellspacing=0>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/url_to_image.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>URL картинок для графіку:</font><br><input size=47 type=text name=url_to_image value=\"$fil[7]\">";
if ($error=~/url_to_image/){print "<br><font color=red size=1>це поле повинне бути заповнине</font>\n";}
print "</td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/width.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<input size=5 type=text name=width value=\"$fil[2]\"><font size=1> довжина максимальної лінії графіку";
if ($error=~/width/){print "<br><font color=red size=1>перевірте правильність вводу довжини</font>\n";}
print "</td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/height.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<input size=5 type=text name=height value=\"$fil[3]\"><font size=1> ширина линій графіку";
if ($error=~/height/){print "<br><font color=red size=1>перевірте правильність вводу ширини</font>\n";}
print "</td></tr>\n";


print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/url_button.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>URL картинки для кнопки голосування (не обов’язковий параметр)</font><br><input size=47 type=text name=url_button value=\"$url_button\">";
if ($error=~/url_button/){print "<br><font color=red size=1>перевірте правильність введення URL</font>\n";}
print "</td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/submit_text.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Напис на кнопці голосування:</font><br><input size=47 type=text name=submit_text value=\"$fil[4]\">";
if ($error=~/submit_text/){print "<br><font color=red size=1>це поле повинне бути заповнине</font>\n";}
print "</td></tr>\n";


# мова системних повідомлень
print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/sys_lang.html',500,290)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Мова системних повідомлень:</font><br>";

$no_lang=0;
if (!open (FILE,"<$data_dir/languages.txt")){
print "<font color=red size=1>Файл $data_dir/languages.txt не знайдено!<br>По замовчунню буде використовуватися англійска мова.</font><br>\n";
print "<select name=sys_lang>\n";
print "<option value=eng>English";
print "</select>\n";
}
else {
@languages=<FILE>;
close FILE;
chomp (@languages);

print "<select name=sys_lang>\n";

for $i(0..$#languages){
if ($languages[$i]=~/^::/){

($temp,$lang_name,$lang_abb)=split/::/,$languages[$i];

print "<option value=$lang_abb";
if ($sys_lang eq $lang_abb){print " selected"}
print ">$lang_name\n";

}
}

print "</select>\n";
}


print "</td></tr>\n";
#########################

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/close_ip.html',500,280)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Заборонити повторне голосування с одного IP адресу?</font><br>";
if ($close_ip eq 'yes'){print "<input type=radio name=close_ip value=yes checked> Так <input type=radio name=close_ip value=no> Ні"}
else {print "<input type=radio name=close_ip value=yes> Так <input type=radio name=close_ip value=no checked> Ні"}
print "<br><font size=1>затримка, після якої можно голосувати повторно.<br>при 0 - повторно голосувати неможна.<br>(працює при включенній опції заборони повторних голосувань)<br>\n";
print "<input size=7 type=text name=close_ip_time value=\"$close_ip_time\"> хв.";
print "</td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/show_result.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Показувати результати голосування користувачам?</font><br>";
if ($show_result eq 'yes'){print "<input type=radio name=show_result value=yes checked> Так <input type=radio name=show_result value=no> Ні"}
else {print "<input type=radio name=show_result value=yes> Так <input type=radio name=show_result value=no checked> Ні"}
print "</td></tr>\n";



print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/sort.html',500,360)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Сортування результатів:</font><br>";
print "<input type=radio name=sort value=none";
if (($sort eq "none") || !$sort){print " checked"}
print "> не сортувати<br>\n";
print "<input type=radio name=sort value=vote";
if ($sort eq "vote"){print " checked"}
print "> к-сть голосів по спаданню<br>\n";
print "<input type=radio name=sort value=vote-reverse";
if ($sort eq "vote-reverse"){print " checked"}
print "> к-сть голосів по зростанню<br>\n";
print "<input type=radio name=sort value=point";
if ($sort eq "point"){print " checked"}
print "> пункти в алфавітному порядку<br>\n";
print "<input type=radio name=sort value=point-reverse";
if ($sort eq "point-reverse"){print " checked"}
print "> пункти в порядку, протилежному алфавітному<br>\n";
print "</td></tr>\n";



# підключення html-оболонки
print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/shell.html',500,380)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>html-оболонка: </font>";

print "<select name=shell>\n";
print "<option value=\"\"";
unless ($shell){print " selected"}
print ">не підключати\n";

opendir (DIR, "$data_dir/shells");
@shells=readdir (DIR);
closedir (DIR);
shift(@shells);shift(@shells);
@shells=sort(@shells);

for $i(0..$#shells){
$shells[$i]=~s/.txt//;
print "<option value=\"$shells[$i]\"";
if ($shell eq $shells[$i]){print " selected"}
print ">$shells[$i]\n";
}
print "</select>\n";

print "<br><font size=1>підключати html-оболонку: </font><br>\n";
print "<input type=checkbox name=shell_on_form value=1";
if ($shell_on_form){print " checked"}
print "> в формі голосування<br>\n";
print "<input type=checkbox name=shell_on_submit value=1";
if ($shell_on_submit){print " checked"}
print "> після нажаття кнопки \"submit\"<br>\n";
print "<input type=checkbox name=shell_on_result value=1";
if ($shell_on_result){print " checked"}
print "> у результатах голосування\n";
print "</td></tr>\n";
################################



print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/tag_body.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Тег BODY</font><br><input size=47 type=text name=tag_body value=\"$fil[8]\"></td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/tag_system.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Теги системних повідомлень (ваш голос прийнятий, закрити вікно і т.д.)<br>відкриваючі:<br><input size=47 type=text name=tag_system_open value=\"$tag_system_open\"><br>";
print "закриваючі:<br></font><input size=47 type=text name=tag_system_close value=\"$tag_system_close\"></td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/tag_title.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Теги заголовка голосування<br>открывающие:<br><input size=47 type=text name=tag_title_open value=\"$tag_title_open\"><br>";
print "закриваючі:<br></font><input size=47 type=text name=tag_title_close value=\"$tag_title_close\"></td></tr>\n";

print "<tr><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/tag_question.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Теги питань голосування<br>відкриваючі:<br><input size=47 type=text name=tag_question_open value=\"$tag_question_open\"><br>";
print "закриваючі:<br></font><input size=47 type=text name=tag_question_close value=\"$tag_question_close\"></td></tr>\n";

if ($FORM{'file'} ne "template"){
print "<tr bgcolor=#bfbfcf><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/title.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td>$tag<font size=1>Заголовок голосування:</font><br><input size=47 type=text name=title value=\"$fil[9]\">";
if ($error=~/title/){print "<br><font color=red size=1>це поле повинне бути заповнине</font>\n";}
print "</td></tr>\n";

print "<tr bgcolor=#bfbfcf><td valign=center align=center><a href=\"javascript:open_new_window('$help_url/row.html',500,240)\"><img src=$help_url/help.gif border=0></a></td><td><font face=arial size=1><b>Пункти голосування:<br>(для знищення пункту поставте галочку)</td></tr>\n\n";

for $i(0..$#row){
print "<tr bgcolor=#bfbfcf><td><input type=checkbox name=del-row value=$i";
if ($del_row[$i]){print " checked"}
print "></td><td>$tag<input type=text size=40 name=row value=\"$row[$i]\"><input type=text size=5 name=number value=\"$number[$i]\"></td></tr>\n";
}
}

print "\n<tr><td colspan=2 align=center>${tag}<input type=\"submit\" value=\"Зберегти\"> &lt;&lt; Зміни &gt;&gt; <input type=\"reset\" value=\"Відмінити\"></td></tr>\n";

print "</table>\n";
print "</form>\n";


if ($FORM{'file'} ne "template"){
print "<form action=tv-adm.cgi method=POST>\n";
print "<input type=hidden name=action value=add>";
print "<input type=hidden name=file value=$FORM{'file'}>";

print "<font size=1 color=\"\#af3030\">Перед додаванням нового пункту збережіть зміни.</font><br>";
print "<table><tr><td>$tag<input type=submit value=\"Додати пункт\">\n";
print "<select name=num>\n";
print "<option value=1 selected>1\n";
print "<option value=2>2\n";
print "<option value=3>3\n";
print "<option value=4>4\n";
print "<option value=5>5\n";
print "<option value=6>6\n";
print "<option value=7>7\n";
print "<option value=8>8\n";
print "<option value=9>9\n";
print "<option value=10>10\n";
print "<select>\n";
print "</td></tr></table>\n";
print "</form>";

}
else {print "<input type=submit value=\"настройки шаблону\nпо замовчуванню\" onClick=\"templateDefault(); return false;\">\n<br><br>\n"}


down();

exit;




###################################################
# форма редагування html-оболонки                 #
###################################################
EDIT_SHELL:

open (FILE,"<$data_dir/shells/$FORM{'file'}.txt") || &Error("Помилка відкриття файлу $data_dir/shells/$FORM{'file'}.txt, помилка $!");
@fil=<FILE>;
close FILE;
chomp (@fil);


EDIT_1:

$found=0;
for $i(0..$#fil){
if ($fil[$i] eq "<!-- #voting# -->"){$found=1;next}
$fil[$i]=~s/&/&amp;/g;
$fil[$i]=~s/\"/&quot;/g;
$fil[$i]=~s/\</&lt;/g;
$fil[$i]=~s/\>/&gt;/g;
unless ($found){push(@header,$fil[$i])}
else {{push(@footer,$fil[$i])}}
}


print "<script language=\"JavaScript\">\n";
print "<!--\n";

print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n\n";

print "// -->\n";
print "</script>\n";


menu();


print "$tag<a href=\"javascript:open_new_window('$help_url/edit_shell.html',500,520)\"><img src=$help_url/help.gif border=0></a>&nbsp;&nbsp;&nbsp;&nbsp;";
print "<font size=3>Редагування ";
print "html-оболонки '$FORM{'file'}'";
print "</font><br><br>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=\"tv-adm.cgi?action=show_shell&file=$FORM{'file'}\" target=_blank>зовнішній вигляд html-оболонки</a>\n";
print "</td></tr></table>\n\n";


#побудова форми
print "<form action=tv-adm.cgi method=POST name=\"edit_form\">\n";
print "<input type=hidden name=action value=edit_shell_data>\n";
print "<input type=hidden name=file value=$FORM{'file'}>\n";

if ($FORM{'save'} eq "ok"){print "<font color=red>зміни збережені</font>\n"}

print "<table border=0 cellspacing=0>\n";

print "<tr><td>${tag}Html-код, який знаходиться до голосування:<br>\n";
print "<textarea name=header cols=80 rows=15>\n";

for $i(0..($#header-1)){print "$header[$i]\n";}
print "$header[$#header]";

print "</textarea>\n";
print "</td></tr>\n";


print "<tr><td align=center>$tag<br>&lt;голосування&gt;<br><br></td></tr>\n";


print "<tr><td>${tag}Html-код, який знаходиться після голосування:<br>\n";
print "<textarea name=footer cols=80 rows=15>\n";

for $i(0..($#footer-1)){print "$footer[$i]\n";}
print "$footer[$#footer]";

print "</textarea>\n";
print "</td></tr>\n";


print "\n<tr><td align=center>${tag}<input type=\"submit\" value=\"Зберегти\"> &lt;&lt; Зміни &gt;&gt; <input type=\"reset\" value=\"Відмінити\"></td></tr>\n";

print "</table>\n";
print "</form>\n";



down();

exit;



###################################################
# зовнішній вигляд html-оболонки                  #
###################################################
SHOW_SHELL:

open (FILE,"<$data_dir/shells/$FORM{'file'}.txt")  || &Error("Помилка відкриття файлу $file_name $data_dir/shells/$FORM{'file'}.txt, помилка $!");
@fil=<FILE>;
close FILE;
chomp (@fil);

print "Content-type: text/html\n\n";

for $i(0..$#fil){
if ($fil[$i] eq "<!-- #voting# -->"){
$fil[$i]="<table border=1 bgcolor=#999999 cellspacing=0 cellpadding=20>\n<tr><td>\n<b>голосування\n</td></tr>\n</table>"
}
print "$fil[$i]\n";
}

exit;




###################################################
# обробка даних редагування голосування           #
###################################################
EDIT_DATA:

$fil[0]="$FORM{'tag_title_open'}|`|$FORM{'tag_title_close'}|`|$FORM{'tag_system_open'}|`|$FORM{'tag_system_close'}\n";
$fil[1]="$FORM{'tag_question_open'}|`|$FORM{'tag_question_close'}\n";
$fil[2]="$FORM{'width'}\n";
$fil[3]="$FORM{'height'}\n";
$fil[4]="$FORM{'submit_text'}\n";
$fil[5]="$FORM{'close_ip'}|`|$FORM{'close_ip_time'}\n";
$fil[6]="$FORM{'show_result'}|`|$FORM{'sys_lang'}|`|$FORM{'sort'}|`|$FORM{'url_button'}|`|$FORM{'shell'}|`|$FORM{'shell_on_form'}|`|$FORM{'shell_on_submit'}|`|$FORM{'shell_on_result'}\n";
$fil[7]="$FORM{'url_to_image'}\n";
$fil[8]="$FORM{'tag_body'}\n";
$fil[9]="$FORM{'title'}\n";

$error="";

unless ($FORM{'width'} =~ /^[\d]+$/){$error.="width "}
unless ($FORM{'height'} =~ /^[\d]+$/){$error.="height "}
unless (!$FORM{'url_button'} || $FORM{'url_button'}=~/(\.gif|\.jpg|\.jpeg)$/){$error.="url_button "}
unless ($FORM{'submit_text'}){$error.="submit_text "}
unless ($FORM{'url_to_image'}){$error.="url_to_image "}
if ($FORM{'file'} ne "template"){
unless ($FORM{'title'}){$error.="title "}
}

if ($error){chomp (@fil);print "Content-type: text/html\n\n";print "$body\n\n$tag\n\n";goto EDIT_1}

if ($FORM{'file'} ne "template"){
for $i(0..$#row){unless($del_row[$i]){push(@fil,"$row[$i]|`|$number[$i]\n")}}
}
else {$fil[9]="Хочете створити нове голосування?\nТак|`|0\nНі|`|0\n"}
for $i(0..$#fil){$fil[$i]=~s/&quot;/\"/g}


if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,">$data_dir/vote/$FORM{'file'}.txt";
print FILE @fil;
close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}

chmod(0755,"$data_dir/vote/$FORM{'file'}.txt");

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=edit&file=$FORM{'file'}&save=ok\n\n";

exit;



###################################################
# обробока даних редагування html-оболонки        #
###################################################
EDIT_SHELL_DATA:


if (&lock("$data_dir/shells/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,">$data_dir/shells/$FORM{'file'}.txt";
print FILE "$FORM{'header'}\n<!-- #voting# -->\n$FORM{'footer'}";
close FILE;
if (&unlock("$data_dir/shells/$FORM{'file'}.txt"))
{print "$error_message";exit}

chmod(0755,"$data_dir/shells/$FORM{'file'}.txt");

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=edit_shell&file=$FORM{'file'}&save=ok\n\n";

exit;


###################################################
# додавання пунктів в голосування                 #
###################################################
ADD:

if ($FORM{'num'}<1 || $FORM{'num'}>10){print "Content-type: text/html\n";print "Location: tv-adm.cgi?action=edit&file=$FORM{'file'}\n\n";}

if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,">>$data_dir/vote/$FORM{'file'}.txt";

for $i(1..$FORM{'num'}){
print FILE "новий пункт|`|0\n";
}

close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=edit&file=$FORM{'file'}\n\n";

exit;


###################################################
# видалення файлів                                #
###################################################
DELETE:

for $i(0..$#del_file){unlink ("$data_dir/vote/$del_file[$i].txt")}

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=start\n\n";

exit;


###################################################
# видалення html-оболонки                          #
###################################################
DELETE_SHELL:

for $i(0..$#del_file){unlink ("$data_dir/shells/$del_file[$i].txt")}

print "Content-type: text/html\n";
print "Location: tv-adm.cgi?action=start\n\n";

exit;


###################################################
# HTML-код голосування                            #
###################################################
VOTE_ON_PAGE:

if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$FORM{'file'}.txt";
@fil=<FILE>;
close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
chomp (@fil);

($tag_title_open,$tag_title_close,$tag_system_open,$tag_system_close)=split/\|`\|/,$fil[0];
($tag_question_open,$tag_question_close)=split/\|`\|/,$fil[1];
$submitText=$fil[4];
($close_ip,$close_ip_time)=split/\|`\|/,$fil[5];
($show_result,$sys_lang,$sort,$url_button,$shell,$shell_on_form,$shell_on_submit,$shell_on_result)=split/\|`\|/,$fil[6];


$form_text="<!-- Lyceum voting start -->
<form action=\"".$cgiUrl."/tigvote.cgi\" method=\"POST\">
<input type=\"hidden\" name=\"action\" value=\"submit\">
<input type=\"hidden\" name=\"file\" value=\"$FORM{'file'}\">
<table border=\"0\">
<tr><td>$tag_title_open$fil[9]$tag_title_close</td></tr>
";

for $i(10..$#fil){
($question)=split /\|`\|/,$fil[$i];
$form_text.="<tr><td><input type=\"radio\" name=\"tigvote\" value=\"".($i-10)."\">$tag_question_open$question$tag_question_close</td></tr>\n";
}

if ($url_button){$form_text.="<tr><td><input type=image src=\"$url_button\" alt=\"$submitText\" border=0></td></tr>\n";}
else {$form_text.="<tr><td><input type=\"submit\" value=\"$submitText\"></td></tr>\n";}
$form_text.="</table>\n";
$form_text.="</form>\n";
$form_text.="<!-- Lyceum voting end -->\n\n";

$check_text=$form_text;
$check_text=~s/<input type=\"radio\"/<input type=\"checkbox\"/g;


menu();
print "$tag<font size=3>\nЯк помістити голосування на сторінку</font><br><br>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?action=edit&file=$FORM{'file'}>Повернутися до редагування</a>\n";
print "</td></tr></table>\n\n";

print "<form>\n";
print "<table border=0 width=650><tr><td>\n";

print "$tag<div align=center><font size=3>Форма голосування</font></div><br>\n";


#radio
print "<div align=center><font size=3><a name=\"radio\">Radiobutton</a> (<input type=radio>) - вибір однієї відповіді</font></div><br>\n";
print "Спосіб №1: щоб голосування знаходилось безпосередньо на вашій сторінці, вставте в неї наступний html-код:<br>\n";

print "<font size=1>Форма голосування:</font><br>";
print "<textarea name=form-form cols=80 rows=15>\n";
print $form_text;
print "</textarea><br><br>\n";

print "Спосіб №2: можна зробити так, щоб голосування відкривалось в окремому маленькому вікні. Для цього вставте в вашу сторінку наступиний код:<br>\n";
print "<textarea name=java-form cols=80 rows=8>\n";
print "<!-- Lyceum voting start -->\n";

print "<script language=\"JavaScript\">\n";
print "<!--\n";
print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n";
print "// -->\n";
print "</script>\n";

print "<a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=form&file=$FORM{'file'}',550,400)\">$fil[9]</а>\n";
print "<br>\n";
print "<!-- Lyceum voting end -->\n";

print "</textarea><br><br>\n";

print "Спосіб №3: Якщо ваш сервер підтримує виконання команд SSI, то вам потрібно вставити в сторінку наступний код:<br>\n";
print "<textarea name=java-form cols=80 rows=3>\n";
print "<!-- Lyceum voting start -->\n";
print "<!--#include virtual=\"/шлях/до/скрипту/tigvote.cgi?action=form&file=$FORM{'file'}\"-->\n";
print "<!-- Lyceum voting end -->\n";
print "</textarea><br><br><hr>\n";
################

#checkbox
print "$tag<div align=center><font size=3><a name=\"check\">Checkbox (<input type=checkbox>) - вибір декількох відповідей</font></div><br>";
print "Спосіб №1: щоб голосування знаходилось безпосередньо на вашій сторінці, вставте в неї наступний html-код:<br>\n";

print "<font size=1>Форма голосування:</font><br>";
print "<textarea name=form-form cols=80 rows=15>\n";
print $check_text;
print "</textarea><br><br>\n";

print "Спосіб №2: можна зробити так, щоб голосування відкривалось в окремому маленькому вікні. Для цього вставте в вашу сторінку наступиний код:<br>\n";
print "<textarea name=java-form cols=80 rows=8>\n";
print "<!-- Lyceum voting start -->\n";

print "<script language=\"JavaScript\">\n";
print "<!--\n";
print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n";
print "// -->\n";
print "</script>\n";

print "<a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=form_check&file=$FORM{'file'}',550,400)\">$fil[9]</а>\n";
print "<br>\n";
print "<!-- Lyceum voting end -->\n";

print "</textarea><br><br>\n";

print "Спосіб №3: Якщо ваш сервер підтримує виконання команд SSI, то вам потрібно вставити в сторінку наступний код:<br>\n";
print "<textarea name=java-form cols=80 rows=3>\n";
print "<!-- Lyceum voting start -->\n";
print "<!--#include virtual=\"/шлях/до/скрипту/tigvote.cgi?action=form_check&file=$FORM{'file'}\"-->\n";
print "<!-- Lyceum voting end -->\n";

print "</textarea><br><br><hr>\n";
#############

#select
print "$tag<div align=center><font size=3><a name=\"select\">Select (<select>\n<option vaue=0>да\n<option vaue=0>нет\n</select>\n) - выпадающее меню с вариантами ответов</font></div><br>";
print "Спосіб №1: щоб голосування знаходилось безпосередньо на вашій сторінці, вставте в неї наступний html-код:<br>\n";

print "<font size=1>Форма голосування:</font><br>";
print "<textarea name=form-form cols=80 rows=15>\n";

print "<!-- Lyceum voting start -->
<form action=\"".$cgiUrl."/tigvote.cgi\" method=\"POST\">
<input type=\"hidden\" name=\"action\" value=\"submit\">
<input type=\"hidden\" name=\"file\" value=\"$FORM{'file'}\">
<table border=\"0\">
<tr><td>$tag_title_open$fil[9]$tag_title_close</td></tr>
";

print "<tr><td>\n";
print "$tag_question_open\n";
print "<select name=tigvote>\n";
for $i(10..$#fil){
($question)=split /\|`\|/,$fil[$i];
print "<option value=".($i-10).">$question\n";
}
print "</select>\n";
print "$tag_question_close\n";
print "</td></tr>\n";


if ($url_button){print "<tr><td><input type=image src=\"$url_button\" alt=\"$submitText\" border=0></td></tr>\n";}
else {print "<tr><td><input type=\"submit\" value=\"$submitText\"></td></tr>\n";}
print "</table>\n";
print "</form>\n";
print "<!-- Lyceum voting end -->";


print "</textarea><br><br>\n";

print "Спосіб №2: можна зробити так, щоб голосування відкривалось в окремому маленькому вікні. Для цього вставте в вашу сторінку наступиний код:<br>\n";
print "<textarea name=java-form cols=80 rows=8>\n";
print "<!-- Lyceum voting start -->\n";

print "<script language=\"JavaScript\">\n";
print "<!--\n";
print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n";
print "// -->\n";
print "</script>\n";

print "<a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=form_select&file=$FORM{'file'}',550,400)\">$fil[9]</а>\n";
print "<br>\n";
print "<!-- Lyceum voting end -->";

print "</textarea><br><br>\n";

print "Спосіб №3: Якщо ваш сервер підтримує виконання команд SSI, то вам потрібно вставити в сторінку наступний код:<br>\n";
print "<textarea name=java-form cols=80 rows=3>\n";
print "<!-- Lyceum voting start -->\n";
print "<!--#include virtual=\"/шлях/до/скрипту/tigvote.cgi?action=form_select&file=$FORM{'file'}\"-->\n";
print "<!-- Lyceum voting end -->";

print "</textarea><br><br><hr>\n";
###########




print "$tag<div align=center><font size=3>Результати голосування</font></div><br>\n";

print "Ссилка на показ результатів:<br><font color=red size=1>Якщо Ви хочете показати результати зразу декількох голосувань, перерахуйте їх імена через кому (без пробілів) після параметра &quot;file=&quot;</font></font><br>";
print "<textarea name=form-result cols=80 rows=4>\n";
print "<!-- Lyceum voting start -->\n";
print "<a href=\"".$cgiUrl."/tigvote.cgi?action=result&file=$FORM{'file'}\">Проглянути результати голосування</a>\n";
print "<!-- Lyceum voting end -->\n";
print "</textarea><br><br>\n";

print "Результати відкриваються у окремому маленькому вікні.<br>\n";
print "<font size=1 color=red>Якщо Ви хочете показати результати зразу декількох голосувань, перерахуйте їх імена через кому (без пробілів) в &quot;voteOpen('jresult','$fName')&quot;</font><br>";
print "<textarea name=java-form cols=80 rows=8>\n";
print "<!-- Lyceum voting start -->\n";

print "<script language=\"JavaScript\">\n";
print "<!--\n";
print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n";
print "// -->\n";
print "</script>\n";

print "<a href=\"javascript:open_new_window('$cgiUrl/tigvote.cgi?action=jresult&file=$FORM{'file'}',550,400)\">Результати голосування '$fil[9]'</a>\n\n";
print "<!-- Lyceum voting end -->\n";

print "</textarea><br><br>\n";


print "Якщо ваш сервер підтримує виконання команд SSI, то результати можна вставити в сторінку:<br>\n";
print "<font size=1 color=red>Якщо Ви хочете показати результати зразу декількох голосувань, перерахуйте їх імена через кому (без пробілів) після параметра \"file=\"</font><br>";
print "<textarea name=java-form cols=80 rows=3>\n";
print "<!-- Lyceum voting start -->\n";
print "<!--#include virtual=\"/шлях/до/скрипту/tigvote.cgi?action=result&file=$FORM{'file'}\"-->\n";
print "<!-- Lyceum voting end -->\n";
print "</textarea><br>\n";


print "</td></tr></table>\n</form>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?action=edit&file=$FORM{'file'}>Повернутися до редагування</a>\n";
print "</td></tr></table><br>\n\n";

down();

exit;


###################################################
# перегляд ip-адрес                               #
###################################################
VIEW:

if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$FORM{'file'}.txt";
@fil=<FILE>;
close FILE;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
chomp (@fil);

menu();
print "$tag\n<br>Перегляд файлу '$FORM{'file'}'</font><br><br>\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?$query>Обновити</a>";
print "</td></tr></table>\n\n";

print "<table border=0 cellspacing=0>\n";

for $i(0..$#fil){
($ip,$time)=split/:/,$fil[$i];
print "<tr><td>$tag$ip</td></tr>";
}

print "</table>\n\n";

print "<table border=0 width=80%><tr bgcolor=\#cfcfdf><td align=center>$tag\n";
print "<a href=tv-adm.cgi?$query>Обновити</a>";
print "</td></tr></table><br>\n\n";

down();

exit;



###################################################
# перегляд логу                                   #
###################################################
VIEW_LOG:

if (&lock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
open LOG,"<$data_dir/vote/$FORM{'file'}.txt";
@fil=<LOG>;
close LOG;
if (&unlock("$data_dir/vote/$FORM{'file'}.txt"))
{print "$error_message";exit}
chomp(@fil);

@fil=reverse @fil;

unless ($FORM{'filter'}){@log=@fil}
else {

for $i(0..$#fil){
($day,$month,$year,$wday,$hour,$min,$sec,$ip,$host,$deistvie,$punkt)=split/=/,$fil[$i];

# фільтри
# день
if ($FORM{'filter'} eq "day"){
if (($day==$FORM{'day'}) && ($month==$FORM{'month'}) && ($year==$FORM{'year'})){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: число ($FORM{'day'}.$FORM{'month'}.$FORM{'year'})<br>";
}
#місяц
elsif ($FORM{'filter'} eq "month"){
if (($month==$FORM{'month'}) && ($year==$FORM{'year'})){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: місяц (xx.$FORM{'month'}.$FORM{'year'})<br>";
}
#рік
elsif ($FORM{'filter'} eq "year"){
if ($year==$FORM{'year'}){
push (@log,$fil[$i]);
}
$filt_desc="Фильтр: рік (xx.xx.$FORM{'year'})<br>";
}
#година
elsif ($FORM{'filter'} eq "hour"){
if (($hour==$FORM{'hour'}) && ($day==$FORM{'day'}) && ($month==$FORM{'month'}) && ($year==$FORM{'year'})){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: година ($FORM{'day'}.$FORM{'month'}.$FORM{'year'} $FORM{'hour'} годин)<br>";
}
#хвилина
elsif ($FORM{'filter'} eq "min"){
if (($min==$FORM{'min'}) && ($hour==$FORM{'hour'}) && ($day==$FORM{'day'}) && ($month==$FORM{'month'}) && ($year==$FORM{'year'})){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: хвилина ($FORM{'day'}.$FORM{'month'}.$FORM{'year'} $FORM{'hour'}:$FORM{'min'} хвилин)<br>";
}
#секунда
elsif ($FORM{'filter'} eq "sec"){
if (($sec==$FORM{'sec'}) && ($min==$FORM{'min'}) && ($hour==$FORM{'hour'}) && ($day==$FORM{'day'}) && ($month==$FORM{'month'}) && ($year==$FORM{'year'})){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: секунда ($FORM{'day'}.$FORM{'month'}.$FORM{'year'} $FORM{'hour'}:$FORM{'min'}.$FORM{'sec'} секунд)<br>";
}
#ip
elsif ($FORM{'filter'} eq "ip"){
if ($ip==$FORM{'ip'}){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: ip ($FORM{'ip'})<br>";
}
#дія
elsif ($FORM{'filter'} eq "deist"){
if ($deistvie==$FORM{'deist'}){
push (@log,$fil[$i]);
}
$filt_desc="Фільтр: дії (";
if ($FORM{'deist'} eq '1'){$filt_desc.="вибраний(і) пункт(и)"}
elsif ($FORM{'deist'} eq '2'){$filt_desc.="додатий пункт"}
elsif ($FORM{'deist'} eq '3'){$filt_desc.="вже голосував. выбраний(і) пункт(и)"}
$filt_desc.=")<br>";
}

}
}

print "<script language=\"JavaScript\">\n";
print "<!--\n";

print "function open_new_window(url,width,height)\n";
print "{\n";
print "windowVar=window.open(url,\"\", \"width=\"+width+\",height=\"+height+\",status=no,toolbar=no,menubar=no,directories=no,location=no,resizable=yes,scrollbars=yes\");\n";
print "}\n\n";

print "// -->\n";
print "</script>\n";


menu();

print "$tagПерегляд лог-Файлу: '$FORM{'file'}'&nbsp;&nbsp;&nbsp;<a href=\"javascript:open_new_window('$help_url/log_file.html',500,400)\"><img src=$help_url/help.gif border=0></a><br><br>";
print $filt_desc;


$numLines=$#log;
$numLines++;
$numscreen=int($numLines/$lines);
$num=$numLines/$lines;
if ($num!=$numscreen){$numscreen++;}

if ($page<0){$page=0}
if ($page>$numscreen){$page=$numscreen-1}

$start=$page*$lines;
$end=$start+$lines-1;
if ($end>$#log){$end=$#log}


# навігація по сторінках
print "<table border=0 bgcolor=\#cfcfdf width=80%>\n";
print "<tr height=25>\n";
print "<td align=center>\n<font size=-1><b>\n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=$page>Обновити</a><br>";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=0>&lt;&lt;&nbsp;</a> \n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=";
if (($page-1)<0){print "0"}
else {print ($page-1)}
print ">&lt;&nbsp;</a> \n";

for $i(1..$numscreen){
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=".($i-1).">";
if (($i-1)==$page){print "<font color=red>$i</font>"}
else {print "$i"}
print "</a> ";
}
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=";
if (($page+1)>=$numscreen){print ($numscreen-1)}
else {print ($page+1)}
print ">&nbsp;&gt;</a> \n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=".($numscreen-1).">&nbsp;&gt;&gt;</a>\n";
print "</td>\n";
print "</tr>\n";
print "</table>\n";
############


print "<table cellpadding=3 cellspacing=0 border=1>\n";

for $i($start..$end)
{

($day,$month,$year,$wday,$hour,$min,$sec,$ip,$host,$deistvie,$punkt)=split/=/,$log[$i];

if ($deistvie eq '1'){$deist="<font color=green>выбраний(і) пункт(и)</font>";}
else {if ($deistvie eq '2'){$deist="<font color=blue>додатий пункт</font>";}
else {if ($deistvie eq '3'){$deist="<font color=red>Вже голосував. выбраний(і) пункт(и)</font>";}
else {$deist="помилка!";}}}

print "<tr>\n<td align=right>$tag".($#log-$i+1)."</td><td>$tag";
print "<a href=tv-adm.cgi?action=viewlog&filter=day&file=$FORM{'file'}&page=$page&day=$day&month=$month&year=$year>$day</a>.";
print "<a href=tv-adm.cgi?action=viewlog&filter=month&file=$FORM{'file'}&page=$page&month=$month&year=$year>$month</a>.";
print "<a href=tv-adm.cgi?action=viewlog&filter=year&file=$FORM{'file'}&page=$page&year=$year>$year</a>($wday)<br>";
print "<a href=tv-adm.cgi?action=viewlog&filter=hour&file=$FORM{'file'}&page=$page&day=$day&month=$month&year=$year&hour=$hour>$hour</a>:";
print "<a href=tv-adm.cgi?action=viewlog&filter=min&file=$FORM{'file'}&page=$page&day=$day&month=$month&year=$year&hour=$hour&min=$min>$min</a>.";
print "<a href=tv-adm.cgi?action=viewlog&filter=sec&file=$FORM{'file'}&page=$page&day=$day&month=$month&year=$year&hour=$hour&min=$min&sec=$sec>$sec</a></td>\n";

print "<td>$tag <a href=tv-adm.cgi?action=viewlog&filter=ip&file=$FORM{'file'}&page=$page&ip=$ip>$ip</a><br>$host</td>\n";
print "<td>$tag <a href=tv-adm.cgi?action=viewlog&filter=deist&file=$FORM{'file'}&page=$page&deist=$deistvie>$deist</a><br>$punkt</td>\n</tr>\n";

}
print "</table>";


# навігація по сторінкам
print "<table border=0 bgcolor=\#cfcfdf width=80%>\n";
print "<tr height=25>\n";
print "<td align=center>\n<font size=-1><b>\n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=0>&lt;&lt;&nbsp;</a> \n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=";
if (($page-1)<0){print "0"}
else {print ($page-1)}
print ">&lt;&nbsp;</a> \n";

for $i(1..$numscreen){
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=".($i-1).">";
if (($i-1)==$page){print "<font color=red>$i</font>"}
else {print "$i"}
print "</a> ";
}
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=";
if (($page+1)>=$numscreen){print ($numscreen-1)}
else {print ($page+1)}
print ">&nbsp;&gt;</a> \n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=".($numscreen-1).">&nbsp;&gt;&gt;</a><br>\n";
print "<a href=tv-adm.cgi?action=viewlog&file=$FORM{'file'}&filter=$FORM{'filter'}&day=$FORM{'day'}&month=$FORM{'month'}&year=$FORM{'year'}&hour=$FORM{'hour'}&min=$FORM{'min'}&sec=$FORM{'sec'}&ip=$FORM{'ip'}&deist=$FORM{'deist'}&page=$page>Обновити</a>";
print "</td>\n";
print "</tr>\n";
print "</table>\n";
############


print "<font size=1 color=\"\#af3030\">Записи можна відфільтрувати по даті (день, місяц, рік), часу (година, хвилина, секунда), IP-адрес і по дії.<br>Просто клікіить на потрібному об’єкті.</font><br>";

down();

exit;



###################################################
#                 підпрограми                     #
###################################################
###################################################
# перевірка куків                                 #
###################################################
sub check_cookie(){
$cookie=$ENV{'HTTP_COOKIE'};
@pairs=split /; /,$cookie;

foreach $pair (@pairs) {
($name, $value)=split /=/,$pair;
$cook{$name} = $value;
}

$pass=$cook{'tvadm-pass'};

# якщо пароль не співпадає, то 0
if ($password ne $pass){$user_logged=0;return 0;}
$user_logged=1;
return 1;
}

#################################################
# меню                                          #
#################################################
sub menu(){

print "<table border=0 width=100% cellspacing=0 cellpadding=2>\n";
print "<tr>\n";
print "<td bgcolor=#8697EA align=left width=60%>\n";
print "${tag}\n";
print "<font size=+0,5>Адміністрування голосування на ліцейському сайті</font>\n";
print "</td>\n";

if ($user_logged){
print "<td bgcolor=#C9CAE7 align=right width=40%>\n";
print "${tag}\n";
print "<a href=tv-adm.cgi>Адміністрування голосування</a> | <a href=http://www.lyceum1.cv.ua>Головна</a> | <a href=tv-adm.cgi?action=exit>Вихід</a>&nbsp;\n";
print "</td>\n";
}

print "</tr>\n";
print "</table>\n";

}

#################################################
# кінець сторінки                               #
#################################################
sub down(){

print "<hr size=0>\n";

print "<div align=right><font face=arial size=2><a href=http://www.lyceum1.cv.ua>www.lyceum1.cv.ua</a></font></div>\n\n";

print "</BODY>\n";
print "</HTML>\n";
}

#################################################
# error                                         #
#################################################
sub Error {
my($errortext) = @_;
print "Content-Type: text/html\n\n";
print $errortext;
exit;
}


##################################################################
#
# lock() Version 2.1
# Written by Craig Patchett craig@patchett.com
# Created 16/09/1996 Last Modified 12/05/2000
#
# Функция создает эксклюзивную блокировку для файла.  Блокировка
# работает только если другие программы, пытающиеся получить
# доступ к файлу, также используют эти подпрограммы.
#
# Функция возвращает:
#       0  -  Если блокировка установлена
#       1  -  При ошибке створення $LOCK_DIR/$filename.tmp
#       2  -  Если $filename используется
#       3  -  Если lock-файл не возможно открыть или создать
#
# Глобальные переменные:
#       $error_message  -  информация о возникшей ошибке
#       $NAME_LEN  -  максимальная довжина файла
#       $LOCK_DIR  -  каталог для створення файла блокировки
#       $MAX_WAIT  -  максимальное время ожидания блокировки
#
# Во время работы создаются:
#       $LOCK_DIR/$filename.tmp
#       $LOCK_DIR/$filename.lok (существует только пока файл
#                                заблокирован)
#
##################################################################
sub lock
{  local($filename)=@_;
   local($wait, $lock_pid);
   local($temp_file)="$LOCK_DIR$$.tmp";
   local($lock_file)=$filename;
   $lock_file=~tr/\/\\:.//d;           # видаляємо розділювачі каталогів
   if ($NAME_LEN && ($NAME_LEN < length($lock_file)))
     {  $lock_file=substr($lock_file, -$NAME_LEN);
     }
   $lock_file="$LOCK_DIR$lock_file.lok";
   $error_message='';
       # створення файлу з PID
   if (!open(TEMP, ">$temp_file"))
     {  $error_message="Content-type: text/html\n\n1. Невозможно создать $temp_file ($!).";
        return(1);
     }
   print TEMP $$;
   close(TEMP);
       # Перевірка lock-файлу
   if (-e $lock_file)
     {
   #Очікування, поки файл розблокується (якщо lock-файл існує)
        for ($wait=$MAX_WAIT; $wait; --$wait)
          {  sleep(1);
             last unless -e $lock_file;
          }
     }
   if ((-e $lock_file) && (-M $lock_file < 0))
     {  unlink($temp_file);
        $error_message="Content-type: text/html\n\n2. Файл \"$filename\" в даний момент використовується. Попробуйте ще раз пізніше.";
        return(2);
     }
   else
     {  if (!rename($temp_file, $lock_file))
          {  unlink($temp_file);
             $error_message="Content-type: text/html\n\n3. Неможливо заблокувати файл \"$filename\" ($!).";
             return(3);
          }
       # Перевірка блокування
        if (!open(LOCK, "<$lock_file"))
          {  $error_message="Content-type: text/html\n\n4. Неможливо провірити блокіровку файлу \"$filename\" ($!).";
             return(3);
          }
        $lock_pid=<LOCK>;
        close(LOCK);
        if ($lock_pid ne $$)
          {  $error_message="Content-type: text/html\n\n5. Файл \"$filename\" в даний момент використовується.  Попробуйте ще раз пізніше.";
             return(2);
          }
        else
          { return(0)
          }
     }
}

 ##################################################################
#
# unlock() Version 2.1
# Written by Craig Patchett craig@patchett.com
# Created 16/09/1996 Last Modified 12/05/2000
#
# Разблокирует файл, заблокированный функцией lock()
#
# Возвращает:
#       0  -  Если файл разблокирован
#       1  -  Если нет доступа к lock-файлу
#       2  -  Если файл заблокирован другим процессом
#       3  -  Если невозможно разблокировать файл
#
# Глобальные переменные:
#       $error_message  -  информация о возникшей ошибке
#       $NAME_LEN  -  максимальная довжина файла
#       $LOCK_DIR  -  каталог для створення файла блокировки
#
# Во время работы удаляется $LOCK_DIR/$filename.lok
#
##################################################################

sub unlock 
{  local($filename)=@_;
   local($lock_file)=$filename;
   $lock_file=~tr/\/\\:.//d;          # Видаляємо розділювачі каталогів
   if ($NAME_LEN<length($lock_file))
     {  $lock_file=substr($lock_file, -$NAME_LEN);
     }
   $lock_file="$LOCK_DIR$lock_file.lok";
   $error_message='';
       # Перевірка блокування
   if (!open(LOCK, "<$lock_file"))
     {  $error_message="Content-type: text/html\n\nНемає доступу до заблокованого файлу \"$filename\" ($!).";
        return(1);
     }

   $lock_pid=<LOCK>;
   close(LOCK);
   if ($lock_pid ne $$)
     {  $error_message="Content-type: text/html\n\nФайл \"$filename\" заблокований іншим процесом.";
        return(2);
     }
       #видалення lock-файлу
   if (!unlink($lock_file))
     {  $error_message="Content-type: text/html\n\nНеможливо розблокувати файл \"$filename\" ($!).";
        return(3);
     }
   return(0);
}