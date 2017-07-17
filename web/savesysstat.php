<?php

ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "params_b"; // Table name

$mystatus = GetInputFromRequest('status');

$mystatus = mysqli_real_escape_string($con, $mystatus);

$sql = "SELECT * FROM $tbl_name where Param_Name='sysstatus'";
$result = mysqli_query($con, $sql);

$name = "NA";

if ($result->num_rows > 0) {
    $sql = "update $tbl_name set Param_Value='$mystatus' where Param_Name='sysstatus'";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "insert into $tbl_name value('sysstatus','$mystatus')";
    $result = mysqli_query($con, $sql);
}

echo "Success";

mysqli_close($con);
ob_end_flush();

?>
