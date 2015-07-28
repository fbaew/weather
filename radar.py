#!/usr/bin/python

import datetime
import requests
import urllib3
from os import listdir
from os.path import isfile,join

#export http_proxy="http://proxy.mtechit.com:80"

radarURL = "http://weather.gc.ca/data/radar/temp_image/XSM/XSM_PRECIP_RAIN_"
townsURL = "http://weather.gc.ca/cacheable/images/radar/layers/default_cities/xsm_towns.gif"
roadsURL = "http://weather.gc.ca/cacheable/images/radar/layers/roads/XSM_roads.gif?ver=1410285168"
circlesURL = "http://weather.gc.ca/cacheable/images/radar/layers/radar_circle/radar_circle.gif"

#get the radar image from
#url = "http://weather.gc.ca/data/satellite/goes_wcan_1070_m_"
url = radarURL

now = datetime.datetime.utcnow()
today = str(now.year) + "_" + str(now.month).zfill(2) + "_" + str(now.day).zfill(2) + "_"
images = []


#Get images since the given hour


def pull_images(latest):
	startHour = latest[0]
	startMinute = latest[1]/10
	endMinute=6
	print "Getting images from: ", str(startHour), str(startMinute)

	n = 0
	for i in range(startHour,now.hour+1):
            n += 1
            if n > 1:
                startMinute = 0;
	    if i == now.hour:
		endMinute = now.minute/10;
            print("{} is the start {} is the end".format(startMinute,endMinute));
            for j in range(startMinute,endMinute):
               print("adding image for minute {}".format(j))
               images.append(today + (str(i).zfill(2) + "_" + str(j*10).zfill(2) + ".GIF"))

	
	

	for image in images:
	    r = requests.get(url+image)
	    imagefile = open(join("radar_img/", image),"w");
	    imagefile.write(r.content)
	    imagefile.close()
	    print ("getting image at " + url + image);


def latest_image():
    files = [ f for f in listdir("radar_img") if isfile(join("radar_img",f)) ]
    if files == []:
	return (0,0)
    files.sort()
    print files
    latest = files[-1].split("_")
    hour = latest[3]
    minute = latest[4].split(".")[0]
    return (int(hour),int(minute))

#pull_images( latest_image() )
#pull_images(0,0)


if __name__ == "__main__":
	pull_images(latest_image())
	print("Done retrieving images")
