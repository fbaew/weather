import ImageAggregator as IA
import datetime

now = datetime.datetime.utcnow()

From = now - datetime.timedelta(minutes=0, hours=1)

sat = IA.Satellite()
for date in sat.dateRange(now,From):
    print(date)
for date in sat.dateRange(From,now):
    print(date)


# sat.downloadImages(sat.dateRange(fortyMinutesAgo))
# sat.printImageList()

# rad = Radar()
# rad.downloadImages(rad.dateRange(fortyMinutesAgo))
# print(rad.dateConverter("2015_07_29_17_40"))
# rad.printImageList()
