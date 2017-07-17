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


$scparam_zonename = GetInputFromRequest('scparam_zonename');
$scparam_zonesensor = GetInputFromRequest('scparam_zonesensor');
$scparam_offset = GetInputFromRequest('scparam_offset');
$scparam_pinnum = GetInputFromRequest('scparam_pinnum');
$zoneid = GetInputFromRequest('zoneid');

$scparam_zonename = mysqli_real_escape_string($con, $scparam_zonename);
$scparam_zonesensor = mysqli_real_escape_string($con, $scparam_zonesensor);
$scparam_offset = mysqli_real_escape_string($con, $scparam_offset);
$scparam_pinnum = mysqli_real_escape_string($con, $scparam_pinnum);
$zoneid = mysqli_real_escape_string($con, $zoneid);

$sql = "update $tbl_name set Zone_Name='$scparam_zonename', Zone_Sensor_ID='$scparam_zonesensor', Zone_Offset=$scparam_offset, Pi_Pin_num=$scparam_pinnum where Zone_ID=$zoneid";
$result = mysqli_query($con, $sql);

echo "<div class='alert alert-info alert-dismissible' role='alert'>Zone settings updated. It might take upto few mins to apply the boost.";
echo "</div>";

mysqli_close($con);
ob_end_flush();

?>
