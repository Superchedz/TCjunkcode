<?php
ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "schedule_b"; // Table name

$scparam_daytoretrieve = GetInputFromRequest('selectedday');
$scparam_zoneid = GetInputFromRequest('zone');
$scparam_fromtime = GetInputFromRequest('fromtime');

$scparam_daytoretrieve = mysqli_real_escape_string($con, $scparam_daytoretrieve);
$scparam_zoneid = mysqli_real_escape_string($con, $scparam_zoneid);
$scparam_fromtime = mysqli_real_escape_string($con, $scparam_fromtime);

$sql = "DELETE FROM $tbl_name where Schedule_Zone_ID = '$scparam_zoneid' and Schedule_Day = '$scparam_daytoretrieve' and Schedule_Starttime='$scparam_fromtime'";
$result = mysqli_query($con, $sql);

mysqli_close($con);

ob_end_flush();

?>
