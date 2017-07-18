<?php 
session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

if (isset($_SESSION['myname'])) {
    $name = $_SESSION['myname'];
} else {
    header('Location:index.php?err=invalidsession');
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<link rel="shortcut icon" href="heat.ico" />
<!-- Meta, title, CSS, favicons, etc. -->
<meta charset="utf-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="Total Control 9000 - Home"/>
<meta name="keywords" content="Total Control 9000, Temperature Adjustments"/>
<meta name="author" content="NagaKishore Movva"/>

<title>
   Total Control 9000 - Home
</title>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="./bs/css/bootstrap.min.css"/>
<link rel="stylesheet" href="./bs/css/bootstrap-timepicker.min.css" />

<!-- Optional theme -->
<link rel="stylesheet" href="./bs/css/bootstrap-theme.min.css" id="bs-theme-stylesheet"/>
<!-- Documentation extras -->
<link href="./bs/css/docs.min.css" rel="stylesheet"/>
<link rel="stylesheet" href="./bs/custom.css"/>

<!--[if lt IE 9]><script src="../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
<script src="./bs/js/ie-emulation-modes-warning.js"></script>
<script src="./bs/custom.js"></script>

</head>

<body>
<a id="skippy" class="sr-only sr-only-focusable" href="#content"><div class="container"><span class="skiplink-text">Skip to main content</span></div></a>
 <header class="navbar navbar-static-top bs-docs-nav" id="top" role="banner">
  <div class="container">
    <div class="navbar-header">
      <button class="navbar-toggle collapsed" type="button" data-toggle="collapse" data-target=".bs-navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a href="#" class="navbar-brand">Total Control</a>
    </div>
    <nav class="collapse navbar-collapse bs-navbar-collapse">
      <ul class="nav navbar-nav">
        <li class="active"> 
          <a href="./home.php">Home</a>
        </li>
      </ul>
      
      
      <ul class="nav navbar-nav navbar-right">
        <li>
            <div class="onoffswitch">
                <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="myonoffswitch" 
                     <?php

ob_start();
$tbl_name = "params_b"; // Table name 2
include 'db.php';

$sql = "SELECT * FROM $tbl_name where Param_Name='sysstatus'";
$result = mysqli_query($con, $sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        if ($row["Param_Value"] == "true") {
            echo " checked ";
        }
    }
} else {
    echo " ";
}
?> onchange="sysStatusChanged()"
                            >
                <label class="onoffswitch-label" for="myonoffswitch">
                    <span class="onoffswitch-inner"></span>
                    <span class="onoffswitch-switch"></span>
                </label>
                
            </div>
        </li>
        <li>
            <button type="button" class="btn btn-link" data-toggle="modal" data-target="#myModal" data-whatever="sysconfig"> <img src='./img/cog.png' class='img-responsive' alt='Configuration'/></button>
        </li>
        <li>
            <button type="button" class="btn btn-link" data-toggle="modal" data-target="#myModalshutdown" data-whatever="shutdown"> <img src='./img/shutdown.png' class='img-responsive' alt='Shutdown'/></button>
        </li>
        <li>
            <a href="localtemp.php"><img src='./img/weatheri.png'></a>
        </li>
        <li>
        <a href="#"> 
          <?php
if (isset($_SESSION['myname'])) {
    echo $name;
}
?>
        </a>
        </li>
        <li>
            <div style="margin-top: 8px;">
            <div class="dropdown">
              <button class="btn btn-link dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
                Administration
                <span class="caret"></span>
              </button>
              <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
                <li role="presentation"><a role="menuitem" tabindex="-1" data-toggle="modal" data-target="#myModalChangePassword">Change Password</a></li>
              </ul>
            </div>
            </div>
        </li>
        <li><a href="logout.php">Logout</a></li>
      </ul>
    </nav>
  </div>
</header>

