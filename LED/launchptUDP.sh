# shell script to auto run the protosen scanner process at startup

cd /
sleep 30
cd home/pi/led
nohup sudo python protosenUDP.py &

cd /
