import matplotlib
matplotlib.use('Agg')
import astropy.units as u
from sunpy.net import hek
from sunpy.net import Fido, attrs as a
from parfive import Downloader
from sunpy.map import Map
from astropy.time import Time
import csv


#loop through day from 2010, export as csv, import to sunspot data grapher in java, ✨compare✨

downloader = Downloader(max_conn=1)  # Limit to 1 connection at a time

#gets number of days in a given month
def numDays(m, y):
    if m == 2 and y%4 !=  0:
        return 28
    elif m == 2:
        return 29
    elif  m == 9 or m == 4 or m == 6 or m == 11:
        return 30
    else:
        return 31


data = []

#edit range depending on which year is being pulled in form range(year, year+1)
for year in range(2014,2015):
    for month in range(1,13):
        for day in range(1, numDays(month, year)+1):

            #Adds '0' to the beginning of month or day if necessary
            if month<10:
                monthStr = "0"+str(month)
            else:
                monthStr = str(month)

            if day < 10:
                dayStr = "0" + str(day)
            else:
                dayStr = str(day)

            #Finds all images within thirty seconds of midnight of selected day
            time = str(year)+"-"+monthStr+"-"+dayStr+"T00:00"
            time = Time(time)
            start = (time - 30 * u.s).iso
            end = (time + 30 * u.s).iso
            result = Fido.search(a.Time(start, end), a.Instrument.aia, a.Wavelength(193 * u.angstrom))

            if result:
                #Gets first file found
                singleResult = result[0,0]
                files = Fido.fetch(singleResult, downloader=downloader)

                #Failsafe
                if not files or len(files) == 0:
                    print(f"Download failed for {time.iso}")
                    continue

                #Get area
                if files:
                    aia_map = Map(files)
                    client = hek.HEKClient()
                    results = client.search(a.Time(start, end), a.hek.EventType("CH"))


                    areaList = []
                    try:
                        #Get area of all coronal holes
                        for event in results:
                            areaList.append(float(str(event['area_atdiskcenter']).split(' ')[0]))

                        #Add area of all coronal holes
                        total = 0
                        for num in areaList:
                            total += num

                        #Converts to thousands of the solar disk
                        percent = total / 3.045e9

                    # add total to array
                        data.append({'year': year, "month": month, "day": day, "percent":percent})
                    except:
                        continue
    print(str(month)+"/"+str(year))

#converts to csv file
fieldnames = ['year', 'month', 'day', 'percent']
with open('coronalhole.csv', 'w', newline='') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()  # Writes the header row
     writer.writerows(data)