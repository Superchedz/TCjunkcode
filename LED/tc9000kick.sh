echo "##########################################################################"
echo "################## Starting TC9000 system jobs ###########################"
echo "##########################################################################"

sleep 30
echo
echo "##########################################################################"
echo "############  Do a GIT repository PULL to check for updates ##############"
echo "##########################################################################"
cd /
cd home/pi/git
sudo git pull https://github.com/Superchedz/TCjunkcode.git 
sudo mv web/* /var/www/boiler
sudo mv crons/* /etc/cron.d
sudo mv LED/* /home/pi/led
cd /

echo
echo "##########################################################################"
echo "##########  Modify any delivered shell scripts to executables ############"
echo "##########################################################################"
cd home/pi/led
echo
ls *.sh
echo 
sudo chmod +x *.sh
sudo chown pi:root *.sh



echo ############### Shutdown installer #####################
echo ## we can always do this as if the row exists it will just give an error.
echo created 16/7/2017
echo
mysql --batch -h localhost -u root --password=pass123 -D  BoilerControl  < insshut.txt > ssqlout.txt    
mysql --batch -h localhost -u root --password=pass123 -D  BoilerControl  < upshut.txt > supout.txt    


echo ################## Sleep installer #####################
echo ##### We test for the existence of sleepdone file ######
echo ############ if not there run scripts ################
echo created 6/5/2016
echo
if ! [ -f sleepdone ]; then
  echo 
  echo The sleepdone file wasnt found, so run sql script to add tables and set new columns to zone
  touch sleepdone
  mysql --batch -h localhost -u root --password=pass123 -D  BoilerControl  < sqlsleep1.txt > sqlout.txt    
else
  echo The sleepdone file was found so its assumed sleep tables are installed already - skipping
fi

echo "##########################################################################"
echo "########## Start the NOIP service to update fowarding service ############"
echo "##########################################################################"
echo starting noip
cd /
nohup sudo usr/local/bin/noip2 &
cd /

echo
echo "##########################################################################"
echo "################# Start the Control1 switching program ###################"
echo "##########################################################################"
cd /
cd home/pi/led
echo end of snooze
nohup sudo python control1.py &
cd /


echo
echo "##########################################################################"
echo "############  Start the ProtoSen scanner job - Serial version ############"
echo "##########################################################################"
cd /
cd home/pi/led
nohup sudo python protosen.py &
cd /



echo
echo "##########################################################################"
echo "#########  Start the IP scanner job (one off run)- Serial version ########"
echo "##########################################################################"

cd /
cd home/pi/led
sudo python sendip.py 



echo
echo "##########################################################################"
echo "################################# The end... #############################"
echo "##########################################################################"
cd /
