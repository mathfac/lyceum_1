#!/usr/bin/perl
#tigvote.cgi

#=============================================================

use CGI::Carp qw(fatalsToBrowser);
require "vars.txt";

#=============================================================

$text[1]="������� ������ �� ���� �������!";
$text[2]="�����������";
$text[3]="������� ��������� �����. ��������� �� ���.";
$text[4]="������. ��� ����� ����������.";
$text[5]="������";
$text[6]="�������";
$text[7]="��� ����� �� ����������, ���i����<br>�� ��� ����������!";



$ip=$ENV{'REMOTE_ADDR'};
if ($ENV{'REQUEST_METHOD'} eq 'GET'){$query=$ENV{'QUERY_STRING'};}
else {if ($ENV{'REQUEST_METHOD'} eq 'POST'){read(STDIN, $query, $ENV{'CONTENT_LENGTH'});}
else {exit;}
}

$query=~tr/;'`\\"|*~<>()[]{}$\n\r//d;
chomp($query);

@pairs=split /&/,$query;
foreach $pair (@pairs){
($name,$value)=split /=/,$pair;
$name=~tr/+/ /;
$name=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value=~tr/+/ /;
$value=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
if ($name eq "tigvote"){$tigvote[$value]=1}
$FORM{$name}=$value;
}
$action=$FORM{'action'};
$FORM{'file'}=~tr/\.\/\\//d;
@files=split /,/,$FORM{'file'};



print "Content-Type: text/html\n\n";

unless (-e "$data_dir/vote/$files[0].txt"){
$pr_page.="���� ����������� �� ��������.<br>\n";
print_page();
exit;
}

getDate();

