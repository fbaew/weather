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

        Two methods:
        timeToUrl(datetime) -- takes a datetime object, returns string of url format. Must be implemented by subclass
        timeToString(datetime) - takes a datetime object and returns "YYYY_MM_DD_HH_MM" format

    """
    def __init__(self, directoryPath, url, fileExtension, timeToUrl):
        #Strings
        self.directoryPath = directoryPath
        self.url = url
        self.fileExtension = fileExtension

        self.timeToUrl = timeToUrl #implemented by subclass

        self.timeToString = lambda dt: "{0:0>4}_{1:0>2}_{2:0>2}_{3:0>2}_{4:0>2}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute)
        """ Takes datetime object, Outputs string of format  "2015_07_29_17_40"

            Output is the format of the radar url filenames and is being used as the local
            storage naming scheme.
        """

    def downloadImages(self, datetimeList):
        """Takes list of datetime objects to download, downloads those times from self.url.
        """

        urlList=[]
        nameList=[]

        for time in datetimeList:
            urlList.append(self.url + self.timeToUrl(time) + self.fileExtension)
            nameList.append(self.directoryPath + self.timeToString(time) + self.fileExtension)

        for fileName,url in zip(nameList,urlList):
            if isfile(fileName):
                print("File already exists, skipping: " + fileName)
                continue

            try:
                r = requests.get(url)
                r.raise_for_status()
            except (requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError) as e:
                print(e)
                continue
            except requests.exceptions.RequestException as e:
                print("Now would be a good time to handle a new exception.")
                print(e)
                sys.exit(1)

            try:
                imageFile = open(fileName,"wb")
                print("Trying: " + url)
                imageFile.write(r.content)
                imageFile.close()
                print("File written to: " + fileName + "\n")
            except IOError:
                #make this better eventually
                print("Error opening/writing  " + fileName + ". Abort! Abort! Abandon program!")
                raise


    def dateRange(self, fromTime, toTime=datetime.datetime.utcnow(), minuteInterval=10):
        """ Generator function for datetime objects fromTime toTime at given minuteInterval.
        """
        #Floors times to 10 minutes, wiping seconds, microseconds
        fromTime -= datetime.timedelta(minutes=fromTime.minute % 10,
                                        seconds=fromTime.second, microseconds=fromTime.microsecond)
        toTime -= datetime.timedelta(minutes=toTime.minute % 10,
                                        seconds=toTime.second, microseconds=toTime.microsecond)

        if (fromTime <= toTime):
            while (fromTime <= toTime):
                yield fromTime
                fromTime += datetime.timedelta(minutes=minuteInterval)
        elif (fromTime > toTime):
            while (fromTime >= toTime):
                yield fromTime
                fromTime -= datetime.timedelta(minutes=minuteInterval)
        else:
            print("AAAAAAHHHHHHH!")
            raise StopIteration

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

    def stringToTime(self, dateString):
        """Parses a date/time of format 2015_07_29_17_40 and returns a datetime object

            To add: error checking. Assumes proper format.
        """
        split = list(map(int,dateString.split("_")))
        obj = datetime.datetime(split[0],split[1],split[2],split[3],split[4])
        return obj

class Radar(ImageAggregator):
    """ Implementation for Alberta radar imagery. Extends ImageAggregator.

        https://weather.gc.ca/data/radar/temp_image/XSM/XSM_PRECIP_RAIN_2015_07_29_17_40.GIF
        XSM_PRECIP_RAIN_2015_07_29_17_40
                        YYYY_MO_DD_HH_MI
        https://weather.gc.ca/cacheable/images/radar/layers/rivers/xsm_rivers.gif
        https://weather.gc.ca/cacheable/images/radar/layers/roads/XSM_roads.gif?ver=1410285168
        https://weather.gc.ca/cacheable/images/radar/layers/additional_cities/xsm_towns.gif

        RADAR:
        http://dd.weather.gc.ca/radar/doc/README_radar.txt
        #3 letter radar station name list
        http://www.msc-smc.ec.gc.ca/projects/nrp/Montreal_e.cfm

        Time in UTC
    """

    def __init__(self):
        self.directoryPath = "radar_img/"
        self.url = "http://weather.gc.ca/data/radar/temp_image/XBE/XBE_PRECIP_RAIN_"
        self.fileExtension = ".GIF"
        #This service operates on the same naming scheme as the remote URLs,
        #no need to convert date string format. Passes string it receives.
        self.timeToUrl = lambda x: self.timeToString(x)
        super().__init__(self.directoryPath,self.url,self.fileExtension,self.timeToUrl)


class Satellite(ImageAggregator):
    """ Implentation for Alberta Satellite imagery. Extends ImageAggregator.

        self.datestring = "2015@07@16_21h00m.jpg"
        Example URL: https://weather.gc.ca/data/satellite/goes_wcan_1070_m_2015@08@01_21h00m.jpg
        Only goes back 48 hours. Time in UTC.
    """

    def __init__(self):
        self.directoryPath = "sat_img/"
        self.url = "http://weather.gc.ca/data/satellite/goes_wcan_1070_m_"
        self.fileExtension = ".jpg"
        #This should not be a oneliner, but, for now... this turns '2015_07_29_17_40' into '2015@07@29_17h40m'
        self.timeToUrl = lambda time: "".join(map(lambda x,y: x + y, self.timeToString(time).split('_'), ['@','@','_','h','m']))

        super().__init__(self.directoryPath,self.url,self.fileExtension,self.timeToUrl)


if __name__ == "__main__":
    now = datetime.datetime.utcnow()

    fortyMinutesAgo = now - datetime.timedelta(minutes=40)

    sat = Satellite()
    sat.downloadImages(sat.dateRange(fortyMinutesAgo))
    sat.printImageList()

    for date in sat.dateRange(now,fortyMinutesAgo):
        print(date)
    for date in sat.dateRange(fortyMinutesAgo,now):
        print(date)

    rad = Radar()
    rad.downloadImages(rad.dateRange(fortyMinutesAgo))
    rad.printImageList()
