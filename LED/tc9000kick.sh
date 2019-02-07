echo "##########################################################################"
echo "################## Starting TC9000 system jobs ###########################"
echo "##########################################################################"
echo "This job now just does the GIT pull, to allow the install to run in one go"
echo "After this, kicker.sh runs to do any install work"
#!/bin/bash

sleep 30
echo
echo "##########################################################################"
echo "############  Do a GIT repository PULL to check for updates ##############"
echo "##########################################################################"
cd /
cd home/pi/git
sudo git pull https://github.com/Superchedz/TCjunkcode.git 
sudo rsync -a web/ /var/www/boiler/

sudo mv crons/* /etc/cron.d
sudo mv LED/* /home/pi/led
cd /

echo "##########################################################################"
echo "############## Backing up previous log files to aid support ##############"
echo "##########################################################################"

cd /home/pi/logs
sudo mkdir -p /home/pi/logs/previous
sudo rm -f /home/pi/logs/previous/*
sudo find . -maxdepth 1 -type f -exec mv {} /home/pi/logs/previous \;
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

echo "Kicking kicker.sh"
cd /
sh ./home/pi/led/kicker.sh > /home/pi/logs/kickero.log

echo '######################################################'
echo "Tidying up MessageBridge logs to avoid getting too big"

sudo rm  /home/pi/WirelessThings-LaunchPad/MessageBridge/MessageBridge.log
sudo rm  /home/pi/Launchpad/MessageBridge/MessageBridge.log

 