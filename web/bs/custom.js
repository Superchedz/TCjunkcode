function resetPassword() {
    var str = document.getElementById("mypemail").value;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById("mypemaildiv").innerHTML = xmlhttp.responseText;
            document.getElementById("mypemail").value = "";
        }
    }
    xmlhttp.open("GET", "resetpassword.php?mypemail=" + str, true);
    xmlhttp.send();
}
    
function sysStatusChanged(){
    var selected = document.getElementById("myonoffswitch").checked;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            
        }
    }
    xmlhttp.open("GET", "savesysstat.php?status=" + selected, true);
    xmlhttp.send();
}

function zoneStatusChanged(fldToUpdate,elementid, zoneid){
    var selected = document.getElementById(elementid).checked;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            ///window.location = "home.php";
            GetZonesInformation();
        }
    }
    xmlhttp.open("GET", "savezonestat.php?field=" + fldToUpdate + "&zoneid=" + zoneid + "&status=" + selected, true);
    xmlhttp.send();
}

function clearalloverrides(zoneid){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            //window.location = "home.php";
            GetZonesInformation();
        }
    }
    xmlhttp.open("GET", "clearalloverrides.php?zoneid=" + zoneid , true);
    xmlhttp.send();
}

function submitBoostConfig(){
    var zoneid = document.getElementById("hdnzoneid1").value;
    var scparam_boostfordegree = document.getElementById("scparam_boostfordegree1").value;
    var timepickerboost = document.getElementById("timepickerboost1").value;
    var boosttime = timepickerboost.split(":"); 
    if (boosttime.length < 2){
        document.getElementById("mysysconfigdiv123").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>Invalid Time.</div>";
        return false;
    }
    var scparam_boostfor = parseInt(boosttime[0]);
    var scparam_boostformin = parseInt(boosttime[1]);

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv123").innerHTML = xmlhttp.responseText;
            GetZonesInformation();
            $('#myModalBoostTemp').modal('hide');
            
        }
    }
    
    var url = "saveboost.php?zoneid=" + zoneid;

    url += "&scparam_boostfor=";
    url +=  scparam_boostfor;
    
    url += "&scparam_boostformin=";
    url +=  scparam_boostformin;

    url += "&scparam_boostfordegree=";
    url +=  scparam_boostfordegree;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function submitBoostConfigt(){
    var zoneid = document.getElementById("hdnzoneid1").value;
    var scparam_boostfordegree = document.getElementById("scparam_boostfordegree").value;
    var timepickerboost = document.getElementById("timepickerboost").value;
    var boosttime = timepickerboost.split(":"); 
    if (boosttime.length < 2){
        document.getElementById("mysysconfigdiv123").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>Invalid Timet.</div>";
        return false;
    }
    var scparam_boostfor = parseInt(boosttime[0]);
    var scparam_boostformin = parseInt(boosttime[1]);

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv123").innerHTML = xmlhttp.responseText;
            GetZonesInformation();
            $('#myModalBoostTemp').modal('hide');
        }
    }
    
    var url = "saveboost.php?zoneid=" + zoneid;

    url += "&scparam_boostfor=";
    url +=  scparam_boostfor;
    
    url += "&scparam_boostformin=";
    url +=  scparam_boostformin;

    url += "&scparam_boostfordegree=";
    url +=  scparam_boostfordegree;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


function submitZoneExtend(){
    var zoneid = document.getElementById("hdnzoneid3").value;
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv12345").innerHTML = xmlhttp.responseText;
            if (xmlhttp.responseText.indexOf("home.php") > -1)
            {
                GetZonesInformation();
                $('#myModalExtend').modal('hide');                
                //window.location = "home.php";
            }
        }

    }
    
    var url = "savextend.php?zoneid=" + zoneid;
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}





function submitZoneDelete(){
    var zoneid = document.getElementById("hdnzoneid3del").value;
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv12345Delete").innerHTML = xmlhttp.responseText;
            if (xmlhttp.responseText.indexOf("home.php") > -1)
            {
                GetZonesInformation();
                $('#myModalDelete').modal('hide');                
                //window.location = "home.php";
            }
        }

    }
     
    var url = "deletezone.php?zoneid=" + zoneid;
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


function submitShutdown(){
    var zoneid = document.getElementById("hdnzoneid3del").value;
    
    var xmlhttp = new XMLHttpRequest();
   
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv12345shutdown").innerHTML = xmlhttp.responseText;
            if (xmlhttp.responseText.indexOf("home.php") > -1)
            {
                GetZonesInformation();
                $('#myModalShutdown').modal('hide');                
                //window.location = "home.php";
            }
        }

    }
    
    var url = "shutdown.php";
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


function submitRestart(){
    var zoneid = document.getElementById("hdnzoneid3del").value;
    
    var xmlhttp = new XMLHttpRequest();
   
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv12345shutdown").innerHTML = xmlhttp.responseText;
            if (xmlhttp.responseText.indexOf("home.php") > -1)
            {
                GetZonesInformation();
                $('#myModalRestart').modal('hide');                
                //window.location = "home.php";
            }
        }

    }
    
    var url = "restart.php";
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}