if (&lock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$files[0].txt";
@fil=<FILE>;
close FILE;
chomp(@fil);

($tag_title_open,$tag_title_close,$tag_system_open,$tag_system_close)=split/\|`\|/,$fil[0];
($tag_question_open,$tag_question_close)=split/\|`\|/,$fil[1];

$graphLenght=$fil[2];
$graphWidth=$fil[3];
$submitText=$fil[4];
($close_ip,$close_ip_time)=split/\|`\|/,$fil[5];
($showResult,$sys_lang,$sort,$url_button,$shell,$shell_on_form,$shell_on_submit,$shell_on_result)=split/\|`\|/,$fil[6];
$URLtoImage=$fil[7];
$body=$first_body=$fil[8];



#��������� ���� � �������

if (open (FILE,"<$data_dir/languages.txt")){

@languages=<FILE>;
close FILE;
chomp (@languages);

for $i(0..$#languages){
if ($languages[$i]=~/^::/){

($temp,$lang_name,$lang_abb)=split/::/,$languages[$i];
if ($lang_abb eq $sys_lang){

$counter=1;
for $n(($i+1)..$#languages){
if ($languages[$n] eq ":end"){last}
$text[$counter]=$languages[$n];
$counter++;
}
}
}
}

}

#########################


if ($action eq 'submit'){goto SUBMIT}

if (&unlock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}

if ($action eq 'result'){
result();
$pr_page.="\n<br><br>\n";
print_page();
exit;
}
if ($action eq 'jresult'){
$j="1";result();
$pr_page.="\n<br><br>\n";
print_page();
exit;
}

if ($action eq 'form'){goto FORM}
if ($action eq 'form_check'){$check=1;goto FORM}
if ($action eq 'form_select'){$select=1;goto FORM}


$pr_page.="���������� ������ � ���������� ����������<br><br>\n";
print_page();

exit;


###################################################
# �������� �����                                #
###################################################
FORM:

$pr_page.="<form action=\"$cgiUrl/tigvote.cgi\" method=POST>\n";
$pr_page.="<input type=hidden name=action value=submit>\n";
$pr_page.="<input type=hidden name=file value=$files[0]>\n";

$pr_page.="$tag_title_open$fil[9]$tag_title_close\n";

$pr_page.="<table border=0>\n";

if ($select){
$pr_page.="<tr><td>\n";
$pr_page.="$tag_question_open\n";
$pr_page.="<select name=tigvote>\n";
for $i(10..$#fil){
($row,$value)=split /\|`\|/,$fil[$i];
$pr_page.="<option value=".($i-10).">$row<br>\n";
}
$pr_page.="</select>\n";
$pr_page.="$tag_question_close";
$pr_page.="</td></tr>\n";
}

else {

for $i(10..$#fil){
($row,$value)=split /\|`\|/,$fil[$i];

$pr_page.="<tr><td>&nbsp;&nbsp;<input type=";
if ($check){$pr_page.="checkbox"}
else {$pr_page.="radio"}
$pr_page.=" name=tigvote value=".($i-10).">$tag_question_open$row$tag_question_close</td></tr>\n";
}
}


if ($url_button){$pr_page.="<tr><td><center><input type=image src=$url_button alt=\"$submitText\" border=0></center>\n"}
else {$pr_page.="<tr><td><center><input type=submit value=\"$submitText\"></center>\n"}


$pr_page.="</td></tr>\n";
$pr_page.="</table></form>\n";
$pr_page.="<!--Lyceum voting-->\n";
print_page();
exit;


###################################################
# ����������� ������                              #
###################################################
SUBMIT:

unless (@tigvote){
$pr_page.="<br>";

$pr_page.="$tag_system_open$text[1]$tag_system_close"; # ������ ����� �� ��� ��������!

$pr_page.="</font><br><br><a href=\"javascript:history.back()\">";

$pr_page.="$tag_system_open$text[2]$tag_system_close"; # �����������

$pr_page.="</a>\n<br><br>\n";
if (&unlock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}
print_page();
exit;
}


for $i(0..$#tigvote){
if ($tigvote[$i]){
($row,$number)=split/\|`\|/,$fil[$i+10];

# ������� ����� � ��������� ������ ������
unless ($row){
$pr_page.="<br>\n";

$pr_page.="$tag_system_open$text[3]$tag_system_close"; # ������� ��������� ������. �������� �������.

$pr_page.="</font><br><br><a href=\"javascript:history.back()\">";

$pr_page.="$tag_system_open$text[2]$tag_system_close"; # �����������

$pr_page.="</a>\n<br><br>\n";
if (&unlock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}
print_page();
exit;
}
############


$number++;
$fil[$i+10]="$row|`|$number";
}
}

# ������� IP
if($close_ip eq 'yes'){IPcheck()}

for $i(0..$#fil){$fil[$i].="\n"}

# ����������� ����� � ��������� ������ ������
chomp($fil[9]);
($fil[9])=split/\|`\|/,$fil[9];
$fil[9].="\n";
for $i(10..$#fil){
($row,$number)=split/\|`\|/,$fil[$i];
unless ($row){$fil[$i]=""}
}
#############


open FILE,">$data_dir/vote/$files[0].txt";
print FILE @fil;
close FILE;

if (&unlock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}


$point="";
for $i(0..$#tigvote){
if ($tigvote[$i]){
($row,$number)=split/\|`\|/,$fil[$i+10];
$point.="$row<br>";
}
}
$forLog="1=$point";
writeLog();

#������� ���� �����������

$pr_page.="$tag_system_open$text[4]$tag_system_close"; # ������, ��� ����� ���������.

$pr_page.="</font><br><br>\n";
if($showResult eq 'yes'){result();}
else {
$pr_page.="<a href=\"javascript:history.back()\">";

$pr_page.="$tag_system_open$text[2]$tag_system_close"; # �����������

$pr_page.="</a>";
}

print_page();
exit;



#################################################
#               �����������                    #
#################################################
#################################################
# ������������ ������ �������                   #
#################################################
sub result()
{

$pr_page.="<table border=0>\n";

for $f(0..$#files){

if (&lock("$data_dir/vote/$files[$f].txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$files[$f].txt";
@fil=<FILE>;
close FILE;
if (&unlock("$data_dir/vote/$files[$f].txt"))
{print "$error_message";exit}
chomp(@fil);

($tag_title_open,$tag_title_close,$tag_system_open,$tag_system_close)=split/\|`\|/,$fil[0];
($tag_question_open,$tag_question_close)=split/\|`\|/,$fil[1];

$graphLenght=$fil[2];
$graphWidth=$fil[3];
$submitText=$fil[4];
($close_ip,$close_ip_time)=split/\|`\|/,$fil[5];
($showResult,$sys_lang,$sort,$url_button)=split/\|`\|/,$fil[6];
$URLtoImage=$fil[7];
$body=$fil[8];

#������� ������ � �����

$sum=0;@num="";
for $i(10..$#fil){
($mess[$i-10],$num[$i-10])=split /\|`\|/,$fil[$i];
$sum+=$num[$i-10];
}

#����������� �������
#����������� ���������� ��������, ����������� ������������
@temp=sort{$b<=>$a}@num;
$max=$temp[0];
unless ($max){$max=1;}
$koeff=$graphLenght/$max;

#���������� �� ��������
if ($sort eq "vote"){
for $i(0..$#num){
for $n(0..$#num-$i-1){
if ($num[$n]<$num[$n+1]){@num[$n,$n+1]=@num[$n+1,$n];@mess[$n,$n+1]=@mess[$n+1,$n]}
}
}
}
if ($sort eq "vote-reverse"){
for $i(0..$#num){
for $n(0..$#num-$i-1){
if ($num[$n]>$num[$n+1]){@num[$n,$n+1]=@num[$n+1,$n];@mess[$n,$n+1]=@mess[$n+1,$n]}
}
}
}

#���������� �� �������
if ($sort eq "point"){
for $i(0..$#mess){
for $n(0..$#mess-$i-1){
if ($mess[$n] gt $mess[$n+1]){@mess[$n,$n+1]=@mess[$n+1,$n];@num[$n,$n+1]=@num[$n+1,$n]}
}
}
}
if ($sort eq "point-reverse"){
for $i(0..$#mess){
for $n(0..$#mess-$i-1){
if ($mess[$n] lt $mess[$n+1]){@mess[$n,$n+1]=@mess[$n+1,$n];@num[$n,$n+1]=@num[$n+1,$n]}
}
}
}

#�������� �������

$pr_page.="<tr><td>\n\n";


$pr_page.="<table border=0>\n";
$pr_page.="<tr><td colspan=4>$tag_title_open$fil[9]$tag_title_close</td></tr>\n";

$num_img=0;
for $i(10..$#fil){
$width=int($num[$i-10]*$koeff);
$percent=0;

if($sum!=0){$percent=$num[$i-10]/$sum*100;$percent=int($percent*100+0.5)/100;}

if($width==0){$pr_page.="<tr><td>$tag_question_open$mess[$i-10]$tag_question_close</td><td>$tag_question_open&nbsp;$num[$i-10]$tag_question_close</td><td>$tag_question_open($percent%)$tag_question_close</td><td></td></tr>\n";}
else {$pr_page.="<tr><td>$tag_question_open$mess[$i-10]$tag_question_close</td><td>$tag_question_open&nbsp;$num[$i-10]$tag_question_close</td><td>$tag_question_open($percent%)$tag_question_close</td><td><img src=$URLtoImage/$num_img.gif height=$graphWidth width=$width></td></tr>\n";}
if ($num_img<9){$num_img++}
else {$num_img=0}
}
$pr_page.="<tr><td>$tag_question_open";

$pr_page.="$text[5]"; # ������


$pr_page.=":$tag_question_close</td><td>$tag_question_open&nbsp;$sum$tag_question_close</td><td colspan=2>&nbsp;</td></tr>\n";
$pr_page.="</table>\n";
$pr_page.="<!--Lyceum voiting-->\n";

$pr_page.="<hr size=1>\n";

$pr_page.="</td></tr>\n\n";

}
$pr_page.="<tr><td align=right><font face=arial size=1><a href=http://www.lyceum1.cv.ua>Lyceum1</a> Copyright &copy; 2003</td></tr>\n";
$pr_page.="</table>\n\n";

if ($j==1){$pr_page.="<a href=\"javascript:window.close()\">";

$pr_page.="$tag_system_open$text[6]$tag_system_close"; # ������� ����

$pr_page.="</a>"}
else {$pr_page.="<a href=\"javascript:history.back()\">";

$pr_page.="$tag_system_open$text[2]$tag_system_close"; # �����������

$pr_page.="</a>"}
}


