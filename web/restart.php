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

$sql1 = "update $tbl_name SET Param_Value = 'R' where Param_Name= 'Shutdown'";
$result1 = mysqli_query($con, $sql1);

echo "<div class='alert alert-info alert-dismissible' role='alert'>The system will now reboot - wait 1 min and reopen webpage";
echo "</div>";

mysqli_close($con);
ob_end_flush();
 
?>
