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
nohup sudo python control1.py > /home/pi/logs/control1.log 2>&1 &
cd /

echo
echo "##########################################################################"
echo "################## Start the Alexa Management service  ###################"
echo "##########################################################################"
cd /
cd home/pi/led
echo end of snooze
nohup sudo python TCAlexa.py /home/pi/logs/TCAlexa.log 2>&1 &
cd /
echo
echo "##########################################################################"
echo "############  Start the ProtoSen scanner job - Serial version ############"
echo "##########################################################################"
cd /
cd home/pi/led
nohup sudo python protosen.py /home/pi/logs/protosen.log 2>&1 &
cd /

echo
echo "##########################################################################"
echo "###################### Start the Bootloop program ########################"
echo "##########################################################################"
cd /
cd home/pi/led
nohup sudo python bootloop.py /home/pi/logs/bootloop.log 2>&1 &
cd /

echo
echo "##########################################################################"
echo "#########  Start the IP scanner job (one off run)- Serial version ########"
echo "##########################################################################"

cd /
cd home/pi/led
nohup sudo python sendip.py /home/pi/logs/sendip.log 2>&1 &



echo
echo "##########################################################################"
echo "################################# The end... #############################"
echo "##########################################################################"
echo "End of kicker"
cd /
