<?php

$host = "localhost"; // Host name
$username = "TCROOT9000"; // Mysql username
$passwordprefix = "TC"; // Mysql password
$passwordsuffix = "9000"; // Mysql password
$db_name = "BoilerControl"; // Database name

$lines = file('/home/pi/led/pwsf.txt');
 
 
foreach($lines as $line) {
    if(empty($line)) continue;
    $line = trim($line);
    $passwordmiddle = substr($line,4, 6);
} 

$password = $passwordprefix.$passwordmiddle.$passwordsuffix;

$con = mysqli_connect("$host", "$username", "$password");
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

mysqli_select_db($con, "$db_name") or die("cannot select DB");

?>