function changePassword(){
    var zoneid = document.getElementById("hdnzoneid3").value;
    var scparam_oldpassword = document.getElementById("scparam_oldpassword").value;
    var scparam_Newpassword = document.getElementById("scparam_Newpassword").value;
    var scparam_Newpassword1 = document.getElementById("scparam_Newpassword1").value;
    document.getElementById("mysysconfigdiv123456").innerHTML = "";
    if (scparam_Newpassword!=scparam_Newpassword1)
    {
        document.getElementById("mysysconfigdiv123456").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>Passwords donot match.</div>";
        return false;
    }
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv123456").innerHTML = xmlhttp.responseText;
        }
    }
    
    var url = "changepassword.php?scparam_oldpassword=" + scparam_oldpassword;

    url += "&scparam_Newpassword=";
    url +=  scparam_Newpassword;
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function submitZoneConfig(){
    var zoneid = document.getElementById("hdnzoneid2").value;
    var scparam_zonename = document.getElementById("scparam_zonename").value;
    var scparam_zonesensor = document.getElementById("scparam_zonesensor").value;
    var scparam_offset = document.getElementById("scparam_offset").value;
    var scparam_zonetype = document.getElementById("scparam_zonetype").value;	
    var scparam_pinnum = document.getElementById("scparam_pinnum").value;
    
    
   var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv1234").innerHTML = xmlhttp.responseText;
            GetZonesInformation();
            $('#myModalZoneConfig').modal('hide');                
            //window.location = "home.php";
        }
    }
    
    var url = "savezoneconfig.php?zoneid=" + zoneid;

    url += "&scparam_zonename=";
    url +=  scparam_zonename;
    
    url += "&scparam_zonesensor=";
    url +=  scparam_zonesensor;

    url += "&scparam_offset=";
    url +=  scparam_offset;
    
	url += "&scparam_zonetype=";
    url +=  scparam_zonetype;
    
	url += "&scparam_pinnum=";
    url +=  scparam_pinnum;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
}

function submitNewZoneConfig(){
    var scparam_zonename = document.getElementById("scparam_addzonename").value;
    var scparam_zonesensor = document.getElementById("scparam_addzonesensor").value;
    var scparam_offset = document.getElementById("scparam_addoffset").value;
	var scparam_zonetype = document.getElementById("scparam_zonetype").value;
    var scparam_pinnum = document.getElementById("scparam_addpinnum").value;

    
    
   var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv1234Add").innerHTML = xmlhttp.responseText;
            GetZonesInformation();
            $('#myModalAddZone').modal('hide');
            //window.location = "home.php";
        }
    }
    
    var url = "savenewzoneconfig.php?";

    url += "scparam_addzonename=";
    url +=  scparam_zonename;
    
    url += "&scparam_addzonesensor=";
    url +=  scparam_zonesensor;

    url += "&scparam_addoffset=";
    url +=  scparam_offset;

    url += "&scparam_addzonetype=";
    url +=  scparam_zonetype;	
	
    url += "&scparam_addpinnum=";
    url +=  scparam_pinnum;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
}

function submitConfig() {
    var scparam_polinterval = document.getElementById("scparam_polinterval").value;
    var scparam_fromemail = document.getElementById("scparam_fromemail").value;
    var scparam_smtpserver = document.getElementById("scparam_smtpserver").value;
    var scparam_emailpwd = document.getElementById("scparam_emailpwd").value;
    var scparam_toemail = document.getElementById("scparam_toemail").value;
    var scparam_logret = document.getElementById("scparam_logret").value;
    var scparam_frost = document.getElementById("scparam_frost").value;
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById("mysysconfigdiv").innerHTML = xmlhttp.responseText;
        }
    }
    var url = "savesysconfig.php?scparam_polinterval=" + scparam_polinterval;

    url += "&scparam_fromemail=";
    url +=  scparam_fromemail;
    
    url += "&scparam_smtpserver=";
    url +=  scparam_smtpserver;

    url += "&scparam_emailpwd=";
    url +=  scparam_emailpwd;

    url += "&scparam_toemail=";
    url +=  scparam_toemail;

    url += "&scparam_logret=";
    url +=  scparam_logret;

    url += "&scparam_frost=";
    url +=  scparam_frost;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function daySelected(selText){

    var zoneid = document.getElementById("hdnzoneid").value;
    document.getElementById("schedulecontent").innerHTML = "";
    document.getElementById("mysysconfigdivschedule").innerHTML = "";
    
    if(selText.toString().trim() == 'Monday' || selText.toString().trim() == 'Tuesday' || selText.toString().trim() == 'Wednesday' || selText.toString().trim() == 'Thursday' || selText.toString().trim() == 'Friday' || selText.toString().trim() == 'Saturday' || selText.toString().trim() == 'Sunday')
    {
        $(".addnewpart").show();
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("schedulecontent").innerHTML = xmlhttp.responseText;
            }
        }
        xmlhttp.open("GET", "scheduleretrieve.php?zone=" + zoneid + "&selectedday=" + selText.toString().trim(), true);
        xmlhttp.send();
    }
    else
    {
        $(".addnewpart").hide();
    }

}

