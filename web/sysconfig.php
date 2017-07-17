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

$sql = "SELECT * FROM $tbl_name";
$result = mysqli_query($con, $sql);

$Interval = 0;
$FromEmail = "";
$ToEmail = "";
$SMTPServer = "";
$SMTPPwd = "";
$FrozenVal = 0;
$LogRetention = 0;

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        if ($row["Param_Name"] == "Loop_Intvl") {
            $Interval = $row["Param_Value"];
        }

        if ($Interval == "") {
            $Interval = "0";
        }

        if ($row["Param_Name"] == "FromEmail") {
            $FromEmail = $row["Param_Value"];
        }

        if ($row["Param_Name"] == "ToEmail") {
            $ToEmail = $row["Param_Value"];
        }

        if ($row["Param_Name"] == "ServerSMTP") {
            $SMTPServer = $row["Param_Value"];
        }

        if ($row["Param_Name"] == "EmailPwd") {
            $SMTPPwd = $row["Param_Value"];
        }

        if ($row["Param_Name"] == "FrostTemp") {
            $FrozenVal = $row["Param_Value"];
        }

        if ($FrozenVal == "") {
            $FrozenVal = "0";
        }


        if ($row["Param_Name"] == "Log_Ret") {
            $LogRetention = $row["Param_Value"];
        }

        if ($LogRetention == "") {
            $LogRetention = "0";
        }


    }
}

echo "<form class='form-vertical'>";
echo "  <div class='form-group'>";
echo "    <label for='scparam_polinterval' class='col-sm-4 control-label'>Polling Interval</label>";
echo "    <div class='col-sm-2'>";
echo "      <input type='number' class='form-control' id='scparam_polinterval' placeholder='Polling Interval' value='" .
    $Interval . "'>";
echo "    </div>";
echo "    <div class='col-sm-2'>";
echo "  <label for='scparam_polinterval1' class='col-sm-6 control-label'>Seconds</label>";
echo "  </div>";
echo "  </div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_fromemail' class='col-sm-4 control-label'>From Email</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='email' class='form-control' id='scparam_fromemail' placeholder='SMTP From Email Address' value='" .
    $FromEmail . "'>";
echo "    </div>";
echo "  </div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_smtpserver' class='col-sm-4 control-label'>SMTP Server</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='email' class='form-control' id='scparam_smtpserver' placeholder='SMTP Server' value='" .
    $SMTPServer . "'>";
echo "    </div>";
echo "  </div>";


echo "  <div class='form-group'>";
echo "    <label for='scparam_emailpwd' class='col-sm-4 control-label'>SMTP Password</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='text' class='form-control' id='scparam_emailpwd' placeholder='Password' value='" .
    $SMTPPwd . "'>";
echo "    </div>";
echo "  </div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_toemail' class='col-sm-4 control-label'>Alert Emails To</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='email' class='form-control' id='scparam_toemail' placeholder='Email Alert Address' value='" .
    $ToEmail . "'>";
echo "    </div>";
echo "  </div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_logret' class='col-sm-4 control-label'>Log Retention</label>";
echo "    <div class='col-sm-2'>";
echo "      <input type='number' class='form-control' id='scparam_logret' placeholder='Retention Period' value='" .
    $LogRetention . "'>";
echo "    </div>";
echo "    <div class='col-sm-2'>";
echo "  <label for='scparam_logret1' class='col-sm-6 control-label'>Days</label>";
echo "  </div>";
echo "  </div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_frost' class='col-sm-4 control-label'>Frost Temperature</label>";
echo "    <div class='col-sm-2'>";
echo "      <input type='number' class='form-control' id='scparam_frost' placeholder='Frost Temperature' value='" .
    $FrozenVal . "'>";
echo "    </div>";
echo "    <div class='col-sm-6'>";
echo "  <label for='scparam_frost1' class='col-sm-6 control-label'>Degrees (&deg;C)</label>";
echo "  </div>";
echo "  </div>";

echo "</form>";


mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();

?>
