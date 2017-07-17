<?php
session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

$name = $_SESSION['myname'];
?>

<!DOCTYPE html>
<html lang="en">
<head>
<link rel="shortcut icon" href="heat.ico" />
<meta charset="utf-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="Boiler Control 9000 - Home"/>
<meta name="keywords" content="Boiler Control 9000, Temperature Adjustments"/>
<meta name="author" content="NagaKishore Movva"/>

<title>
   Boiler Control 9000 - Local Temperature
</title>
<link rel="stylesheet" href="./bs/css/bootstrap.min.css"/>
<link rel="stylesheet" href="./bs/css/bootstrap-theme.min.css" id="bs-theme-stylesheet"/>
<link href="./bs/css/docs.min.css" rel="stylesheet"/>
<link rel="stylesheet" href="./bs/custom.css"/>
<!--[if lt IE 9]><script src="../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
<script src="./bs/js/ie-emulation-modes-warning.js"></script>
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
      <a href="./home.php" class="navbar-brand">Boiler Control</a>
    </div>
    <nav class="collapse navbar-collapse bs-navbar-collapse">
      <ul class="nav navbar-nav">
        <li class="active"> 
          <a href="./home.php">Home</a>
        </li>
      </ul>
      <ul class="nav navbar-nav navbar-right">

        <li><a href="#"> 
      <?php
echo $name;
?>
      </a>
      </li>
        <li><a href="logout.php">Logout</a></li>
      </ul>
    </nav>
  </div>
</header>

<div class="jumbotron" id="content">
    <div class="container">
    <h3>Hello
      <?php
echo $name;
?>
      </h3>
    </div>
</div>

<div class="container">
    <a href="http://www.accuweather.com/en/gb/guildford/gu1-3/driving-current-weather/331057" class="aw-widget-legal">
    </a>
    <div id="awtd1426170069470" class="aw-widget-36hour"  data-locationkey="331057" data-unit="c" data-language="en-us" data-useip="false" data-uid="awtd1426170069470" data-editlocation="true" data-lifestyle="driving"></div><script type="text/javascript" src="http://oap.accuweather.com/launch.js"></script>
</div>

<footer class="bs-docs-footer" role="contentinfo">
  <div class="container">
    <p>Designed and Developed by <a href="https://www.facebook.com/graham.chedzoy?fref=ts" target="_blank">Graham Chedzoy</a> and <a href="https://www.facebook.com/nagakishore.movva" target="_blank">NagaKishore Movva</a>.</p>
    </div>
</footer>

<script src="./bs/jquery.min.js"></script>
<script src="./bs/js/bootstrap.min.js"></script>
<script src="./bs/js/docs.min.js"></script>
<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="./bs/js/ie10-viewport-bug-workaround.js"></script>
</body>
</html>