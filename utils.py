import os
import pickle
import h5pyd
import pandas as pd


def get_nsrdb_data(data_year, datum, site_idx, site_timezone):
    """Get the full year of ghi data for this site from NSRDB

    Args:
        data_year (String): e.g. 2016
        site_idx (int): NSRDB site index, see yearly_ghi.ipynb
        site_timezone (String): pandas timezone string, e.g.g America/Los_Angeles

    Returns:
        site_ghi_series: a 1d ndarray with ghi values for the year
        time_series: a pandas DateTimeIndex localized to the site timezone.
    """    
    

    cached_data_path = f'cached/site-{site_idx}-data-{data_year}.pkl'
    if os.path.exists(cached_data_path):
        print(f'Found {cached_data_path}, loading...')
        with open(cached_data_path, 'rb') as file:
            ghi_series = pickle.load(file)
    else:
        print('No cached data found, querying NSRDB...')
        nsrdb_year = h5pyd.File(f'/nrel/nsrdb/v3/nsrdb_{data_year}.h5', 'r')
        
        site_ghi_series = nsrdb_year[datum][:, site_idx]
        site_time_series_naive = pd.to_datetime(nsrdb_year['time_index'][...].astype(str))
        # timestamps for the ghi data are in UTC so we localize them here for convenience
        site_time_series = site_time_series_naive.tz_localize('UTC').tz_convert(site_timezone)

        ghi_series = pd.Series(data=site_ghi_series, index=site_time_series)
        
        with open(cached_data_path, 'wb') as file:
            pickle.dump((ghi_series), file)
    
    return ghi_series

