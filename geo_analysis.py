#!/usr/bin/python
__author__ = 'Gungor Ozer'

import numpy
import math
import csv
import sys

infile = 'input_data/yellow_tripdata_2015-01.csv'

# PROGRAM
# 
# INITIALIZATION
# Manhattan Max/Min Longitude & Latitude
max_LO = -73.9
min_LO = -74.05
max_LA = 40.88
min_LA = 40.68
# Determine PDF bins
bin_size = 0.010
size_LO = int(round((max_LO-min_LO)/bin_size))
size_LA = int(round((max_LA-min_LA)/bin_size))

# Declare PDF arrays --- [Longitude][Latitude][Hours]
pick_PDF = numpy.zeros((size_LO,size_LA,12))
pick_PDF_fare = numpy.zeros((size_LO,size_LA,12))
pick_PDF_tip = numpy.zeros((size_LO,size_LA,12))
pick_PDF_fare_per_distance = numpy.zeros((size_LO,size_LA,12))
pick_PDF_tip_per_distance = numpy.zeros((size_LO,size_LA,12))
drop_PDF = numpy.zeros((size_LO,size_LA,12))
drop_PDF_fare = numpy.zeros((size_LO,size_LA,12))
drop_PDF_tip = numpy.zeros((size_LO,size_LA,12))
drop_PDF_fare_per_distance = numpy.zeros((size_LO,size_LA,12))
drop_PDF_tip_per_distance = numpy.zeros((size_LO,size_LA,12))

with open(infile, 'r') as f:
     # Read line by line
     first_line = f.readline()
     for line in f:
         currentline = line.split(",")
         pick_TIME = str(currentline[1])
         drop_TIME = str(currentline[2])
         trip_DISTANCE = float(currentline[4])
         pick_LO = float(currentline[5])
         pick_LA = float(currentline[6])
         drop_LO = float(currentline[9])
         drop_LA = float(currentline[10])
         trip_FARE = float(currentline[12])
         trip_TIP = float(currentline[15])

         # Eliminate empty entries
         if trip_DISTANCE > 0:
            # Limit to rides that originate or end in Manhattan
            if pick_LO>min_LO and pick_LO<max_LO and pick_LA>min_LA and pick_LA<max_LA:
               if drop_LO>min_LO and drop_LO<max_LO and drop_LA>min_LA and drop_LA<max_LA:
                  trip_FARE_per_distance = trip_FARE/trip_DISTANCE
                  trip_TIP_per_distance = trip_TIP/trip_DISTANCE
                  # Calculate bins corresponding to pick-up/drop-off locations and times
                  pick_time_bin = pick_TIME.split(" ")[1].split(":")[0]
                  pick_time_bin = int(math.floor(float(pick_time_bin)/2.0))
                  drop_time_bin = drop_TIME.split(" ")[1].split(":")[0]
                  drop_time_bin = int(math.floor(float(drop_time_bin)/2.0))
                  pick_LO_bin = int(math.floor((pick_LO-min_LO)/bin_size))
                  pick_LA_bin = int(math.floor((pick_LA-min_LA)/bin_size))
                  drop_LO_bin = int(math.floor((drop_LO-min_LO)/bin_size))
                  drop_LA_bin = int(math.floor((drop_LA-min_LA)/bin_size))

                  # Calculate HOURLY $ (fare and/or tip) Spendings


                  # Calculate GEOGRAPHICAL $ (fare and/or tip) Spendings
                  pick_PDF[pick_LO_bin][pick_LA_bin][pick_time_bin] += 1
                  pick_PDF_fare[pick_LO_bin][pick_LA_bin][pick_time_bin] += trip_FARE
                  pick_PDF_tip[pick_LO_bin][pick_LA_bin][pick_time_bin] += trip_TIP
                  pick_PDF_fare_per_distance[pick_LO_bin][pick_LA_bin][pick_time_bin] += trip_FARE_per_distance
                  pick_PDF_tip_per_distance[pick_LO_bin][pick_LA_bin][pick_time_bin] += trip_TIP_per_distance
                  drop_PDF[drop_LO_bin][drop_LA_bin][drop_time_bin] += 1
                  drop_PDF_fare[drop_LO_bin][drop_LA_bin][drop_time_bin] += trip_FARE
                  drop_PDF_tip[drop_LO_bin][drop_LA_bin][drop_time_bin] += trip_TIP
                  drop_PDF_fare_per_distance[drop_LO_bin][drop_LA_bin][drop_time_bin] += trip_FARE_per_distance
                  drop_PDF_tip_per_distance[drop_LO_bin][drop_LA_bin][drop_time_bin] += trip_TIP_per_distance

