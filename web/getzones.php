<?php
ob_start();

session_start();
if (!isset($_SESSION['myemail'])) {
    header('Location:index.php?err=invalidsession');
}
include 'error.php';
include 'db.php';
include 'helper.php';

$sql = "select * from zone_b left outer join (select zone_id as zid, Override_start, Override_end, Override_Temp, Override_Duration_mins from override_b where override_b.Override_start <= now() and Override_end >=now()) B on zone_b.Zone_ID = B.zid left outer join  (select schedule_zone_id as zid, Schedule_Day, Schedule_Starttime, Schedule_Endtime, Schedule_Temp from schedule_b where lcase(Schedule_Day) = LCASE(DayName(NOW())) and schedule_b.Schedule_Starttime <= current_time and schedule_b.Schedule_Endtime >= current_time) C on zone_b.Zone_ID = C.zid order by Zone_ID";
$result = mysqli_query($con, $sql);

if ($result->num_rows > 0) {
    echo "<table class='table table-striped table-condensed'>";
    echo "<tr class='danger'>";
    echo "<td>Delete?</td>";
//    echo "<td>Zone Id</td>";
    echo "<td>Zone Name</td>";
    echo "<td>Zone Enabled?</td>";
    echo "<td>Zone Status</td>";
    echo "<td> Boost</td>";
    echo "<td> Extend</td>";
    echo "<td>Schedule</td>";
    echo "<td>Zone Info</td>";
    echo "</tr>";

    while ($row = $result->fetch_assoc()) {

 //       echo "<tr>";
        $zoneid = $row["Zone_ID"];
 //
 //       echo "<td style='vertical-align:middle'>";
 //       echo "<img src='./img/deletered.png' class='img-thumbnail img-responsive' data-toggle='modal' data-target='#myModalDelete'  data-zoneid='" .
 //           $row["Zone_ID"] . "' data-zonename='" . $row["Zone_Name"] . "' alt='Delete'>";
 //       echo "</td>";


 //       echo "<td style='vertical-align:middle'>";
 //       echo $zoneid;
 //       echo "</td>";

        $zonename = $row["Zone_Name"];
        echo "<td style='vertical-align:middle'>";
        echo $zonename;
        
        $pipinnum = $row["Pi_Pin_num"];
        if ($pipinnum == ""){
            $pipinnum = 0;
        }
        echo "<button class='btn btn-link' data-toggle='modal' data-target='#myModalZoneConfig'  data-zoneid='" .
            $row["Zone_ID"] . "' data-zonename='" . $row["Zone_Name"] .
            "' data-zonesensor='" . $row["Zone_Sensor_ID"] . "' data-zoneoffset='" . $row["Zone_Offset"] .
            "' data-pinnum='" . $pipinnum ."'>Settings</button>";

        echo "</td>";

        $active = $row["Zone_Active_Ind"];
        echo "<td style='vertical-align:middle'>";

        echo "            <div class='onoffswitchn'>";
        echo "                <input type='checkbox' name='onoffswitchn" . $zoneid .
            "' class='onoffswitchn-checkbox' id='myonoffswitchn" . $zoneid .
            "' onchange=zoneStatusChanged('Zone_Active_Ind','myonoffswitchn" . $zoneid .
            "','" . $zoneid . "') ";
        if ($active == "Y") {
            echo "checked ";
        } else {
            echo "";
        }
        echo "                 ><label class='onoffswitchn-label' for='myonoffswitchn" .
            $zoneid . "'>";
        echo "                    <span class='onoffswitchn-inner'></span>";
        echo "                    <span class='onoffswitchn-switch'></span>";
        echo "                </label>";
        echo "            </div>";

        echo "</td>";

        $currentstauts = $row["Zone_Current_State_Ind"];

        //                    echo "<td style='vertical-align:middle'>";
        //echo "            <div class='onoffswitchn1'>";
        //echo "                <input type='checkbox' name='onoffswitchx".$zoneid."' class='onoffswitchn1-checkbox' id='myonoffswitchx".$zoneid."' onchange=zoneStatusChanged('Zone_Current_State_Ind','myonoffswitchx".$zoneid."','".$zoneid."') ";
        //                    if ($currentstauts == "ON"){
        //                        echo "checked ";
        //                    }
        //                    else{
        //                        echo "";
        //                    }
        //echo "                 ><label class='onoffswitchn1-label' for='myonoffswitchx".$zoneid."'>";
        //echo "                    <span class='onoffswitchn1-inner'></span>";
        //echo "                    <span class='onoffswitchn1-switch'></span>";
        //echo "                </label>";
        //echo "            </div>";
        //                    echo "</td>";

        $temper = $row["Zone_Last_Temp_Reading"];
        $override = $row["Override_Temp"];
        $schedule = $row["Schedule_Temp"];
        $lastdate = $row["Zone_Last_Temp_Reading_Dtime"];
		$battpct  = $row["Zone_Sensor_Batt_pcnt"];


        echo "<td style='text-align:center; vertical-align:middle'>";
        if ($currentstauts == "ON") {
            echo "<img src='./img/on.png' class='img-thumbnail img-responsive' alt='Current State'>";
        } else {
            echo "<img src='./img/off.png' class='img-thumbnail img-responsive' alt='Current State'>";
        }
        echo "</td>";

        echo "<td style='text-align:center; vertical-align:middle'>";
        if ($active == "Y") {
            echo "<img src='./img/boostenable.png' class='img-thumbnail' data-toggle='modal' data-target='#myModalBoost'  data-zoneid='" .
                $row["Zone_ID"] . "' data-zonename='" . $row["Zone_Name"] . "'alt='Boost'>";
        } else {
            echo "<img src='./img/boostdisable.png' class='img-thumbnail' alt='Boost'>";
        }
        echo "</td>";
        echo "<td style='text-align:center; vertical-align:middle'>";
        if ($active == "Y" && $schedule == "" && $override == "") {
            echo "<img src='./img/extendenable.png' class='img-thumbnail' data-toggle='modal' data-target='#myModalExtend'  data-zoneid='" .
                $row["Zone_ID"] . "' data-zonename='" . $row["Zone_Name"] .
                "' data-currentexpiry='Boost until " . $row["Override_end"] . "'alt='Extend'>";
        } else {
            echo "<img src='./img/extenddisable.png' class='img-thumbnail' alt='Boost'>";
        }
        echo "</td>";
        echo "<td style='vertical-align:middle'>";
        echo "<img src='./img/appointment.jpg' class='img-thumbnail' data-toggle='modal' data-target='#myModalSchedule'  data-zoneid='" .
            $row["Zone_ID"] . "' data-zonename='" . $row["Zone_Name"] . "' alt='Schedule'>";
        echo "</td>";


        echo "<td style='vertical-align:middle'>";

            echo "<table>";
            echo "<tr>";
            echo "<td>";
            echo "Temp: <span class='badge'>";
            echo $temper;
            echo "&deg;C</span>";
			echo "Batt%: <span class='badge'>";
			echo $battpct;
            echo "</td>";
            echo "</tr>";
			
			
			
			
        if ($active == "Y") {
            echo "<tr>";
            echo "<td>";
            echo "Boost <span class='badge'>";
            if ($override <> "") {
                echo $override;
                echo "&deg;C ";
                echo "</span> / ";
                echo strstr($row["Override_end"], ' ');
            } else {
                echo "-";
                echo "</span> ";
            }
            echo " / ";
            echo "<button type='button' onclick=clearalloverrides(" . $zoneid .
                ") class='btn btn-danger btn-xs'>Clear</button>";
            echo "<br/>";
            echo "</td>";
            echo "</tr>";
            echo "<tr>";
            echo "<td>";
            echo "Target <span class='badge'>";
            if ($schedule <> "") {
                echo $schedule;
                echo "&deg;C";
            } else {
                echo "-";
            }
            echo "</span>";
            //echo "<span class='label label-info'>updated: ";
            //echo $lastdate;
            echo "</td>";
            echo "</tr>";
        }
            
            echo "</table>";
            //echo "</span>";

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