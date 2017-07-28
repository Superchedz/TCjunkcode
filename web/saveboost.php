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


$scparam_boostfor = GetInputFromRequest('scparam_boostfor');
$scparam_boostformin = GetInputFromRequest('scparam_boostformin');
$scparam_boostfordegree = GetInputFromRequest('scparam_boostfordegree');



$zoneid = GetInputFromRequest('zoneid');

$scparam_boostfor = mysqli_real_escape_string($con, $scparam_boostfor);
$scparam_boostformin = mysqli_real_escape_string($con, $scparam_boostformin);
$scparam_boostfordegree = mysqli_real_escape_string($con, $scparam_boostfordegree);
	$zoneid = mysqli_real_escape_string($con, $zoneid);

if ($scparam_boostfor >= 0 && $scparam_boostformin >= 0 && $scparam_boostfordegree >=
    0 && $zoneid >= 0) {
    $sql = "DELETE FROM $tbl_name where Zone_ID=$zoneid";
    $result = mysqli_query($con, $sql);
}

    $sql = "insert into $tbl_name value($zoneid,NOW(), DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE), TIME_TO_SEC(TIMEDIFF(DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE),NOW()))/60, $scparam_boostfordegree)";
    $result = mysqli_query($con, $sql);

echo "<div class='alert alert-info alert-dismissible' role='alert'>Inserted a new row to the override table. It might take upto few mins to apply the boost.";
echo "</div>";
echo $sql;

mysqli_close($con);
ob_end_flush();

?>
