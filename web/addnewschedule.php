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
$scparam_totime = GetInputFromRequest('totime');
$scparam_temp = GetInputFromRequest('temp');

$scparam_daytoretrieve = mysqli_real_escape_string($con, $scparam_daytoretrieve);
$scparam_zoneid = mysqli_real_escape_string($con, $scparam_zoneid);
$scparam_fromtime = mysqli_real_escape_string($con, $scparam_fromtime);
$scparam_totime = mysqli_real_escape_string($con, $scparam_totime);
$scparam_temp = mysqli_real_escape_string($con, $scparam_temp);


$sql = "SELECT * FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = '$scparam_daytoretrieve' and ((Schedule_Starttime >='$scparam_fromtime' and Schedule_Starttime<='$scparam_totime')  or (Schedule_Endtime >='$scparam_fromtime' and Schedule_Endtime<='$scparam_totime') or (Schedule_Starttime <='$scparam_fromtime' and Schedule_Endtime>='$scparam_totime'))";
$result = mysqli_query($con, $sql);
if ($result->num_rows > 0) {
    echo "<div class='alert alert-danger alert-dismissible' role='alert'>New schedule is overlapping with existing schedule.";
    echo "</div>";
} else {
    $sql1 = "INSERT INTO $tbl_name value($scparam_zoneid , '$scparam_daytoretrieve', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
    $result1 = mysqli_query($con, $sql1);
}
mysqli_close($con);

ob_end_flush();

?>
