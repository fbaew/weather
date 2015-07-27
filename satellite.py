#!/usr/bin/python

import datetime
import requests
import urllib3
from os import listdir
from os.path import isfile,join

#export http_proxy="http://proxy.mtechit.com:80"


#get the radar image from
url = "http://weather.gc.ca/data/satellite/goes_wcan_1070_m_"
datestring = "2015@07@16_21h00m.jpg"

now = datetime.datetime.now()
today = str(now.year) + "@" + str(now.month).zfill(2) + "@" + str(now.day).zfill(2) + "_"
images = []


#Get images since the given hour


def pull_images(latest):
	startHour = latest[0]
	startMinute = latest[1]
	print "Getting images from: ", str(startHour), str(startMinute)

	n = 0
	for i in range(startHour,now.hour+1):
            print("startHour: " + str(startHour))
            n += 1
            if n > 1:
                startMinute = 0;
            for j in range(startMinute,6):
               print("adding image for minute {}".format(j))
               images.append(today + (str(i).zfill(2) + "h" + str(j*10).zfill(2) + "m.jpg"))

	
	

	for image in images:
	    r = requests.get(url+image)
	    imagefile = open(join("sat_img/", image),"w");
	    imagefile.write(r.content)
	    imagefile.close()
	    print ("getting image at " + url + image);


def latest_image():
    files = [ f for f in listdir("sat_img") if isfile(join("sat_img",f)) ]
    if files == []:
	return (0,0)
    files.sort()
    print files
    latest = files[-1].split("_")[1].split(".")[0]
    hour = latest.split("h")[0]
    minute = latest.split("h")[1].split("m")[0]
    return (int(hour),int(minute))

#pull_images( latest_image() )
#pull_images(0,0)


if __name__ == "__main__":
	pull_images(latest_image())
	print("Done retrieving images")
