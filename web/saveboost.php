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
$scparam_allzones = GetInputFromRequest('scparam_allzones');


$zoneid = GetInputFromRequest('zoneid');

$scparam_boostfor = mysqli_real_escape_string($con, $scparam_boostfor);
$scparam_boostformin = mysqli_real_escape_string($con, $scparam_boostformin);
$scparam_boostfordegree = mysqli_real_escape_string($con, $scparam_boostfordegree);
$scparam_allzones = mysqli_real_escape_string($con, $scparam_allzones);
$zoneid = mysqli_real_escape_string($con, $zoneid);

if ($scparam_allzones == "true") {
    $sql = "select * from zone_b where Zone_Active_Ind='Y'";
    $result = mysqli_query($con, $sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $zoneid = $row["Zone_ID"];
            if ($scparam_boostfor >= 0 && $scparam_boostformin >= 0 && $scparam_boostfordegree >=
                0 && $zoneid >= 0) {
                $sql1 = "DELETE FROM $tbl_name where Zone_ID=$zoneid";
                $result1 = mysqli_query($con, $sql1);
            }

            $sql2 = "insert into $tbl_name value($zoneid,NOW(), DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE), TIME_TO_SEC(TIMEDIFF(DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE),NOW()))/60, $scparam_boostfordegree)";
            $result2 = mysqli_query($con, $sql2);
        }
    }
} else {
    if ($scparam_boostfor >= 0 && $scparam_boostformin >= 0 && $scparam_boostfordegree >=
        0 && $zoneid >= 0) {
        $sql = "DELETE FROM $tbl_name where Zone_ID=$zoneid";
        $result = mysqli_query($con, $sql);
    }

    $sql = "insert into $tbl_name value($zoneid,NOW(), DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE), TIME_TO_SEC(TIMEDIFF(DATE_ADD(DATE_ADD(NOW(), INTERVAL $scparam_boostfor HOUR), INTERVAL $scparam_boostformin MINUTE),NOW()))/60, $scparam_boostfordegree)";
    $result = mysqli_query($con, $sql);
}
echo "<div class='alert alert-info alert-dismissible' role='alert'>Inserted a new row to the override table. It might take upto few mins to apply the boost.";
echo "</div>";

mysqli_close($con);
ob_end_flush();

?>
