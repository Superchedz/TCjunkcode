<?php

function GetInputFromRequest($value)
{
    $inputval = $_GET[$value];
    $inputval = stripslashes($inputval);
    return $inputval;
}

function GetInputFromRequestPost($value)
{
    $inputval = $_POST[$value];
    $inputval = stripslashes($inputval);
    return $inputval;
}

?>
