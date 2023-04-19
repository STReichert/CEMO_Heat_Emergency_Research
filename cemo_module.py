"""Module with custom functions for use in CEMO Heat Emergency Project"""

import pandas as pd
import geopandas as gpd
import numpy as np
import osgeo.gdal
from rasterstats import zonal_stats
import rioxarray as rxr
import rasterio as rio
from affine import Affine
import warnings
warnings.filterwarnings("ignore", message="pandas.Int64Index") # needed to supress repeated future warning in loop https://github.com/GenericMappingTools/pygmt/issues/1946

def interpolate_temp(temp_gdf:gpd.GeoDataFrame, district_shapes:gpd.GeoDataFrame, date:str, col:str):
    """
    Takes in the the temperature dataframe, fire districts, date to slice by and column to interpolate
    Returns geodataframe in shape of districts_shapes with interpolated mean data for date and col
    
    Arguments:
        temp_gdf: Geodataframe of weatherstations with data \n
        districts_shapes: GeoDataFrame of districts to interpolate to \n
        date: date to slice temp_gdf by \n
        col: column to interpolate in temp_gdf
    """
    bounds = district_shapes.total_bounds
    temp_station_path = 'data/working/temp_data.shp'
    temp_raster_path = 'data/working/temp_raster.tiff'
    temp_gdf = temp_gdf[['date_time', col, 'geometry']]
    temp_gdf = temp_gdf.rename(columns={col:'z_col'})
    temp_gdf['date_time'] = temp_gdf['date_time'].astype(str) #avoids shapefile error with processing datetime types
    temp_gdf[temp_gdf['date_time']==date].to_file('data/working/temp_data.shp') # slice data by date and create shapefile for interpolating

    rasterDs = osgeo.gdal.Grid(
        temp_raster_path,
        temp_station_path,
        format='GTiff',
        zfield='z_col',
        outputBounds=bounds,
        algorithm='invdist',
    )
    
    rasterDs = None
    del rasterDs

    ### For some reason GDAL creates a raster with unexpected affine transform that begins in lower left corner
    ### we must create an affine transorm with a negative cell height and flip the array to read the data properly for zonal stats

    af = Affine(0.002003195255464829, 0.0, -118.66818799560865,
       0.0, -0.002475198135987511, 34.33730781636643)
    
    
    with rio.open(temp_raster_path) as src:
    # Read the raster data as an array
        raster_array = src.read(1)
        
        # Flip the array vertically
        flipped_array = np.flip(raster_array, axis=0)
        
        # Update the metadata of the raster
        kwargs = src.meta.copy()
        
        # Write the flipped raster to a new file
        with rio.open(temp_raster_path, 'w', **kwargs) as dst:
            dst.write(flipped_array, 1)
            dst.transform = af
        
    data = rio.open(temp_raster_path)
    stats = pd.DataFrame(zonal_stats(district_shapes, data.read(1), affine=af, stats=['mean']))
    stats_gdf = district_shapes.join(stats)
    stats_gdf = stats_gdf.rename(columns={'mean':col})
    stats_gdf['date_time'] = date

    return stats_gdf

def heat_index(t:float, rh:float) -> float:
    """
    Calculate Heat Index or "Feels Like" temperature from air temperature and relative humidity

    Arguments:
        t: air temperature\n
        rh: relative humidity\n

    formula source: https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
    """
    HI = 0.5*(t + 61 + ((t-68)*1.2) + (rh*0.094)) # general formula for days where the average between this and the air temp is less than 80

    if ((HI+t)/2) > 80:
        HI = (-42.379 + 
            2.04901523*t + 10.14333127*rh - 
            0.22475541*t*rh - 0.00683783*t*t - 0.05481717*rh*rh + 
            0.00122874*t**2*rh + .00085282*t*rh**2 - 
            .00000199*t**2*rh**2
        )
    # conditional adjustments 
        if rh < 13 and 80 < t < 112:
            HI = HI - (((13-rh)/4)* math.sqrt((17-abs(t-95))/17)) 
        elif rh > 85 and 80 < t < 87:
            HI = HI + (((rh-85)/10)*((87-t)/5))

    return HI