#!/bin/bash

#feh overlay

export http_proxy="http://proxy.mtechit.com:80"

echo "helllooo" > ~/script/weather/hiya

#get radar image for calgary area
RADAR="http://weather.gc.ca/data/radar/temp_image/XSM/XSM_PRECIP_RAIN_$(date +"%Y_%m_%d_")$(echo $(date +%H) +5|bc)_$(echo $(date +%M)/ 10 | bc)0.GIF"
echo $RADAR > ~/tmp.txt
#RADAR="http://weather.gc.ca/data/radar/temp_image/XSM/XSM_COMP_PRECIP_RAIN_2015_07_16_20_50.GIF"
TOWNS="http://weather.gc.ca/cacheable/images/radar/layers/default_cities/xsm_towns.gif"
ROADS="http://weather.gc.ca/cacheable/images/radar/layers/roads/XSM_roads.gif?ver=1410285168"

CIRCLES="http://weather.gc.ca/cacheable/images/radar/layers/radar_circle/radar_circle.gif"


rm img/*
curl -o ~/script/weather/img/radar.gif -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" $RADAR
curl -o ~/script/weather/img/towns.gif $TOWNS
curl -o ~/script/weather/img/roads.gif $ROADS
curl -o ~/script/weather/img/circles.gif $CIRCLES
convert ~/script/weather/img/*.gif -layers flatten ~/script/weather/img/output.gif

feh ~/script/weather/img/output.gif
