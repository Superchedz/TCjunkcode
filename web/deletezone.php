<?php

ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "zone_b"; // Table name

$zoneid = GetInputFromRequest('zoneid');

$zoneid = mysqli_real_escape_string($con, $zoneid);

$sql1 = "DELETE FROM $tbl_name where Zone_ID=$zoneid";
$result1 = mysqli_query($con, $sql1);

$sql2 = "DELETE FROM schedule_b where Schedule_Zone_ID=$zoneid";
$result2 = mysqli_query($con, $sql2);

$sql3 = "DELETE FROM override_b where Zone_ID=$zoneid";
$result3 = mysqli_query($con, $sql3);


echo "<div class='alert alert-info alert-dismissible' role='alert'>Selected zone deleted.(home.php)";
echo "</div>";

mysqli_close($con);
ob_end_flush();

?>
