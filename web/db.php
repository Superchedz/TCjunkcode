<?php

$host = "localhost"; // Host name
$username = "root"; // Mysql username
$password = "pass123"; // Mysql password
$db_name = "BoilerControl"; // Database name

$con = mysqli_connect("$host", "$username", "$password");
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

mysqli_select_db($con, "$db_name") or die("cannot select DB");

?>
