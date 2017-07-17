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

$sql = "delete from $tbl_name where Zone_ID=$zoneid";
$result = mysqli_query($con, $sql);

echo "Success";

mysqli_close($con);
ob_end_flush();

?>
