<?php

function customError($errno, $errstr)
{
    echo "<div class='alert alert-danger alert-dismissible' role='alert'>";
    echo "<b>Error:</b> [$errno] $errstr<br>";
    echo "</div>";
    die();
}

set_error_handler("customError");

?>
