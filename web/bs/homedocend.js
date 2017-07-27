$('#myModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var recipient = button.data('whatever'); // Extract info from data-* attributes
   var modal = $(this);
         document.getElementById("mysysconfigdiv").innerHTML = "";
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("sysconfigcontent").innerHTML = xmlhttp.responseText;
            }
        }
        xmlhttp.open("GET", "sysconfig.php", true);
        xmlhttp.send();
  //modal.find('.sysconfigcontent').text(recipient);
  //modal.find('.modal-body input').val(recipient)
});

$('#myModalSchedule').on('hidden.bs.modal', function () {
    //window.location = "home.php";
    GetZonesInformation();
})


$('#myModalLogs').on('show.bs.modal', function (event) {
     //var selText = $('#lnkPeriod').text();
     //alert(selText);
    //GetLogsInformation(2);
});

$('#myModalSchedule').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var selText = $('#lnkScheduleSelect').text();

  var zoneid = button.data('zoneid'); // Extract info from data-* attributes
  var zonename = button.data('zonename'); // Extract info from data-* attributes
  document.getElementById("myForgotPwd1Label").innerHTML = zoneid + " - " + zonename + " Schedule";
  document.getElementById("hdnzoneid").value = zoneid;
   var modal = $(this);
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
});

$('#myModalBoost').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

  var zoneid = button.data('zoneid'); // Extract info from data-* attributes
  var zonename = button.data('zonename'); // Extract info from data-* attributes
  var zonetype = button.data('zonetype');
  
  document.getElementById("myForgotPwd2Label").innerHTML = "Boost: " + zonename;
  document.getElementById("hdnzoneid1").value = zoneid;
  document.getElementById("timepickerboost").value = "01:00";
//  document.getElementById("ezonetype").value = zonetype;
  document.getElementById("mysysconfigdiv123").innerHTML = "";
    
});



$('#myModalChangePassword').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

  document.getElementById("scparam_oldpassword").value = "";
  document.getElementById("scparam_Newpassword").value = "";
  document.getElementById("scparam_Newpassword1").value = "";

    document.getElementById("mysysconfigdiv123456").innerHTML = "";
    
});



$('#myModalZoneConfig').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

  var zoneid = button.data('zoneid'); // Extract info from data-* attributes
  var zonename = button.data('zonename'); // Extract info from data-* attributes
  var zonesensor = button.data('zonesensor'); // Extract info from data-* attributes
  var zoneoffset = button.data('zoneoffset'); // Extract info from data-* attributes
  var zonezonetype = button.data('zonezonetype'); // Extract info from data-* attributes  
  var pinnum = button.data('pinnum'); // Extract info from data-* attributes
    
  document.getElementById("myForgotPwd3Label").innerHTML = zoneid + " - " + zonename + " Settings";
  document.getElementById("hdnzoneid2").value = zoneid;
  document.getElementById("scparam_zonename").value = zonename;
  document.getElementById("scparam_zonesensor").value = zonesensor;
  document.getElementById("scparam_offset").value = zoneoffset;  
  document.getElementById("scparam_zonetype").value = zonezonetype;  
  document.getElementById("scparam_pinnum").value = pinnum;  
  
  

    document.getElementById("mysysconfigdiv1234").innerHTML = "";
    
});

$('#myModalExtend').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

  var zoneid = button.data('zoneid'); // Extract info from data-* attributes
  var zonename = button.data('zonename'); // Extract info from data-* attributes
  document.getElementById("mysysconfigdiv12345").innerHTML = "";
    
  document.getElementById("myForgotPwd4Label").innerHTML = zoneid + " - " + zonename + " Extend";
  document.getElementById("hdnzoneid3").value = zoneid;
    
});


$('#myModalDelete').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

  var zoneid = button.data('zoneid'); // Extract info from data-* attributes
  var zonename = button.data('zonename'); // Extract info from data-* attributes
  document.getElementById("mysysconfigdiv12345Delete").innerHTML = "";
    
  document.getElementById("myForgotPwd14Label").innerHTML = zoneid + " - " + zonename + " Delete?";
  document.getElementById("hdnzoneid3del").value = zoneid;
    
});

$('#myModalDelete').on('hidden.bs.modal', function () {
    //window.location = "home.php";
    GetZonesInformation();
})

$('#myModalAddZone').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal

    document.getElementById("mysysconfigdiv1234Add").innerHTML = "";
    document.getElementById("scparam_addzonename").value = "";
    document.getElementById("scparam_addzonesensor").value = "";
    document.getElementById("scparam_addoffset").value = "0";
    document.getElementById("scparam_addzonetype").value = "0";	
    document.getElementById("scparam_addpinnum").value = "0";
    
});


$('#myModalAddZone').on('hidden.bs.modal', function () {
    //window.location = "home.php";
    GetZonesInformation();
})

$(".dropdown-menu li a").click(function(){
  var selText = $(this).text();
  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});

GetZonesInformation();