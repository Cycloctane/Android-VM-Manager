#! /system/bin/sh
# run on android guest vm when guest starts. should be added to /system/etc/init.sh
curl http://$controller_host/signin --data-urlencode "mac=`cat /sys/class/net/wlan0/address`" || true