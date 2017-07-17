<?php
ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}

include 'error.php';
include 'db.php';
include 'helper.php';

$tbl_name = "schedule_b"; // Table name

$scparam_daytoretrieve = GetInputFromRequest('selectedday');
$scparam_copydays = GetInputFromRequest('copydays');
$scparam_zoneid = GetInputFromRequest('zone');

$scparam_daytoretrieve = mysqli_real_escape_string($con, $scparam_daytoretrieve);
$scparam_copydays = mysqli_real_escape_string($con, $scparam_copydays);
$scparam_zoneid = mysqli_real_escape_string($con, $scparam_zoneid);

$sql = "SELECT * FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = '$scparam_daytoretrieve'";
$result = mysqli_query($con, $sql);

if ($result->num_rows > 0) {

    $dayselect = strtolower($scparam_daytoretrieve);

    $pos = strpos($scparam_copydays, "mon");
    if ($pos !== false) {
        if ($dayselect != "monday") {
            $sql1 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Monday'";
            $result1 = mysqli_query($con, $sql1);
        }
    }

    $pos1 = strpos($scparam_copydays, "tue");
    if ($pos1 !== false) {
        if ($dayselect != "tuesday") {
            $sql2 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Tuesday'";
            $result2 = mysqli_query($con, $sql2);
        }
    }

    $pos2 = strpos($scparam_copydays, "wed");
    if ($pos2 !== false) {
        if ($dayselect != "wednesday") {
            $sql3 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Wednesday'";
            $result3 = mysqli_query($con, $sql3);
        }
    }

    $pos3 = strpos($scparam_copydays, "thu");
    if ($pos3 !== false) {
        if ($dayselect != "thursday") {
            $sql4 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Thursday'";
            $result4 = mysqli_query($con, $sql4);
        }
    }


    $pos4 = strpos($scparam_copydays, "fri");
    if ($pos4 !== false) {
        if ($dayselect != "friday") {
            $sql5 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Friday'";
            $result5 = mysqli_query($con, $sql5);
        }
    }

    $pos5 = strpos($scparam_copydays, "sat");
    if ($pos5 !== false) {
        if ($dayselect != "saturday") {
            $sql6 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Saturday'";
            $result6 = mysqli_query($con, $sql6);
        }
    }

    $pos6 = strpos($scparam_copydays, "sun");
    if ($pos6 !== false) {
        if ($dayselect != "sunday") {
            $sql7 = "DELETE FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = 'Sunday'";
            $result7 = mysqli_query($con, $sql7);
        }
    }


    while ($row = $result->fetch_assoc()) {
        $scparam_fromtime = $row["Schedule_Starttime"];
        $scparam_totime = $row["Schedule_Endtime"];
        $scparam_temp = $row["Schedule_Temp"];

        $lpos = strpos($scparam_copydays, "mon");
        if ($lpos !== false) {
            if ($dayselect != "monday") {
                $lsql1 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Monday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult1 = mysqli_query($con, $lsql1);
            }
        }

        $lpos1 = strpos($scparam_copydays, "tue");
        if ($lpos1 !== false) {
            if ($dayselect != "tuesday") {
                $lsql2 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Tuesday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult2 = mysqli_query($con, $lsql2);
            }
        }

        $lpos2 = strpos($scparam_copydays, "wed");
        if ($lpos2 !== false) {
            if ($dayselect != "wednesday") {
                $lsql3 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Wednesday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult3 = mysqli_query($con, $lsql3);
            }
        }

        $lpos3 = strpos($scparam_copydays, "thu");
        if ($lpos3 !== false) {
            if ($dayselect != "thursday") {
                $lsql4 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Thursday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult4 = mysqli_query($con, $lsql4);
            }
        }


        $lpos4 = strpos($scparam_copydays, "fri");
        if ($lpos4 !== false) {
            if ($dayselect != "friday") {
                $lsql5 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Friday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult5 = mysqli_query($con, $lsql5);
            }
        }

        $lpos5 = strpos($scparam_copydays, "sat");
        if ($lpos5 !== false) {
            if ($dayselect != "saturday") {
                $lsql6 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Saturday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult6 = mysqli_query($con, $lsql6);
            }
        }

        $lpos6 = strpos($scparam_copydays, "sun");
        if ($lpos6 !== false) {
            if ($dayselect != "sunday") {
                $lsql7 = "INSERT INTO $tbl_name value($scparam_zoneid , 'Sunday', '$scparam_fromtime', '$scparam_totime','$scparam_temp')";
                $lresult7 = mysqli_query($con, $lsql7);
            }
        }
    }

    echo "<div class='alert alert-info alert-info' role='alert'>Copied.";
    echo "</div>";
}
mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();

?>