function GetZonesInformation(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById("placeholderzones").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "getzones.php", true);
    xmlhttp.send();
}


function copySchedule(){
    var zoneid = document.getElementById("hdnzoneid").value;
    var totalrows = document.getElementById("hdnCount").value;
    var selText = $('#lnkScheduleSelect').text();
    document.getElementById("mysysconfigdivschedule").innerHTML = "";
    
    var chkmonday = document.getElementById("chkmonday").checked;
    var chktuesday = document.getElementById("chktuesday").checked;
    var chkwednesday = document.getElementById("chkwednesday").checked;
    var chkthursday = document.getElementById("chkthursday").checked;
    var chkfriday = document.getElementById("chkfriday").checked;
    var chksaturday = document.getElementById("chksaturday").checked;
    var chksunday = document.getElementById("chksunday").checked;
    
    if (totalrows<=0)
    {
        document.getElementById("mysysconfigdivschedule").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>There must be atleast one entry for the selected weekday to copy.</div>";
        return false;
    }

    
    if(selText.toString().trim() == 'Monday' || selText.toString().trim() == 'Tuesday' || selText.toString().trim() == 'Wednesday' || selText.toString().trim() == 'Thursday' || selText.toString().trim() == 'Friday' || selText.toString().trim() == 'Saturday' || selText.toString().trim() == 'Sunday')
    {
        if (chkmonday == true || chktuesday == true || chkwednesday == true || chkthursday == true || chkfriday == true || chksaturday == true || chksunday == true){
            
            //Copy
            
            var daysToCopy = "";
            if (chkmonday)
                daysToCopy += "mon";
             
            if (chktuesday)
                daysToCopy += "tue";

            if (chkwednesday)
                daysToCopy += "wed";

            if (chkthursday)
                daysToCopy += "thu";

            if (chkfriday)
                daysToCopy += "fri";

            if (chksaturday)
                daysToCopy += "sat";

            if (chksunday)
                daysToCopy += "sun";
                
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    document.getElementById("mysysconfigdivschedule").innerHTML = xmlhttp.responseText;
                }
            }
            xmlhttp.open("GET", "copyscheduleacross.php?zone=" + zoneid + "&copydays=" + daysToCopy.toString().trim() + "&selectedday=" + selText.toString().trim(), true);
            xmlhttp.send();
        }
        else
        {
            document.getElementById("mysysconfigdivschedule").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>Please select atleast one weekday to copy.</div>";;
        }
    }    
}


function addNewSchedule(){
    var zoneid = document.getElementById("hdnzoneid").value;
    var selText = $('#lnkScheduleSelect').text();
    selText = selText.toString().trim();
    var fromtime = document.getElementById("timepicker1").value;
    var totime = document.getElementById("timepicker2").value;
    
    if (fromtime>=totime){
        document.getElementById("mysysconfigdivschedule").innerHTML = "<div class='alert alert-info alert-danger' role='alert'>From time should always be less than To time.</div>";;
        return false;
    }
    
    var temp = document.getElementById("scparam_temp").value;
    document.getElementById("mysysconfigdivschedule").innerHTML = "";
    
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            daySelected(selText);
            document.getElementById("mysysconfigdivschedule").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "addnewschedule.php?zone=" + zoneid + "&selectedday=" + selText.toString().trim() + "&fromtime=" + fromtime + "&totime=" + totime + "&temp=" + temp, true);
    xmlhttp.send();
}

function deleteSchedule(fromtime){
    var zoneid = document.getElementById("hdnzoneid").value;
    var selText = $('#lnkScheduleSelect').text();
    document.getElementById("mysysconfigdivschedule").innerHTML = "";
    selText = selText.toString().trim();
    
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            daySelected(selText);
        }
    }
    xmlhttp.open("GET", "deleteschedule.php?zone=" + zoneid + "&selectedday=" + selText.toString().trim() + "&fromtime=" + fromtime , true);
    xmlhttp.send();
}

function GetLogsInformation(period){
    document.getElementById("placeholderpregress").innerHTML = "In Progress...";
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById("placeholderlogs").innerHTML = xmlhttp.responseText;
            document.getElementById("placeholderpregress").innerHTML = "";
        }
    }
    xmlhttp.open("GET", "getlogs.php?period=" + period, true);
    xmlhttp.send();
}

function legend(parent, data) {
    parent.className = 'legend';
    var datas = data.hasOwnProperty('datasets') ? data.datasets : data;

    // remove possible children of the parent
    while(parent.hasChildNodes()) {
        parent.removeChild(parent.lastChild);
    }

    datas.forEach(function(d) {
        var title = document.createElement('span');
        title.className = 'title';
        parent.appendChild(title);

        var colorSample = document.createElement('div');
        colorSample.className = 'color-sample';
        colorSample.style.backgroundColor = d.hasOwnProperty('strokeColor') ? d.strokeColor : d.color;
        colorSample.style.borderColor = d.hasOwnProperty('fillColor') ? d.fillColor : d.color;
        title.appendChild(colorSample);

        var text = document.createTextNode(d.label);
        title.appendChild(text);
    });
}
