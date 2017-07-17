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
$scparam_zoneid = GetInputFromRequest('zone');

$scparam_daytoretrieve = mysqli_real_escape_string($con, $scparam_daytoretrieve);
$scparam_zoneid = mysqli_real_escape_string($con, $scparam_zoneid);


$sql = "SELECT * FROM $tbl_name where Schedule_Zone_ID = $scparam_zoneid and Schedule_Day = '$scparam_daytoretrieve'";
$result = mysqli_query($con, $sql);

echo "<br />";
echo "<div class='table-responsive'>";
echo "          <table class='table table-striped table-condensed'>";
echo "                <tr class='danger'>";
echo "                <td>From Time</td>";
echo "                <td>To Time</td>";
echo "                <td>Temperature</td>";
echo "                <td>Delete?</td>";
echo "                </tr>";

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        $starttime = $row["Schedule_Starttime"];
        $endtime = $row["Schedule_Endtime"];
        $temperature = $row["Schedule_Temp"];

        echo "<td style='vertical-align:middle'>";
        echo $starttime;
        echo "</td>";

        echo "<td style='vertical-align:middle'>";
        echo $endtime;
        echo "</td>";

        echo "<td style='vertical-align:middle'>";
        echo $temperature . " &deg;C";
        echo "</td>";

        echo "<td style='vertical-align:middle'>";
        echo "<a onclick=deleteSchedule('" . $starttime .
            "')><img src='./img/deletered.png' class='img-thumbnail img-responsive' alt='Delete'></a>";
        echo "</td>";


        echo "</tr>";
    }
}
echo "</table>";
$count = mysqli_num_rows($result);
echo "<input type='hidden' id='hdnCount' value='$count'>";
echo "</div>";

mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();

?>