h_file = 'output_data/hours_summary.txt'
h_print = open(h_file, 'w+')
for k in range(0,12):
    hour_PDF_pick = 0
    hour_PDF_pick_fare = 0.0
    hour_PDF_pick_tip = 0.0
    hour_PDF_drop = 0
    hour_PDF_drop_fare = 0.0
    hour_PDF_drop_tip = 0.0
        
    bin_k = str(2*k+1)
    o_file = 'output_data/geo_summary_'+bin_k+'.txt'
    g_print = open(o_file, 'w+')
    g_print.write("%8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %8s %8s\n" %  ('LONGITUD', 'LATITUDE', 'NUM_PICK', 'FARE_PIC', 'TIP_PICK', 'FPD_PICK', 'TPD_PICK', 'TPF_PICK', 'NUM_DROP', 'FARE_DRO', 'FARE_TIP', 'FPD_DROP', 'TPD_DROP', 'TPF_DROP'))
    for i in range(0,size_LO):
        print_LO = i*bin_size+min_LO
        for j in range(0,size_LA):
            print_LA = j*bin_size+min_LA
            if pick_PDF[i][j][k] > 0 and drop_PDF[i][j][k] > 0:
               # Calculate hourly $
               hour_PDF_pick += pick_PDF[i][j][k]
               hour_PDF_pick_fare += pick_PDF_fare[i][j][k]
               hour_PDF_pick_tip += pick_PDF_tip[i][j][k]
               hour_PDF_drop += drop_PDF[i][j][k]
               hour_PDF_drop_fare += drop_PDF_fare[i][j][k]
               hour_PDF_drop_tip += drop_PDF_tip[i][j][k]
       
               # Calculate geographical $
               pick_PDF_fare[i][j][k] /= pick_PDF[i][j][k]
               pick_PDF_tip[i][j][k] /= pick_PDF[i][j][k]
               pick_PDF_fare_per_distance[i][j][k] /= pick_PDF[i][j][k]
               pick_PDF_tip_per_distance[i][j][k] /= pick_PDF[i][j][k]
               drop_PDF_fare[i][j][k] /= drop_PDF[i][j][k]
               drop_PDF_tip[i][j][k] /= drop_PDF[i][j][k]
               drop_PDF_fare_per_distance[i][j][k] /= drop_PDF[i][j][k]
               drop_PDF_tip_per_distance[i][j][k] /= drop_PDF[i][j][k]
               if pick_PDF_fare[i][j][k] > 0:
                  pick_PDF_tip_per_fare = pick_PDF_tip[i][j][k]/pick_PDF_fare[i][j][k]
               else:
                  pick_PDF_tip_per_fare = 0.0
               if drop_PDF_fare[i][j][k] > 0:
                  drop_PDF_tip_per_fare = drop_PDF_tip[i][j][k]/drop_PDF_fare[i][j][k]
               else:
                  drop_PDF_tip_per_fare = 0.0
               g_print.write("%8.3f %8.3f %8d %8.3f %8.3f %8.3f %8.3f %8.3f %8d %8.3f %8.3f %8.3f %8.3f %8.3f\n" %  (print_LO, print_LA, pick_PDF[i][j][k], pick_PDF_fare[i][j][k], pick_PDF_tip[i][j][k], pick_PDF_fare_per_distance[i][j][k], pick_PDF_tip_per_distance[i][j][k], pick_PDF_tip_per_fare, drop_PDF[i][j][k], drop_PDF_fare[i][j][k], drop_PDF_tip[i][j][k], drop_PDF_fare_per_distance[i][j][k], drop_PDF_tip_per_distance[i][j][k], drop_PDF_tip_per_fare))
            else:
               g_print.write("%8.3f %8.3f %8d %8.3f %8.3f %8.3f %8.3f %8.3f %8d %8.3f %8.3f %8.3f %8.3f %8.3f\n" %  (print_LO, print_LA, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0))

    hour_PDF_pick_fare /= hour_PDF_pick
    hour_PDF_pick_tip /= hour_PDF_pick
    hour_PDF_pick_tpf = hour_PDF_pick_tip/hour_PDF_pick_fare
    hour_PDF_drop_fare /= hour_PDF_drop
    hour_PDF_drop_tip /= hour_PDF_drop
    hour_PDF_drop_tpf = hour_PDF_drop_tip/hour_PDF_drop_fare
     
    h_print.write("%3d %8d %8.3f %8.3f %8.3f %8d %8.3f %8.3f %8.3f\n" % (k+1, hour_PDF_pick/100000, hour_PDF_pick_fare, hour_PDF_pick_tip, hour_PDF_pick_tpf, hour_PDF_drop/100000, hour_PDF_drop_fare, hour_PDF_drop_tip, hour_PDF_drop_tpf)) 
