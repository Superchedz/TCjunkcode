<?php

ob_start();

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "myusers"; // Table name

$myemail = GetInputFromRequest('mypemail');

$myemail = mysqli_real_escape_string($con, $myemail);

$sql = "SELECT * FROM $tbl_name WHERE email='$myemail'";
$result = mysqli_query($con, $sql);

$name = "NA";
if ($result->num_rows > 0) {
    // output data of each row
    while ($row = $result->fetch_assoc()) {
        $name = $row["Name"];
        $pwd = $row["password"];
        // the message
        $msg = "Dear ";
        $msg .= $name;
        $msg .= "\n";
        $msg .= "Your password is:" . $pwd;
        $headers = 'From: <nagakishore.movva@gmail.com>' . "\r\n";
        // use wordwrap() if lines are longer than 70 characters
        $msg = wordwrap($msg, 70);
        // send email
        mail($myemail, "Password Request", $msg, $headers);
        echo "<div class='alert alert-danger alert-dismissible' role='alert'>Password emailed to ";
        echo $name;
        echo "</div>";
    }
} else {
    echo "<div class='alert alert-danger alert-dismissible' role='alert'>Invalid Email address, Please make sure the email address is provided is valid.";
    echo "</div>";
}

mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();

?>
