if pgrep -f "python bootloop.py" > /dev/null
then
    echo "bootloop.py process is running"
    exit
else
    echo "Bootloop.py process is not running - ohhh no"
    sudo python /home/pi/led/alerter.py "Alerter  - Bootloop Error" "Process bootloop.py was not found, check logs and restart"
fi
