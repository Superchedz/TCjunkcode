# starts the job that checks the ip addresses and emails if changed and ngrok to open the alexa https tunnel
cd /
cd home/pi/led
sudo ngrok http -config=/home/pi/.ngrok2/ngrok.yml 5000 &
sleep 2
nohup sudo python sendip.py &
cd /