<div class="jumbotron" id="content">
    <div class="container">
          <p><img src='./img/translogo.png' class='img-thumbnail img-responsive' alt='Home'/> Total Control 9000 - manage the system settings, monitor active zones and set controls<BR>          (Release v1.2) </p>
    </div>
</div>


<div class="container">
    <div class="panel panel-success">
      <div class="panel-heading">
      <table style="width:100%">
      <tr>
      <td style="width:60%">
      <H3>My Zones</H3>
      </td>
      <td>
      <div style="float: right;">
      <a role="button" class="btn btn-link" data-toggle="modal" data-target="#myModalLogs"><img src='./img/log.png' class='img-thumbnail img-responsive' alt='Home'/>View Logs</a>
      <a role="button" class="btn btn-link"  href="dashboard.php"><img src='./img/bar-chart-icon.png' class='img-thumbnail img-responsive' alt='Home'/>Temperature Graphs</a>
      </div>
      </td>
      </tr>
      </table>
      </div>
        <div class="table-responsive">
        <div id="placeholderzones"> </div>
      <div>
      <button type="button" class="btn btn-link" data-toggle="modal" data-target="#myModalAddZone">Add New Zone</button>
      </div>
      </div>
    </div>
</div>

<footer class="bs-docs-footer" role="contentinfo">
  <div class="container">
    <p>Total Control 9000 v1.10 - Designed and Developed by the Total Control 9000 team</p>
    </div>
</footer>

