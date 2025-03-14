#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Jan 20 20:22:02 2024

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Generates a country-wide plot of Re-Climate® temperature variable from an ASCII input.

"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
import cartopy.crs as ccrs
import calendar

country = 'UK' # Analysis data is currently available for the UK only
start_years = ['2023','2023','2023','2024','2024','2024','2024'] # ['2023','2023','2023','2024','2024','2024','2024'] # Forecast initiation years
start_months = ['10','11','12','01','02','03','04'] # ['10','11','12','01','02','03','04'] # Forecast start/ valid month
lead_times = [1,2] # Lead month(s)/ extension of forecast from start month e.g. 1 or 2 month forecast
forecasts = ['','weatherlogisticsltd']

for lead_time in lead_times:
    
    for mth_index, start_month in enumerate(start_months):

        lead_month = (int(start_month)+lead_time-1) % 12
        if lead_month < int(start_month):
            year_lead = int(start_years[mth_index]) + 1
        else:
            year_lead = int(start_years[mth_index])
        month_long = calendar.month_name[lead_month+1]
        print(month_long)
        
        now = datetime.datetime.now()
        copy_yr = now.year
        
        '''User to define 2 ascii plots to be compared'''
        ascii_files = []
        for forecast in forecasts:
            ascii_files.append(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}_Temperature{forecast}.asc')
        #
        title = (f'Degrees Celsius Departure from Recent Climate Mean\n{month_long} {year_lead}')
        variable_units = "Mean Temperature/ DegC Departure"
        
        plt.figure(dpi=350, figsize=(10, 10))
        ax = plt.axes(projection=ccrs.Mercator(), frameon=True)
        # ax.suptitle("Re-Climate® February Temperature Forecast. Copyright "+str(copy_yr)+". All rights reserved.")
        
        # Read in Re-Climate data header data
        for ascii_file in ascii_files:
            with open(ascii_file, 'r') as data_f:
                data_header = data_f.readlines()[:6]
             
            # Read the Re-Climate ASCII raster header
            data_header = [item.strip().split()[-1] for item in data_header]
            data_cols = int(data_header[0])
            data_rows = int(data_header[1])
            data_xll = float(data_header[2])
            data_yll = float(data_header[3])
            data_cs = float(data_header[4])
            data_nodata = float(data_header[5])
             
            # Read in the data array
            data_arrayx = np.loadtxt(ascii_file, dtype=np.float, skiprows=6)
        
            # Set the nodata values to nan
            data_arrayx[data_arrayx == data_nodata] = np.nan
            
            # Collate into array
            if ascii_file == ascii_files[0]:
                data_array = data_arrayx
            else:
                data_array += data_arrayx
        
        # Divide by forecast length
        data_array /= len(ascii_files)
        
        # Plot Re-Climate ASCII grid with colorbar
        ax.set_title(title)
        
        # Show a colorbar legend
        img_plot = ax.imshow(data_array, cmap='seismic', vmin=-1.75, vmax=2.25)
         
        ax.grid(True)
        
        # Place a colorbar next to the map
        plt.suptitle('RE-CLIMATE Seasonal Climate Forecast', y=1.05, fontsize=18)
        plt.colorbar(img_plot,orientation="horizontal",ax=ax,
                    pad=0,
                    aspect=50)
        
        # Save
        if len(forecasts) == 1:
            plt.savefig(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}_Temperature{forecast}.png', dpi=350, bbox_inches='tight')
        else:
            plt.savefig(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}_TemperatureCOMBINED.png', dpi=350, bbox_inches='tight')
        # Show forecast plots
        plt.show()
