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


$scparam_polinterval = GetInputFromRequest('scparam_polinterval');
$scparam_fromemail = GetInputFromRequest('scparam_fromemail');
$scparam_smtpserver = GetInputFromRequest('scparam_smtpserver');
$scparam_emailpwd = GetInputFromRequest('scparam_emailpwd');
$scparam_toemail = GetInputFromRequest('scparam_toemail');
$scparam_webaddr = GetInputFromRequest('scparam_webaddr');
$scparam_logret = GetInputFromRequest('scparam_logret');
$scparam_frost = GetInputFromRequest('scparam_frost');
$scparam_yplan = GetInputFromRequest('scparam_yplan');
$scparam_yplan_chzone = GetInputFromRequest('scparam_yplan_chzone');
$scparam_yplan_hwzone = GetInputFromRequest('scparam_yplan_hwzone');
$scparam_yplan_gpio = GetInputFromRequest('scparam_yplan_gpio');
$scparam_alexa = GetInputFromRequest('scparam_alexa');

$scparam_polinterval = mysqli_real_escape_string($con, $scparam_polinterval);
$scparam_fromemail = mysqli_real_escape_string($con, $scparam_fromemail);
$scparam_smtpserver = mysqli_real_escape_string($con, $scparam_smtpserver);
$scparam_emailpwd = mysqli_real_escape_string($con, $scparam_emailpwd);
$scparam_toemail = mysqli_real_escape_string($con, $scparam_toemail);
$scparam_webaddr = mysqli_real_escape_string($con, $scparam_webaddr);
$scparam_logret = mysqli_real_escape_string($con, $scparam_logret);
$scparam_frost = mysqli_real_escape_string($con, $scparam_frost);
$scparam_yplan = mysqli_real_escape_string($con, $scparam_yplan);
$scparam_yplan_chzone = mysqli_real_escape_string($con, $scparam_yplan_chzone);
$scparam_yplan_hwzone = mysqli_real_escape_string($con, $scparam_yplan_hwzone);
$scparam_yplan_gpio = mysqli_real_escape_string($con, $scparam_yplan_gpio);
$scparam_alexa = mysqli_real_escape_string($con, $scparam_alexa);


$scparam_polinterval_exist = "no";
$scparam_fromemail_exist = "no";
$scparam_smtpserver_exist = "no";
$scparam_emailpwd_exist = "no";
$scparam_toemail_exist = "no";
$scparam_webaddr_exist = "no";
$scparam_logret_exist = "no";
$scparam_yplan_exist = "no";
$scparam_yplan_chzone_exist = "no";
$scparam_yplan_hwzone_exist = "no";
$scparam_yplan_gpio_exist = "no";
$scparam_alexa_exist = "no";

$sql = "SELECT * FROM $tbl_name";
$result = mysqli_query($con, $sql);


if ($result->num_rows > 0) {
    // output data of each row
    while ($row = $result->fetch_assoc()) {

        if ($row["Param_Name"] == "Loop_Intvl") {
            $scparam_polinterval_exist = "yes";
        }

        if ($row["Param_Name"] == "FromEmail") {
            $scparam_fromemail_exist = "yes";
        }

        if ($row["Param_Name"] == "ToEmail") {
            $scparam_toemail_exist = "yes";
        }

        if ($row["Param_Name"] == "ServerSMTP") {
            $scparam_smtpserver_exist = "yes";
        }

        if ($row["Param_Name"] == "EmailPwd") {
            $scparam_emailpwd_exist = "yes";
        }

        if ($row["Param_Name"] == "Ext_Web_Address") {
            $scparam_emailpwd_exist = "yes";
        }

        if ($row["Param_Name"] == "FrostTemp") {
            $scparam_frost_exist = "yes";
        }

        if ($row["Param_Name"] == "Log_Ret") {
            $scparam_logret_exist = "yes";
        }
		
        if ($row["Param_Name"] == "Ext_Web_Address") {
            $scparam_webaddr_exist = "yes";
        }

        if ($row["Param_Name"] == "YPlan_YN") {
            $scparam_yplan_exist = "yes";
        }

        if ($row["Param_Name"] == "YPlan_CH_Zone") {
            $scparam_yplan_chzone_exist = "yes";
        }

        if ($row["Param_Name"] == "YPlan_HW_Zone") {
            $scparam_yplan_hwzone_exist = "yes";
        }

        if ($row["Param_Name"] == "YPlan_GPIO") {
            $scparam_yplan_gpio_exist = "yes";
        }
        if ($row["Param_Name"] == "Alexa_YN") {
            $scparam_alexa_exist = "yes";
        }
    }
}

if ($scparam_polinterval_exist == "no") {
    $sql = "insert into $tbl_name value('Loop_Intvl','$scparam_polinterval')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_polinterval' where Param_Name='Loop_Intvl'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_fromemail_exist == "no") {
    $sql = "insert into $tbl_name value('FromEmail','$scparam_fromemail')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_fromemail' where Param_Name='FromEmail'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_smtpserver_exist == "no") {
    $sql = "insert into $tbl_name value('ServerSMTP','$scparam_smtpserver')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_smtpserver' where Param_Name='ServerSMTP'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_emailpwd_exist == "no") {
    $sql = "insert into $tbl_name value('EmailPwd','$scparam_emailpwd')";	
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_emailpwd' where Param_Name='EmailPwd'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_toemail_exist == "no") {
    $sql = "insert into $tbl_name value('ToEmail','$scparam_toemail')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_toemail' where Param_Name='ToEmail'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_webaddr_exist == "no") {
    $sql = "insert into $tbl_name value('Ext_Web_Address','$scparam_webaddr')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_webaddr' where Param_Name='Ext_Web_Address'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_logret_exist == "no") {
    $sql = "insert into $tbl_name value('Log_Ret','$scparam_logret')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_logret' where Param_Name='Log_Ret'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_frost_exist == "no") {
    $sql = "insert into $tbl_name value('FrostTemp','$scparam_frost')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_frost' where Param_Name='FrostTemp'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_yplan_exist == "no") {
    $sql = "insert into $tbl_name value('YPlan_YN','$scparam_yplan')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_yplan' where Param_Name='YPlan_YN'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_yplan_chzone_exist == "no") {
    $sql = "insert into $tbl_name value('YPlan_CH_Zone','$scparam_yplan_chzone')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_yplan_chzone' where Param_Name='YPlan_CH_Zone'";
    $result = mysqli_query($con, $sql);
}


if ($scparam_yplan_hwzone_exist == "no") {
    $sql = "insert into $tbl_name value('YPlan_HW_Zone','$scparam_yplan_hwzone')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_yplan_hwzone' where Param_Name='YPlan_HW_Zone'";
    $result = mysqli_query($con, $sql);
}

if ($scparam_yplan_gpio_exist == "no") {
    $sql = "insert into $tbl_name value('YPlan_GPIO','$scparam_yplan_gpio')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_yplan_gpio' where Param_Name='YPlan_GPIO'";
	
    $result = mysqli_query($con, $sql);
}

if ($scparam_alexa_exist == "no") {
    $sql = "insert into $tbl_name value('Alexa_YN','$scparam_alexa')";
    $result = mysqli_query($con, $sql);
} else {
    $sql = "update $tbl_name set Param_Value='$scparam_alexa' where Param_Name='Alexa_YN'";
	
    $result = mysqli_query($con, $sql);
}
 
echo "<div class='alert alert-info alert-dismissible' role='alert'>Configuration has been updated. You may need to refresh to see changes ( Press F5)";
echo "</div>";

mysqli_close($con);

ob_end_flush();

?>
