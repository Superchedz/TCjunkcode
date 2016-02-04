echo "##########################################################################"
echo "################## Starting TC9000 system jobs ###########################"
echo "##########################################################################"

echo
echo "##########################################################################"
echo "############  Do a GIT repository PULL to check for updates ##############"
echo "##########################################################################"
cd /
cd home/pi/git
sudo git pull https://github.com/Superchedz/TCjunkcode.git 
sudo mv web/* /var/www/boiler
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
echo sleep for 30 secs to allow git pulls to work
sleep 30
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
