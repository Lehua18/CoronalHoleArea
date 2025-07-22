"""
================================================
Overplotting HEK feature/event polygons on a map
================================================

How to overplot HEK outlines on a map.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')  # Requires PyQt5 or PySide2 installed

import numpy as np

import astropy.units as u
from astropy.time import TimeDelta

import sunpy.data.sample
import sunpy.map
from sunpy.net import attrs as a
from sunpy.net import hek
from sunpy.physics.differential_rotation import solar_rotate_coordinate
from sunpy.net import Fido, attrs as a
from sunpy.map import Map
from astropy.time import Time
import csv


###############################################################################
#loop through day from 2010, export as csv, import to sunspot data grapher in java, ✨compare✨
for day in day:
    time = Time(input("Please enter a time in the form yyyy-MM-ddThh-mm: "))
    start = (time - 30 * u.s).iso
    end = (time + 30 * u.s).iso
    result = Fido.search(
        a.Time(start, end),
        a.Instrument.aia,
        a.Wavelength(193 * u.angstrom)
    )

    #Failsafe
    if not result:
        print("No matching images found.")
        exit()

    files = Fido.fetch(result)
    closest_file = min(files, key=lambda f: abs(Map(f).date - time))
    aia_map = Map(closest_file)
    client = hek.HEKClient()
    results = client.search(a.Time(start, end), a.hek.EventType("CH"))
    areaList = []
    for event in results:
        areaList.append(float(event['area_atdiskcenter'].split(' ')[0]))

    total = 0
    for num in areaList:
        total += num
##############################################################################
# Look for coronal holes detected using the SPoCA feature recognition method:

    hek_client = hek.HEKClient()
    start_time = aia_map.date - TimeDelta(2*u.hour)
    end_time = aia_map.date + TimeDelta(2*u.hour)
    responses = hek_client.search(a.Time(start_time, end_time), a.hek.CH, a.hek.FRM.Name == 'SPoCA')

##############################################################################
# Let's find the biggest coronal hole within 80 degrees north/south of the
# equator:

area = 0.0
for i, response in enumerate(responses):
    if response['area_atdiskcenter'] > area and np.abs(response['hgc_y']) < 80.0:
        area = response['area_atdiskcenter']
        response_index = i

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
