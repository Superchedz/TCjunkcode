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


$scparam_zonename = GetInputFromRequest('scparam_addzonename');
$scparam_zonesensor = GetInputFromRequest('scparam_addzonesensor');
$scparam_offset = GetInputFromRequest('scparam_addoffset');
$scparam_zonetype = GetInputFromRequest('scparam_addzonetype');
$scparam_pinnum = GetInputFromRequest('scparam_addpinnum');



$scparam_zonename = mysqli_real_escape_string($con, $scparam_zonename);
$scparam_zonesensor = mysqli_real_escape_string($con, $scparam_zonesensor);
$scparam_offset = mysqli_real_escape_string($con, $scparam_offset);
$scparam_zonetype = mysqli_real_escape_string($con, $scparam_zonetype);
$scparam_pinnum = mysqli_real_escape_string($con, $scparam_pinnum);

$sql = "select IFNULL(max(zone_id),0) + 1 as 'Id' from zone_b";
$result = mysqli_query($con, $sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $NewId = $row["Id"];

    $sql1 = "insert into $tbl_name (Zone_ID, Zone_Name, Zone_Active_Ind, Zone_Current_State_Ind, Zone_Last_Temp_Reading, Zone_Last_Temp_Reading_Dtime, Zone_Sensor_ID, Zone_Offset, Pi_Pin_num, Zone_Type) value($NewId , '$scparam_zonename', 'N', 'OFF', 0, current_date, '$scparam_zonesensor', $scparam_offset, $scparam_pinnum, '$scparam_zonetype')";
    $result1 = mysqli_query($con, $sql1);

    echo "<div class='alert alert-info alert-dismissible' role='alert'>New Zone Created.";
    echo "</div>";
}

mysqli_close($con);
ob_end_flush();

?>
