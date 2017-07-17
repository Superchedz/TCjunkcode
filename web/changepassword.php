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


$scparam_oldpassword = GetInputFromRequest('scparam_oldpassword');
$scparam_newpassword = GetInputFromRequest('scparam_Newpassword');
$loggedemail = $_SESSION['myemail'];

$scparam_oldpassword = mysqli_real_escape_string($con, $scparam_oldpassword);
$scparam_newpassword = mysqli_real_escape_string($con, $scparam_newpassword);

if ($scparam_newpassword == "" || $scparam_oldpassword == "") {
    echo "<div class='alert alert-info alert-danger' role='alert'>Old/New password cannot be blank.";
    echo "</div>";
} else {
    $sql = "select * from myusers where email='$loggedemail' and BINARY password='$scparam_oldpassword'";
    $result = mysqli_query($con, $sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {

            $sql2 = "update myusers set password='$scparam_newpassword' where email='$loggedemail'";
            $result2 = mysqli_query($con, $sql2);

            echo "<div class='alert alert-info alert-dismissible' role='alert'>Password changed.";
            echo "</div>";

        }
    } else {
        echo "<div class='alert alert-info alert-danger' role='alert'>Invalid Password.";
        echo "</div>";
    }
}


mysqli_close($con);
ob_end_flush();

?>
