<?php
ob_start();

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "myusers"; // Table name


$myemail = GetInputFromRequestPost('myemail');
$mypassword = GetInputFromRequestPost('mypassword');

$myemail = mysqli_real_escape_string($con, $myemail);
$mypassword = mysqli_real_escape_string($con, $mypassword);

$sql = "SELECT * FROM $tbl_name WHERE email='$myemail' and password='$mypassword'";
$result = mysqli_query($con, $sql);

$name = "NA";
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $name = $row["Name"];
        echo $name;
    }
} else {
    echo "0 results";
}

$count = mysqli_num_rows($result);

mysqli_free_result($result);
mysqli_close($con);

// If result matched $myusername and $mypassword, table row must be 1 row
if ($count == 1) {
    session_start();
    $_SESSION['myemail'] = $myemail;
    $_SESSION['myname'] = $name;
    header('Location:home.php');
} else {
    header('Location:index.php?err=wrongcredentials');
}
ob_end_flush();

?>
