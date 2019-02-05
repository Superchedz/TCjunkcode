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
$AlexaYN = "";
$Interval = 0;
$FromEmail = "";
$ToEmail = "";
$SMTPServer = "";
$SMTPPwd = "";
$FrozenVal = 0;
$LogRetention = 0;
$YPlan = "";
$YPlan_ch_zone = 0;
$YPlan_hw_zone = 0;
$YPlan_gpio = 0;
$WebAddr = "";
$NGROK = "Not Set";

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
        if ($row["Param_Name"] == "Ext_Web_Address") {
            $WebAddr = $row["Param_Value"];
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
		
        if ($row["Param_Name"] == "YPlan_YN") {
            $YPlan = $row["Param_Value"];
        }
		
        if ($row["Param_Name"] == "YPlan_CH_Zone") {
            $YPlan_ch_zone = $row["Param_Value"];
        }
        if ($row["Param_Name"] == "YPlan_HW_Zone") {
            $YPlan_hw_zone = $row["Param_Value"];
        }
        if ($row["Param_Name"] == "YPlan_GPIO") {
            $YPlan_gpio = $row["Param_Value"];

        }	
        if ($row["Param_Name"] == "Alexa_YN") {
            $AlexaYN = $row["Param_Value"];

        }        
        if ($row["Param_Name"] == "NGROK_address") {
            $NGROK = $row["Param_Value"];
        }
    }
}


echo "  <div class='form-group'>";
echo "    <label for='scparam_ngrok' class='col-sm-4 control-label'>Alexa Endpoint</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='text' class='form-control' id='scparam_ngrok' placeholder='Alexa Endpoint' value='" .
    $NGROK . "'>";
echo "    </div>";
echo "  </div>";




echo "<form class='form-vertical'>";
echo "  <div class='form-group'>";
echo "    <label for='scparam_polinterval' class='col-sm-4 control-label'>Polling Interval</label>";
echo "    <div class='col-sm-2'>";
echo "      <input type='number' class='form-control' id='scparam_polinterval' placeholder='Polling Interval' value='" . $Interval . "'>";
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
echo "      <input type='password' class='form-control' id='scparam_emailpwd' placeholder='Password' value='" .
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
echo "    <label for='scparam_webaddr' class='col-sm-4 control-label'>Your External web address</label>";
echo "    <div class='col-sm-8'>";
echo "      <input type='text' class='form-control' id='scparam_webaddr' placeholder='External Web address' value='" .
    $WebAddr . "'>";
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

echo "    <label for='scparam_frost1' class='col-sm-2 text-nowrap control-label'>Deg(&deg;C)</label>";
echo "    <div class='col-sm-4'>";
echo "  </div>";
echo "  </div>";


echo "  <div class='form-group'>";
echo "    <label for='scparam_frost' class='col-sm-10 text-left control-label'>A reboot is required if any of the below fields are changed.</label>";
echo "  </div>";




echo "<div class='form-group'>";
echo "  <label for='scparam_alexa' class='col-sm-5 control-label'>Alexa Enabled</label>";
echo "    <div class='col-sm-7'>";
echo "  <select id='scparam_alexa' name='scparam_alexa'>"; 

if ($AlexaYN == 'Y')
{
	echo "     <option value='Y' selected>Y</option>";
}
else{
	echo "     <option value='Y'>Y</option>";
}

if ($AlexaYN == 'N')
{
	echo "     <option value='N' selected>N</option>";
}
else{
	echo "     <option value='N'>N</option>";
}

echo "  </select>";
echo "   </div>";
echo "</div>";  
 






echo "<div class='form-group'>";
echo "  <label for='scparam_yplan' class='col-sm-5 control-label'>Plan Type</label>";
echo "    <div class='col-sm-7'>";
echo "  <select id='scparam_yplan' name='scparam_yplan'>"; 
echo "     <option value='0'>Select a value--</option>";
if ($YPlan == 'Y')
{
	echo "     <option value='Y' selected>Y-Plan</option>";
}
else{
	echo "     <option value='Y'>Y-Plan</option>";
}
if ($YPlan == 'N')
{
	echo "     <option value='N' selected>S-Plan/None</option>";
}
else{
	echo "     <option value='N'>S-Plan/None</option>";
}
echo "  </select>";
echo "</div>";
echo "</div>";

echo "<div class='form-group'>";
echo "  <label for='scparam_yplanchzone' class='col-sm-5 control-label'>YPlan CH Zone</label>";
echo "    <div class='col-sm-7'>";
$tbl_name1 = "zone_b"; // Table name
$sql1 = "SELECT Zone_ID, Zone_Name FROM $tbl_name1";
$result1 = mysqli_query($con, $sql1);
echo "<select id='scparam_yplanchzone' name='scparam_yplanchzone'>";
echo "     <option value='0'>Select  Zone--</option>";
if ($result1->num_rows > 0) {
    while ($row = $result1->fetch_assoc()) {
		if ($YPlan_ch_zone == $row["Zone_ID"])
		{
			echo "<option value='" . $row["Zone_ID"] . "' selected>";
		}
		else{
			echo "<option value='" . $row["Zone_ID"] . "'>";
		}
		echo "" . $row["Zone_Name"] . "";
		echo "</option>";
	}
}
echo "  </select>";
echo "</div>";
echo "</div>";

echo "<div class='form-group'>";
echo "  <label for='scparam_yplanhwzone' class='col-sm-5 control-label'>Y-Plan HW Zone</label>";
echo "    <div class='col-sm-7'>";
echo "<select id='scparam_yplanhwzone' name='scparam_yplanhwzone'>";

$tbl_name2 = "zone_b"; // Table name
$sql2 = "SELECT Zone_ID, Zone_Name FROM $tbl_name2";
$result2 = mysqli_query($con, $sql2);
echo "     <option value='0'>Select  Zone--</option>";
if ($result2->num_rows > 0) {
    while ($row = $result2->fetch_assoc()) {
		if ($YPlan_hw_zone == $row["Zone_ID"])
		{
			echo "<option value='" . $row["Zone_ID"] . "' selected>";
		}
		else{
			echo "<option value='" . $row["Zone_ID"] . "'>";
		}		
		echo "" . $row["Zone_Name"] . "";
		echo "</option>";
	}
}
echo "  </select>";
echo "</div>";
echo "</div>";

echo "  <div class='form-group'>";
echo "    <label for='scparam_yplan_gpio' class='col-sm-5 control-label'>Y-Plan GPIO(HW off)</label>";
echo "    <div class='col-sm-2'>";
echo "      <input type='number' class='form-control' id='scparam_yplan_gpio' placeholder='N' value='" .
    $YPlan_gpio . "'>";
echo "    </div>";
echo "    <div class='col-sm-2'>";
echo "  <label for='scparam_yplan_gpio' class='col-sm-6 control-label'></label>";
echo "  </div>";
echo "  </div>";

echo "</form>";


mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();

?>
