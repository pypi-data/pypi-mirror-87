import netCDF4 as nc

#    GCW / WMO recommends including only one borehole per dataset (erddap/opendap)
#    but this means that if you have a larger dataset that comprises many boreholes, 
#    each will be required to have its own title & ID, whereas you might want the files to be 
#    grouped into their own title, and especially if "ID" is used to be the DOI, you want one for
#    the larger datset.
#
#    Ground temperature stations are much less costly and easier to set up than ocean mooring cables,
#    so it is more likely that a dataset submission will have many more of them.
#     
#    Including multiple stations in a file would require having indices for depth and time, because
#    not all stations will have the same depths (or number of sensors), and they may not
#    record at the same time (and may not have the same number of recordings).
#
#    One solution is to not expect that individual sites have *all* of the ACDD information since
#    we are not using them to represent 'full' datasets. This keeps them useful as a way to store and
#    transmit data. If we want to combine them into 'full' datasets with IDs then that is possible with
#    some further work.

def nc_new_file(ncfile_out):
    rootgrp = nc.Dataset(ncfile_out, 'w', format='NETCDF4_CLASSIC')
    rootgrp.Conventions = 'CF-1.8, ACDD'
    rootgrp.featureType = "TimeSeriesProfile"

    return rootgrp

def ncdim_add_station(rootgrp, n=1):
    dim = rootgrp.createDimension('station', size=n)

    return dim

def ncdim_add_strlen(rootgrp, n=32):
    dim = rootgrp.createDimension('strlen', size=n)

    return dim

def ncdim_add_time(rootgrp):
    dim = rootgrp.createDimension('time', size=0)
    
    return dim

def ncdim_add_depth(rootgrp, n=1):
    dim = rootgrp.createDimension('depth', size=n)

    return dim


def ncvar_add_latitude(rootgrp, dimensions=('station')):
    latitude  = rootgrp.createVariable('latitude', 'f8', dimensions)
    latitude.long_name  = 'latitude'
    latitude.units  = 'degrees_north'
    latitude.standard_name = 'latitude'
    latitude.axis  = 'Y'

    return latitude

def ncvar_add_longitude(rootgrp, dimensions=('station')):
    longitude           = rootgrp.createVariable('longitude', 'f8', dimensions)
    longitude.long_name = 'longitude'
    longitude.units     = 'degrees_east'
    longitude.standard_name = 'longitude'
    longitude.axis  = 'X'

    return longitude

def ncvar_add_time(rootgrp, units, calendar, dimensions=('time'), dtype='i4'):
    time           = rootgrp.createVariable('time', dtype, dimensions)
    time.long_name = 'time'
    time.units     = units
    time.calendar  = calendar
    time.standard_name = 'time'
    time.axis = 'T'
    time.cf_role = 'profile_id'

    return time

def ncvar_add_ground_temp(rootgrp, dimensions=('station', 'time', 'depth')):
    longitude           = rootgrp.createVariable('ground_temperature', 'f8', dimensions)
    longitude.long_name = 'ground temperature'
    longitude.units     = 'degrees_C'
    longitude.standard_name = 'soil_temperature'
    longitude.axis  = 'X'

    return longitude

def ncvar_add_depth(rootgrp, dimensions=('depth')):
    longitude           = rootgrp.createVariable('depth', 'f8', dimensions)
    longitude.long_name = 'depth below the surface'
    longitude.units     = 'm'
    longitude.standard_name = 'depth'


    return longitude


def ncvar_add_station(rootgrp, dimensions=('station')):
    station             = rootgrp.createVariable('station', 'i4', dimensions)
    station.long_name   = 'station for time series data'
    station.units       = '1'

    return station

def ncvar_add_ellipsoid_height(rootgrp, dimensions=('station')):
    height           = rootgrp.createVariable('height', 'f4', dimensions)
    height.long_name = 'Elevation relative to ellipsoid'
    height.units     = 'm'
    height.axis      = 'Z'
    height.standard_name = 'height_above_reference_ellipsoid'
    height.positive  = 'up'

    return height

def ncglobal_add_attributes(rootgrp, attr_dict):
    for key in attr_dict:
        value = attr_dict[key]
        rootgrp.setncattr(key, value)

def create_nc(ncfile_out):

    rootgroup = nc_new_file(ncfile_out)


global_cf_dict = {}

global_acdd_dict = {}

def nc_ground_temperature(ncfile):
    rootgrp = nc_new_file(ncfile)
    
    ncdim_add_station(rootgrp)
    ncdim_add_depth(rootgrp)
    ncdim_add_time(rootgrp)
    ncdim_add_strlen(rootgrp)

    lat = ncvar_add_latitude(rootgrp)
    lon = ncvar_add_longitude(rootgrp)
    depth = ncvar_add_depth(rootgrp)
    #time = ncvar_add_time(rootgrp)
    tg = ncvar_add_ground_temp(rootgrp)
    tg = ncvar_add_station(rootgrp)

    ncglobal_add_attributes(rootgrp, global_acdd_dict)
    
    return rootgrp

if __name__ == "__main__":
    pass
    