<!-- Modals -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myForgotPwdLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwdLabel">System Settings</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv"> </span>
      <form class="form-horizontal">

            <div id="sysconfigcontent" class="sysconfigcontent"></div>
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitConfig()" class="btn btn-primary">Apply Changes</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalSchedule" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd1Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd1Label">Schedule</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdivschedule"> </span>
        <div class="btn-group"> <a id="lnkScheduleSelect" class="btn btn-default dropdown-toggle btn-select" data-toggle="dropdown" href="#">Select Weekday<span class="caret"></span></a>
            <ul class="dropdown-menu">
                <li><a onclick="daySelected('Monday');">Monday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Tuesday');">Tuesday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Wednesday');">Wednesday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Thursday');">Thursday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Friday');">Friday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Saturday');">Saturday</a></li>
                <li class="divider"></li>
                <li><a onclick="daySelected('Sunday');">Sunday</a></li>
            </ul>
        </div>   
      <input type="hidden" id="hdnzoneid">
      
      <form class="form-horizontal">
            <div id="schedulecontent" class="schedulecontent"></div>
      </form>
      </div>
      <div class="modal-footer">
      <div class="addnewpart">
        <table class="table table-condensed">
        <tr>
        <td style="vertical-align:middle">
        
         <input type="time" class="form-control" id="timepicker1" value="00:00">            

        </td>
        <td style="vertical-align:middle">
        
         <input type="time" class="form-control" id="timepicker2" value="00:00">            

        </td>
        <td style="vertical-align:middle">
        
         <input type="number" class="form-control" id="scparam_temp" value="">
        
        </td>
        <td>&deg;C</td>
        <td style="vertical-align:middle">
            <button type="button" onclick="addNewSchedule()" class="btn btn-primary">Add New</button>
        </td>
        </tr>
        </table>
        
        <table  class="table table-condensed">
        <tr>
        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chkmonday" checked>
                MON
              </label>
            </div>        
        </td>


        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chktuesday" checked>
                TUE
              </label>
            </div>        
        </td>

        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chkwednesday" checked>
                WED
              </label>
            </div>        
        </td>

        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chkthursday" checked>
                THU
              </label>
            </div>        
        </td>
        <td></td>
        </tr>
        <tr>
        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chkfriday" checked>
                FRI
              </label>
            </div>        
        </td>

        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chksaturday" checked>
                SAT
              </label>
            </div>        
        </td>

        <td>
         <div class="checkbox">
              <label>
                <input type="checkbox" id="chksunday" checked>
                SUN
              </label>
            </div>        
        </td>
        <td></td>
        <td>
        <button type="button" onclick="copySchedule()" class="btn btn-primary">Copy Schedule</button>
        </td>

        </tr>
        
        </table>
        
        
      </div>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalLogs" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd51Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd51Label">View Logs</h4>
      </div>

      <div class="modal-body">
        <div class="btn-group"> <a id="lnkPeriod" class="btn btn-default dropdown-toggle btn-select" data-toggle="dropdown" href="#">Select Period<span class="caret"></span></a>
            <ul class="dropdown-menu">
                <li><a onclick="GetLogsInformation(2);">Last 2 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(6);">Last 6 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(8);">Last 8 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(16);">Last 16 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(24);">Last 24 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(48);">Last 48 Hours</a></li>
                <li class="divider"></li>
                <li><a onclick="GetLogsInformation(-1);">All</a></li>
            </ul>
            <div id="placeholderpregress"></div>
        </div>   

      
      <form class="form-horizontal">
      <br />
        <div style="height: 250px;overflow:auto;">
        <div class="table-responsive">
            <div id="placeholderlogs"> </div>
        </div>
        </div>
      </form>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalBoost" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd2Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd2Label">Boost</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv123"> </span>
      <input type="hidden" id="hdnzoneid1">
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='timepickerboost' class='col-sm-4 control-label'>Boost For Another </label>
        <div class='col-sm-3'>
            <input type="time" class="form-control" id="timepickerboost" value="01:00">
        </div>
        <div class='col-sm-2'>
            <label for='scparam_boostfor1' class='col-sm-6 control-label'>Hrs:Mins</label>
        </div>
    </div>
    
    <div class='form-group'>
        <label for='scparam_boostfordegree' class='col-sm-4 control-label'>at</label>
        <div class='col-sm-2'>
            <input type='number' class='form-control' id='scparam_boostfordegree' value="">
        </div>
        <div class='col-sm-2'>
            <label for='scparam_boostfordegree1' class='col-sm-6 control-label'>&deg;C</label>
        </div>
    </div>

    <div class="checkbox">
      <label>
        <input type="checkbox" id="applytoallzones" value="">
        Apply to all zones
      </label>
    </div>
        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitBoostConfig()" class="btn btn-primary">Apply</button>
      </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalZoneConfig" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd3Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd3Label">Boost</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv1234"> </span>
      <input type="hidden" id="hdnzoneid2">
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_zonename' class='col-sm-4 control-label'>Zone Name</label>
        <div class='col-sm-4'>
            <input type='text' class='form-control' id='scparam_zonename'>
        </div>
    </div>

    <div class='form-group'>
    <label for='scparam_zonesensor' class='col-sm-4 control-label'>Sensor</label>
        <div class='col-sm-4'>
            <input type='text' class='form-control' id='scparam_zonesensor'>
        </div>
    </div>

    <div class='form-group'>
    <label for='scparam_pinnum' class='col-sm-4 control-label'>Pin Num (Pi)</label>
        <div class='col-sm-2'>
            <input type='number' class='form-control' id='scparam_pinnum'>
        </div>
    </div>

    <div class='form-group'>
        <label for='scparam_offset' class='col-sm-4 control-label'>Offset</label>
        <div class='col-sm-2'>
            <input type='number' class='form-control' id='scparam_offset' value="0">
        </div>
        <div class='col-sm-2'>
            <label for='scparam_offset1' class='col-sm-6 control-label'>&deg;C</label>
        </div>
    </div>

        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitZoneConfig()" class="btn btn-primary">Apply</button>
      </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalExtend" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd4Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd4Label">Extend</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv12345"> </span>
      <input type="hidden" id="hdnzoneid3">
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_extendperiod' class='col-sm-12 control-label'>Are you sure you wish to extend until next schedule for this zone?</label>
    </div>

        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitZoneExtend()" class="btn btn-primary">Extend</button>
      </div>
    </div>
  </div>