#################################################
# ����������� ������� IP                      #
#################################################
sub IPcheck()
{

$close_ip_time*=60;

if (&lock("$data_dir/vote/$files[0]-ip.txt"))
{print "$error_message";exit}
open FILE,"<$data_dir/vote/$files[0]-ip.txt";
@filip=<FILE>;
close FILE;


# �� ������, ���� ����� ���� � ����
for $i(0..$#filip){
($file_ip,$ip_time)=split/:/,$filip[$i];
chomp($ip_time);

if($file_ip eq $ip){

if ((!$close_ip_time) || (time-$ip_time)<$close_ip_time){


if (&unlock("$data_dir/vote/$files[0].txt"))
{print "$error_message";exit}

if (&unlock("$data_dir/vote/$files[0]-ip.txt"))
{print "$error_message";exit}




$pr_page.="$tag_system_open$text[7]$tag_system_close"; # "��� ����� �� ���������,�� �� ��� ����������!


$pr_page.="</font><br><br>";
if($showResult eq 'yes'){result();}


$point="";
for $i(0..$#tigvote){
if ($tigvote[$i]){
($row,$number)=split/\|`\|/,$fil[$i+10];
$point.="$row<br>";
}
}

$forLog="3=$point";
writeLog();

print_page();
exit;
}
else {$filip[$i]="";}
}
}

push (@filip,"$ip:".time."\n");

open FILE,">$data_dir/vote/$files[0]-ip.txt";
print FILE @filip;
close FILE;
if (&unlock("$data_dir/vote/$files[0]-ip.txt"))
{print "$error_message";exit}
}


#################################################
# ����������� ������ ���-�����                 #
#################################################
sub writeLog()
{
if (&lock("$data_dir/vote/$files[0]-log.txt"))
{print "$error_message";exit}
open LOG,">>$data_dir/vote/$files[0]-log.txt";
print LOG "$date=$ENV{'REMOTE_ADDR'}=$ENV{'REMOTE_HOST'}=$forLog\n";
close LOG;
if (&unlock("$data_dir/vote/$files[0]-log.txt"))
{print "$error_message";exit}
}

#################################################
# ����������� ���������� ����                  #
#################################################
sub getDate()
{
@days = ('�����������','�����������','�������','�����','�������','�������','�������');
@months = ('01','02','03','04','05','06','07','08','09','10','11','12');

($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$year=$year-100;
if($year < 10) { $year = "0$year"; }
if($hour < 10) { $hour = "0$hour"; }
if ($min < 10) { $min = "0$min"; }
if ($sec < 10) { $sec = "0$sec"; }

$date = "$mday=$months[$mon]=$year=$days[$wday]=$hour=$min=$sec";
}

#################################################
# �� ���� ������� ���� � ������                #
#################################################
sub no_lang(){
$no_lang=1;
}


#################################################
# ���� ������ �������                       #
#################################################
sub print_page(){

if ($shell){
open FILE,"<$data_dir/shells/$shell.txt";
@shell=<FILE>;
close FILE;

for $i(0..$#shell){
$shell[$i]=~s/<!-- #voting# -->/$pr_page/;
}
}

if ($shell && $shell_on_form && (($action eq "form") || ($action eq "form_check") || ($action eq "form_select"))){
print @shell;
return;
}
if ($shell && $shell_on_submit && ($action eq "submit")){
print @shell;
return;
}
if ($shell && $shell_on_result && (($action eq "result") || ($action eq "jresult"))){
print @shell;
return;
}

# html-�������� ���������
print "<HTML>\n<HEAD>\n<TITLE>����������� �� ���������� ����</TITLE>\n</HEAD>\n$first_body\n\n";

print $pr_page;

print <<END_of_multiple_text;

</BODY>
</HTML>
END_of_multiple_text

}


##################################################################
#
# lock() Version 2.1
# Written by Craig Patchett craig@patchett.com
# Created 16/09/1996 Last Modified 12/05/2000
#
# ������� ������� ������������ ���������� ��� �����.  ����������
# �������� ������ ���� ������ ���������, ���������� ��������
# ������ � �����, ����� ���������� ��� ������������.
#
# ������� ����������:
#       0  -  ���� ���������� �����������
#       1  -  ��� ������ �������� $LOCK_DIR/$filename.tmp
#       2  -  ���� $filename ������������
#       3  -  ���� lock-���� �� �������� ������� ��� �������
#
# ���������� ����������:
#       $error_message  -  ���������� � ��������� ������
#       $NAME_LEN  -  ������������ ����� �����
#       $LOCK_DIR  -  ������� ��� �������� ����� ����������
#       $MAX_WAIT  -  ������������ ����� �������� ����������
#
# �� ����� ������ ���������:
#       $LOCK_DIR/$filename.tmp
#       $LOCK_DIR/$filename.lok (���������� ������ ���� ����
#                                ������������)
#
##################################################################
sub lock
{  local($filename)=@_;
   local($wait, $lock_pid);
   local($temp_file)="$LOCK_DIR$$.tmp";
   local($lock_file)=$filename;
   $lock_file=~tr/\/\\:.//d;           # �������� ���������� ��������
   if ($NAME_LEN && ($NAME_LEN < length($lock_file)))
     {  $lock_file=substr($lock_file, -$NAME_LEN);
     }
   $lock_file="$LOCK_DIR$lock_file.lok";
   $error_message='';
       # ��������� ����� � PID
   if (!open(TEMP, ">$temp_file"))
     {  $error_message="Content-type: text/html\n\n1. ��������� �������� $temp_file ($!).";
        return(1);
     }
   print TEMP $$;
   close(TEMP);
       # ������� lock-�����
   if (-e $lock_file)
     {
   #����������, ���� ���� ������������ (���� lock-���� ����)
        for ($wait=$MAX_WAIT; $wait; --$wait)
          {  sleep(1);
             last unless -e $lock_file;
          }
     }
   if ((-e $lock_file) && (-M $lock_file < 0))
     {  unlink($temp_file);
        $error_message="Content-type: text/html\n\n2. ���� \"$filename\" � ������ ������ ���������������. ����������� �� ��� �����.";
        return(2);
     }
   else
     {  if (!rename($temp_file, $lock_file))
          {  unlink($temp_file);
             $error_message="Content-type: text/html\n\n3. ��������� ����������� ���� \"$filename\" ($!).";
             return(3);
          }
       # ������� ���������
        if (!open(LOCK, "<$lock_file"))
          {  $error_message="Content-type: text/html\n\n4. ��������� �������� ��������� ����� \"$filename\" ($!).";
             return(3);
          }
        $lock_pid=<LOCK>;
        close(LOCK);
        if ($lock_pid ne $$)
          {  $error_message="Content-type: text/html\n\n5. ���� \"$filename\" � ������ ������ ���������������. ����������� �� ��� �����.";
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
# ������������ ����, ��������������� �������� lock()
#
# ����������:
#       0  -  ���� ���� �������������
#       1  -  ���� ��� ������� � lock-�����
#       2  -  ���� ���� ������������ ������ ���������
#       3  -  ���� ���������� �������������� ����
#
# ���������� ����������:
#       $error_message  -  ���������� � ��������� ������
#       $NAME_LEN  -  ������������ ����� �����
#       $LOCK_DIR  -  ������� ��� �������� ����� ����������
#
# �� ����� ������ ��������� $LOCK_DIR/$filename.lok
#
##################################################################

sub unlock 
{  local($filename)=@_;
   local($lock_file)=$filename;
   $lock_file=~tr/\/\\:.//d;          # ��������� ���������� ��������
   if ($NAME_LEN<length($lock_file))
     {  $lock_file=substr($lock_file, -$NAME_LEN);
     }
   $lock_file="$LOCK_DIR$lock_file.lok";
   $error_message='';
       # �������� ����������
   if (!open(LOCK, "<$lock_file"))
     {  $error_message="Content-type: text/html\n\n�� �� ������� �� ������������� ����� \"$filename\" ($!).";
        return(1);
     }

   $lock_pid=<LOCK>;
   close(LOCK);
   if ($lock_pid ne $$)
     {  $error_message="Content-type: text/html\n\n���� \"$filename\" ������������ ����� ��������.";
        return(2);
     }
       #��������� lock-�����
   if (!unlink($lock_file))
     {  $error_message="Content-type: text/html\n\n��������� ������������ ���� \"$filename\" ($!).";
        return(3);
     }
   return(0);
}