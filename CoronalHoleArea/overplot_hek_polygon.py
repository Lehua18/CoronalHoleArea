"""
================================================
Overplotting HEK feature/event polygons on a map
================================================

How to overplot HEK outlines on a map.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Requires PyQt5 or PySide2 installed
import numpy as np
import astropy.units as u
from astropy.time import TimeDelta
import sunpy.data.sample
import sunpy.map
from sunpy.net import attrs as a
from sunpy.net import hek
from sunpy.physics.differential_rotation import solar_rotate_coordinate
from sunpy.net import Fido, attrs as a
from parfive import Downloader
from sunpy.map import Map
from astropy.time import Time
import csv


###############################################################################
#loop through day from 2010, export as csv, import to sunspot data grapher in java, ✨compare✨

downloader = Downloader(max_conn=1)  # Limit to 1 connection at a time

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

for year in range(2010,2011):
    for month in range(1,13):
        for day in range(1, numDays(month, year)+1):
            if month<10:
                monthStr = "0"+str(month)
            else:
                monthStr = str(month)

            if day < 10:
                dayStr = "0" + str(day)
            else:
                dayStr = str(day)


            # time = Time(input("Please enter a time in the form yyyy-MM-ddThh-mm: "))
            time = str(year)+"-"+monthStr+"-"+dayStr+"T00:00"
            time = Time(time)
            start = (time - 30 * u.s).iso
            end = (time + 30 * u.s).iso
            result = Fido.search(a.Time(start, end), a.Instrument.aia, a.Wavelength(193 * u.angstrom))

            #Failsafe
            if result:
                singleResult = result[0,0]
                files = Fido.fetch(singleResult, downloader=downloader)
                if not files or len(files) == 0:
                    print(f"Download failed for {time.iso}")
                    continue
                if files:
                    aia_map = Map(files)
                    client = hek.HEKClient()
                    results = client.search(a.Time(start, end), a.hek.EventType("CH"))
                    areaList = []
                    try:
                        for event in results:
                            areaList.append(float(str(event['area_atdiskcenter']).split(' ')[0]))

                        total = 0
                        for num in areaList:
                            total += num

                        percent = total / 6.09e12

                    # add total to array
                        data.append({'year': year, "month": month, "day": day, "percent":percent})
                    except:
                        continue
    print(str(month)+"/"+str(year))


# CSV STUFF (WORK HERE :))
fieldnames = ['year', 'month', 'day', 'percent']

with open('coronalhole.csv', 'w', newline='') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()  # Writes the header row
     writer.writerows(data)
##############################################################################
# Look for coronal holes detected using the SPoCA feature recognition method:
#
#     hek_client = hek.HEKClient()
#     start_time = aia_map.date - TimeDelta(2*u.hour)
#     end_time = aia_map.date + TimeDelta(2*u.hour)
#     responses = hek_client.search(a.Time(start_time, end_time), a.hek.CH, a.hek.FRM.Name == 'SPoCA')

##############################################################################
# Let's find the biggest coronal hole within 80 degrees north/south of the
# equator:

# area = 0.0
# for i, response in enumerate(responses):
#     if response['area_atdiskcenter'] > area and np.abs(response['hgc_y']) < 80.0:
#         area = response['area_atdiskcenter']
#         response_index = i
#
#
#
#
# print("CSV file 'example.csv' created successfully.")

#*PRETTY SURE THIS IS ALL JUST DISPLAY STUFF, DON'T NEED FOR AREA*
##############################################################################
# Next let's get the boundary of the coronal hole.

# ch = responses[response_index]
# ch_boundary = responses[response_index]["hpc_boundcc"]
#
# ##############################################################################
# # The coronal hole was detected at different time than the AIA image was
# # taken so we need to rotate it to the map observation time.
#
# rotated_ch_boundary = solar_rotate_coordinate(ch_boundary, time=aia_map.date)
#
# ##############################################################################
# # Now let's plot the rotated coronal hole boundary on the AIA map, and fill
# # it with hatching.
#
# fig = plt.figure()
# ax = fig.add_subplot(projection=aia_map)
# aia_map.plot(axes=ax, clip_interval=(1, 99.99)*u.percent)
# ax.plot_coord(rotated_ch_boundary, color='c')
# ax.set_title('{:s}\n{:s}'.format(aia_map.name, ch['frm_specificid']))
# plt.colorbar()
#
# plt.show()