</div>



<div class="modal fade" id="myModalshutdown" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd4Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd4Label">Shutdown System</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv12345shutdown"> </span>
      <input type="hidden" id="hdnzoneid3">
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_extendperiod' class='col-sm-12 control-label'>Select to Shutdown or Restart the system?</label>
    </div>

        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
        <button type="button" onclick="submitShutdown()" class="btn btn-primary">Shutdown</button>
		<button type="button" onclick="submitRestart()" class="btn btn-primary">Restart</button>
      </div>
    </div>
  </div>
</div>









<div class="modal fade" id="myModalChangePassword" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd5Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd5Label">Change Password</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv123456"> </span>
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_oldpassword' class='col-sm-4 control-label'>Old Password</label>
        <div class='col-sm-4'>
            <input type='password' class='form-control' id='scparam_oldpassword' value="">
        </div>
    </div>


    <div class='form-group'>
        <label for='scparam_Newpassword' class='col-sm-4 control-label'>New Password</label>
        <div class='col-sm-4'>
            <input type='password' class='form-control' id='scparam_Newpassword' value="">
        </div>
    </div>


    <div class='form-group'>
        <label for='scparam_Newpassword1' class='col-sm-4 control-label'>Repeat New Password</label>
        <div class='col-sm-4'>
            <input type='password' class='form-control' id='scparam_Newpassword1' value="">
        </div>
    </div>
        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="changePassword()" class="btn btn-primary">Change Password</button>
      </div>
    </div>
  </div>
</div>



<div class="modal fade" id="myModalAddZone" tabindex="-1" role="dialog" aria-labelledby="AddZoneLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="AddZoneLabel">New Zone</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv1234Add"> </span>
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_addzonename' class='col-sm-4 control-label'>Zone Name</label>
        <div class='col-sm-4'>
            <input type='text' class='form-control' id='scparam_addzonename'>
        </div>
    </div>

    <div class='form-group'>
    <label for='scparam_addzonesensor' class='col-sm-4 control-label'>Sensor</label>
        <div class='col-sm-4'>
            <input type='text' class='form-control' id='scparam_addzonesensor'>
        </div>
    </div>

    <div class='form-group'>
    <label for='scparam_addpinnum' class='col-sm-4 control-label'>Pin Num (Pi)</label>
        <div class='col-sm-2'>
            <input type='number' class='form-control' id='scparam_addpinnum'>
        </div>
    </div>    

    <div class='form-group'>
        <label for='scparam_addoffset' class='col-sm-4 control-label'>Offset</label>
        <div class='col-sm-2'>
            <input type='number' class='form-control' id='scparam_addoffset' value="0">
        </div>
        <div class='col-sm-2'>
            <label for='scparam_addoffset1' class='col-sm-6 control-label'>&deg;C</label>
        </div>
    </div>
    
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitNewZoneConfig()" class="btn btn-primary">Create New</button>
      </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalDelete" tabindex="-1" role="dialog" aria-labelledby="myForgotPwd14Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwd14Label">Delete</h4>
      </div>

      <div class="modal-body">
      <span id="mysysconfigdiv12345Delete"> </span>
      <input type="hidden" id="hdnzoneid3del">
      <form class="form-horizontal">

    <div class='form-group'>
        <label for='scparam_deletezone' class='col-sm-12 control-label'>Are you sure you wish to delete this zone?</label>
    </div>

        
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="submitZoneDelete()" class="btn btn-primary">Confirm</button>
      </div>
    </div>
  </div>
</div>

<script src="./bs/jquery.min.js"></script>
<script src="./bs/js/bootstrap.min.js"></script>
<script src="./bs/js/bootstrap-timepicker.min.js"></script>
<script src="./bs/js/docs.min.js"></script>
<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="./bs/js/ie10-viewport-bug-workaround.js"></script>
<script src="./bs/homedocend.js"></script>
</body>
</html>