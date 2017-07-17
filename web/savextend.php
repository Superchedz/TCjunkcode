<?php

ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "override_b"; // Table name

$zoneid = GetInputFromRequest('zoneid');

$zoneid = mysqli_real_escape_string($con, $zoneid);

$sql = "call getNextSchedule($zoneid);";
$result = mysqli_query($con, $sql);

if ($result->num_rows == 1) {
    $row = $result->fetch_assoc();
    $currentdate = $row["formated_date"];
    $currenttime = $row["timefrom"];
    $tempnow = $row["temp"];

    $currentdate = mysqli_real_escape_string($con, $currentdate);
    $currenttime = mysqli_real_escape_string($con, $currenttime);
    $tempnow = mysqli_real_escape_string($con, $tempnow);
    $count = $result->num_rows;
    $result->close();
    $con->next_result();

    $sql1 = "DELETE FROM $tbl_name where Zone_ID=$zoneid";
    $result1 = mysqli_query($con, $sql1);

    $sql2 = "insert into $tbl_name value($zoneid,NOW(),'$currentdate $currenttime', TIME_TO_SEC(TIMEDIFF('$currentdate $currenttime', NOW()))/60, $tempnow)";
    $result2 = mysqli_query($con, $sql2);

    echo "<div class='alert alert-info alert-dismissible' role='alert'>Inserted a new row to the override table.(home.php)";
    echo "</div>";
} else {
    echo "<div class='alert alert-danger alert-dismissible' role='alert'>No schedule exist.";
    echo "</div>";

}
mysqli_close($con);
ob_end_flush();

?>
