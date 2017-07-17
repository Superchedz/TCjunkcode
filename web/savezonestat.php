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

$mystatus = GetInputFromRequest('status');
$zoneid = GetInputFromRequest('zoneid');
$fieldName = GetInputFromRequest('field');

$mystatus = mysqli_real_escape_string($con, $mystatus);
$zoneid = mysqli_real_escape_string($con, $zoneid);
$fieldName = mysqli_real_escape_string($con, $fieldName);

if ($fieldName == "Zone_Current_State_Ind") {
    if ($mystatus == "true") {
        $mystatus = "ON";
    } else {
        $mystatus = "OFF";
    }
} else {
    if ($mystatus == "true") {
        $mystatus = "Y";
    } else {
        $mystatus = "N";
    }
}

$sql = "update $tbl_name set $fieldName='$mystatus' where Zone_ID=$zoneid";
$result = mysqli_query($con, $sql);

echo "Success";

mysqli_close($con);
ob_end_flush();

?>
