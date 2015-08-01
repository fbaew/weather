#!/usr/bin/env python
import datetime
import requests
#import urllib3
from os import listdir
from os.path import isfile,join

#export http_proxy="http://proxy.mtechit.com:80"
# townsURL = "http://weather.gc.ca/cacheable/images/radar/layers/default_cities/xsm_towns.gif"
# roadsURL = "http://weather.gc.ca/cacheable/images/radar/layers/roads/XSM_roads.gif?ver=1410285168"
# circlesURL = "http://weather.gc.ca/cacheable/images/radar/layers/radar_circle/radar_circle.gif"
#Takes a datetime.utcnow()

class ImageAggregator(object):
    """Not instantiated directly. Contains logic that children will use/extend. 

        Attributes to be set by children:
        directoryPath -- string, local subfolder, for image storage
        url -- file root url for scraping, e.g 'https://weather.gc.ca/data/radar/temp_image/XSM/XSM_PRECIP_RAIN_'
        fileExtension -- short string. e.g. ".jpg" or ".GIF"
        dateConverter -- Lambda function that takes "YYYY_MM_DD_HH_MM" and converts to string of url format.
    """
    def __init__(self, directoryPath, url, fileExtension, dateConverter):
        #datetime object
        self.created = datetime.datetime.utcnow()
        #Strings
        self.directoryPath = directoryPath
        self.url = url
        self.fileExtension = fileExtension
        #A function to turn local naming scheme string into child's URL one
        self.dateConverter = dateConverter

    def downloadImages(self, nameList):
        """Takes list of filenames in format YYYY_MM_DD_HH_MM, downloads those images from self.url. 

              Can be overridden by children for differing filename conventions. Checks if  file
              exists locally, appends appropriate file extension. 

              Todo: This function can and should be split up for more general usage. Should accept single arg"""

        urlList=[]
        for dateString in nameList:
            urlList.append(self.url + self.dateConverter(dateString) + self.fileExtension)
        #for item,url in zip(urlList,nameList): print(item,url)
        for fileName,url in zip(nameList,urlList):
            fileName += self.fileExtension
            if isfile(self.directoryPath + fileName):
                print("File already exists, skipping: " + fileName)
                continue #skips this file
            #Needs to catch requests exceptions, io exceptions. Rough catch-all that will
            #terminate program in place. remove the 'raise' in the exception to have it continue
            #running despite errors.
            try:
                r = requests.get(url)
                imageFile = open(join(self.directoryPath, fileName),"wb")
                print("\nAttempting to get image at: " + url)
                imageFile.write(r.content)
                imageFile.close()
                #print(hello)
                print("File written to: " + join(self.directoryPath + fileName) + "\n")
            except:
                #make this better eventually
                print("Error opening/writing  " + join(self.directoryPath, fileName) + ". Abort! Abort! Abandon program!")
                raise

    def dateRange(self, fromTime,toTime=datetime.datetime.utcnow(),minuteInterval=10):
        """ Takes two datetime objects, returns sequential list of date strings in given minute increments 

            Outputs list of format  "2015_07_29_17_40" 
                                    (YYYY_MM_DD_HH_MM)
            Output is the format of the radar url filenames and has been used as
            the standard for internal representation. Children should provide a
            dateConverter function that translates a string of this format to their URL format.

            Needs to be tested with lists/corner cases, should implement case/handling 
            for toTime < fromTime which gives a chronologically descending list.
            Should make it iterable. 
        """

        #Floors times to 10 minutes, wiping seconds, microseconds
        fromTime -= datetime.timedelta(minutes=fromTime.minute % 10, 
                                        seconds=fromTime.second, microseconds=fromTime.microsecond)
        toTime -= datetime.timedelta(minutes=toTime.minute % 10, 
                                        seconds=toTime.second, microseconds=toTime.microsecond)

        #Generate list of "2015_07_29_17_40" format strings

        dateList = []
        c = fromTime
        while (c <= toTime):
            dateList.append("{0:0>4}_{1:0>2}_{2:0>2}_{3:0>2}_{4:0>2}".format(c.year,c.month,c.day,c.hour,c.minute))
            c += datetime.timedelta(minutes=minuteInterval)

        print(dateList)
        return dateList

    def makeLatestImage(self, fromTime):
        """ Needs implementation.
            Takes a datetime object 'from', generates a gif fromTime til present. use os calls to imagemagik? Put it in self.directoryPath"""
        pass

    def printImageList(self): 
        """Prints a list of files in the child's subdirectory"""
        files = [ f for f in listdir(self.directoryPath) if isfile(join(self.directoryPath,f)) ]
        if files == []:
            print("[]")
            return 0
        files.sort()
        print("\nAll files in " + self.directoryPath)
        print(files)
        print("\n")
        
    def nameToTime(self, dateString):
        """Parses a date/time of format 2015_07_29_17_40 and returns a datetime object of that time

            To add: error checking. Assumes proper format."""
        obj = datetime.datetime(dateString.split("_"))
        return obj

class Radar(ImageAggregator):
    """Implementation for weather.gc.ca radar images. Single hardcoded example at the moment.
    Example URL: 
    https://weather.gc.ca/data/radar/temp_image/XSM/XSM_PRECIP_RAIN_2015_07_29_17_40.GIF
    XSM_PRECIP_RAIN_2015_07_29_17_40
                    YYYY_MO_DD_HH_MI
    https://weather.gc.ca/cacheable/images/radar/layers/rivers/xsm_rivers.gif
    https://weather.gc.ca/cacheable/images/radar/layers/roads/XSM_roads.gif?ver=1410285168
    https://weather.gc.ca/cacheable/images/radar/layers/additional_cities/xsm_towns.gif
    """

    def __init__(self):
        self.directoryPath = "radar_img/"
        self.url = "http://weather.gc.ca/data/radar/temp_image/XBE/XBE_PRECIP_RAIN_"
        self.fileExtension = ".GIF"
        #This service operates on the same naming scheme as the remote URLs,
        #no need to convert date string format. Passes string it receives.
        self.dateConverter = lambda x: x
        super().__init__(self.directoryPath,self.url,self.fileExtension,self.dateConverter)


class Satellite(ImageAggregator):
    """ Implentation for Alberta Satellite imagery. Single imagetype at the moment.
        Currently only one map type, need to create list of all available.
        URL sample:                                          YYYY@MO@DD_HHhMIm.jpg

        self.datestring = "2015@07@16_21h00m.jpg"
    """

    def __init__(self):
        self.directoryPath = "sat_img/"
        self.url = "http://weather.gc.ca/data/satellite/goes_wcan_1070_m_"
        self.fileExtension = ".jpg"
        #Maybe shouldn't be a oneliner, but, for now... this turns '2015_07_29_17_40' into '2015@07@29_17h40m'
        self.dateConverter = lambda string: "".join(map(lambda x,y: x + y, string.split('_'), ['@','@','_','h','m']))
        
        super().__init__(self.directoryPath,self.url,self.fileExtension,self.dateConverter)


if __name__ == "__main__":
    now = datetime.datetime.utcnow()
    
    fortyMinutesAgo = now - datetime.timedelta(minutes=40)
    
    sat = Satellite()
    sat.downloadImages(sat.dateRange(fortyMinutesAgo))
    print(sat.dateConverter("2015_07_29_17_40"))
    sat.printImageList()

    rad = Radar()
    rad.downloadImages(rad.dateRange(fortyMinutesAgo))
    print(rad.dateConverter("2015_07_29_17_40"))
    rad.printImageList()
