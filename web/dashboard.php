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
<meta name="description" content="Total Control 9000 - Home"/>
<meta name="keywords" content="Total Control 9000, Temperature Adjustments"/>
<meta name="author" content="NagaKishore Movva"/>

<title>
   Total Control 9000 - Dashboard
</title>
<link rel="stylesheet" href="./bs/css/bootstrap.min.css"/>
<link rel="stylesheet" href="./bs/css/bootstrap-theme.min.css" id="bs-theme-stylesheet"/>
<link href="./bs/css/docs.min.css" rel="stylesheet"/>
<link rel="stylesheet" href="./bs/custom.css"/>
<!--[if lt IE 9]><script src="../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
<script src="./bs/js/ie-emulation-modes-warning.js"></script>
<script src="./bs/custom.js"></script>
<script src="./bs/Chart.min.js"></script>
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
      <a href="./home.php" class="navbar-brand">Total Control</a>
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
    <h3>Temperature History
    </h3>
    </div>
</div>

<div class="container">
		
        <div class="col-md-12">
			<div>
				<canvas id="canvas" height="200" width="600"></canvas>
			</div>
			<div id="templegend"></div>
		</div>
        
	<script>
		var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
		var lineChartData = {

        <?php

include 'error.php';
include 'db.php';
include 'helper.php';

$sql = "call last24hourdashboard();";
$result = mysqli_query($con, $sql);
$labelresult = "labels : [";
$dataresult = "datasets : [";
$dataset = "";
$zone = 0;
$firstzone = 0;
$firstcolor = 131;
$secondcolor = 167;
$thirdcolor = 185;

while ($row = $result->fetch_assoc()) {
    if ($zone == 0) {
        $firstzone = $row["Zone_ID"];
    }
    if ($zone != $row["Zone_ID"]) {
        if ($zone != 0) {
            $dataset .= "]},";
            $dataresult .= $dataset;
            $dataset = "";
        }
    }

    if ($zone != $row["Zone_ID"]) {
        if ($row["Zone_ID"] == 1) {
            $firstcolor = "0";
            $secondcolor = "255";
            $thirdcolor = "204";
        } else
            if ($row["Zone_ID"] == 2) {
                $firstcolor = "51";
                $secondcolor = "153";
                $thirdcolor = "255";
            } else
                if ($row["Zone_ID"] == 3) {
                    $firstcolor = "255";
                    $secondcolor = "153";
                    $thirdcolor = "204";
                } else
                    if ($row["Zone_ID"] == 4) {
                        $firstcolor = "153";
                        $secondcolor = "255";
                        $thirdcolor = "153";
                    } else
                        if ($row["Zone_ID"] == 5) {
                            $firstcolor = "255";
                            $secondcolor = "255";
                            $thirdcolor = "102";
                        } else
                            if ($row["Zone_ID"] == 6) {
                                $firstcolor = "51";
                                $secondcolor = "204";
                                $thirdcolor = "51";
                            } else
                                if ($row["Zone_ID"] == 7) {
                                    $firstcolor = "255";
                                    $secondcolor = "153";
                                    $thirdcolor = "0";
                                } else
                                    if ($row["Zone_ID"] == 8) {
                                        $firstcolor = "204";
                                        $secondcolor = "0";
                                        $thirdcolor = "102";
                                    } else
                                        if ($row["Zone_ID"] == 9) {
                                            $firstcolor = "204";
                                            $secondcolor = "0";
                                            $thirdcolor = "204";
                                        } else
                                            if ($row["Zone_ID"] == 10) {
                                                $firstcolor = "51";
                                                $secondcolor = "51";
                                                $thirdcolor = "0";
                                            }

        $dataset .= "{ label: '";
        $dataset .= $row["Zone_ID"];
        $dataset .= "-";
        $dataset .= $row["Zone_Name"];
        $dataset .= "',";
        $dataset .= "fillColor : 'rgba($firstcolor,$secondcolor,$thirdcolor,0.2)',";
        $dataset .= "strokeColor : 'rgba($firstcolor,$secondcolor,$thirdcolor,1)',";
        $dataset .= "pointColor : 'rgba($firstcolor,$secondcolor,$thirdcolor,1)',";
        $dataset .= "pointStrokeColor : '#fff',";
        $dataset .= "pointHighlightFill : '#fff',";
        $dataset .= "pointHighlightStroke : 'rgba($firstcolor,$secondcolor,$thirdcolor,1)',";
        $dataset .= "data : [";
        $firstcolor = $firstcolor + ($row["Zone_ID"] * 10);
        $secondcolor = $secondcolor + ($row["Zone_ID"] * 10);
        $thirdcolor = $thirdcolor + ($row["Zone_ID"] * 10);
        $dataset .= $row["avgtemp"];
        $dataset .= ",";
    } else {
        $dataset .= $row["avgtemp"];
        $dataset .= ",";
    }

    if ($firstzone == $row["Zone_ID"]) {
        $labelresult .= "'";
        $labelresult .= $row["hourvalue"];
        $labelresult .= ":00";
        $labelresult .= "',";
    }

    $zone = $row["Zone_ID"];
}

$dataset .= "]},";
$dataresult .= $dataset;
$dataset = "";


$dataresult .= "]";
$labelresult .= "],";
echo $labelresult;
echo $dataresult;
mysqli_free_result($result);
mysqli_close($con);
?>

		}

	window.onload = function(){
		var ctx = document.getElementById("canvas").getContext("2d");
		window.myLine = new Chart(ctx).Line(lineChartData, {
			responsive: true
			  
		});

        legend(document.getElementById("templegend"), lineChartData);


	}

    </script>

</div>

<footer class="bs-docs-footer" role="contentinfo">
  <div class="container">
    <p>For futher info and support visit <a href="http://www.totalcontrol9000.co.uk" target="_blank">Our Website</a></p>
    </div>
</footer>

<script src="./bs/jquery.min.js"></script>
<script src="./bs/js/bootstrap.min.js"></script>
<script src="./bs/js/docs.min.js"></script>
<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="./bs/js/ie10-viewport-bug-workaround.js"></script>
</body>
</html>