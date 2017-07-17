<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="Total Control 9000 - Home"/>
<meta name="keywords" content="Total Control 9000, Temperature Adjustments"/>
<meta name="author" content="NagaKishore Movva"/>

<title>
   Total Control 9000 - Login
</title>

<link rel="shortcut icon" href="heat.ico" />
<link rel="stylesheet" href="./bs/css/bootstrap.min.css"/>
<link rel="stylesheet" href="./bs/css/bootstrap-theme.min.css" id="bs-theme-stylesheet"/>
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
          <a href="./index.php">Login</a>
        </li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="http://visualbasicsource.itgo.com" onclick="ga('send', 'event', 'Navbar', 'My Site', 'About');">About</a></li>
      </ul>
    </nav>
  </div>
</header>


<div class="jumbotron" id="content">
    <div class="container">
          <h1><img src='./img/logobb.png' class='img-thumbnail img-responsive' alt='Login'/>Total Control 9000</h1>
            <p>A web enabled system to allow you to manage and monitor a multi-zone heating system</p>
			<p>Authorised Access only - All Activity is logged</p>
    </div>
</div>

 
 
<div class="container">

    <?php
if (isset($_GET["err"])) {
    $error = $_GET["err"];
    $error = stripslashes($error);
    if ($error == "wrongcredentials") {
        echo "<div class='alert alert-danger alert-dismissible' role='alert'> <button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>Invalid Email Address/ Password, Please try again with valid credentials.</div>";
    } elseif ($error == "logout") {
        echo "<div class='alert alert-success alert-dismissible' role='alert'> <button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>You have been successfully logged out from Total Control 9000 portal.</div>";
    }
}
?>
    
    <form  name="form1" method="POST" action="checklogin.php">
      <div class="form-group">
        <label for="myemail">Email address</label>
        <input type="email" class="form-control" id="myemail" name="myemail" placeholder="Enter email">
      </div>
      <div class="form-group">
        <label for="mypassword">Password</label>
        <input type="password" class="form-control" id="mypassword" name="mypassword" placeholder="Password">
      </div>
      <button type="submit" class="btn btn-primary">Sign In</button>
        <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#myForgotPassword">Forgot Password?</button>
    </form>
</div>

<footer class="bs-docs-footer" role="contentinfo">
  <div class="container">
    <p>Designed and Developed by <a href="https://www.facebook.com/graham.chedzoy?fref=ts" target="_blank">Graham Chedzoy</a> and <a href="https://www.facebook.com/nagakishore.movva" target="_blank">NagaKishore Movva</a>.</p>
    </div>
</footer>


<!-- Modal -->
<div class="modal fade" id="myForgotPassword" tabindex="-1" role="dialog" aria-labelledby="myForgotPwdLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myForgotPwdLabel">Forgot Password?</h4>
      </div>

      <div class="modal-body">
            <span id="mypemaildiv">
            </span >

          <div class="form-group">
            <label for="mypemail">Email address</label>
            <input type="email" class="form-control" id="mypemail" name="mypemail" placeholder="Enter email">
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" onclick="resetPassword()" class="btn btn-primary">Send Password</button>
      </div>
    </div>
  </div>
</div>


<script src="./bs/jquery.min.js"></script>
<script src="./bs/js/bootstrap.min.js"></script>
<script src="./bs/js/docs.min.js"></script>
<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="./bs/js/ie10-viewport-bug-workaround.js"></script>
</body>
</html>