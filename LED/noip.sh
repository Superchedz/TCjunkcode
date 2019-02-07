cd /
cd home/pi/led
nohup sudo usr/local/bin/noip2 &
nohup sudo python /home/pi/led/logger.py "Startup" "NOIP URL redirection service started" &
cd /

