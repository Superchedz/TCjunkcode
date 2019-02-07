# shell script to auto run the ALEXA process at startup

cd /
cd home/pi/led
sleep 2
nohup sudo python TCAlexa.py &
nohup sudo python /home/pi/led/logger.py "Startup" "Alexa listener job started" &
cd /
