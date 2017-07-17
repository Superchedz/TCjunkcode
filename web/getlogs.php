<?php
ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}
include 'error.php';
include 'db.php';
include 'helper.php';


$scparam_period = GetInputFromRequest('period');

$scparam_period = mysqli_real_escape_string($con, $scparam_period);

$sql = "select * from log order by Log_Time desc";

if ($scparam_period == -1){
    $sql = "select * from log order by Log_Time desc";    
}
else
{
    $scparam_period = 0-$scparam_period;
    $sql = "select * from log where Log_Time>= date_add(current_date(), interval $scparam_period hour) order by Log_Time desc";
}

$result = mysqli_query($con, $sql);

if ($result->num_rows > 0) {
    echo "<table class='table table-striped table-condensed'>";
    echo "<tr class='danger'>";
    echo "<td>Date</td>";
    echo "<td>From</td>";
    echo "<td>Text</td>";
    echo "</tr>";

    while ($row = $result->fetch_assoc()) {

        echo "<tr>";
        echo "<td style='vertical-align:middle'>";
        echo $row["Log_Time"];;
        echo "</td>";

        echo "<td style='vertical-align:middle'>";
        echo $row["Log_From"];;
        echo "</td>";

        echo "<td style='vertical-align:middle'>";
        echo $row["Log_Text"];;
        echo "</td>";

        echo "</tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}

mysqli_free_result($result);
mysqli_close($con);

ob_end_flush();
?>