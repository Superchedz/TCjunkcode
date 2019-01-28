echo "##########################################################################"
echo "################## Starting TC9000 system jobs ###########################"
echo "##########################################################################"

echo "This is stage 2 of installing patches.  This does the actual installs"
echo "Stage 1 was the TC9000kick.sh which pulled any new code down from GIT"

cd /home/pi/led

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
echo "################## Start the Alexa Management service  ###################"
echo "##########################################################################"
cd /
cd home/pi/led
echo end of snooze
nohup sudo python TCAlexa.py &
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
echo "###################### Start the Bootloop program ########################"
echo "##########################################################################"
cd /
cd home/pi/led
nohup sudo python bootloop.py &
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
echo "End of kicker"
cd /
