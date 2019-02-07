cd /
sleep 3
nohup sudo ngrok http 5000 &
nohup sudo python /home/pi/led/logger.py "Startup" "NGROK Secure Tunnel opened" &
cd /
