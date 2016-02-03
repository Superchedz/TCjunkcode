# shell script to auto run the protosen scanner process at startup

cd /
cd home/pi/led
sleep 10
#nohup sudo python protosen.py &
nohup sudo python control1.py &
cd /
