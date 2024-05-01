import os
import pickle
import h5pyd
import requests

import matplotlib.dates as mdates
import pandas as pd

from scipy.interpolate import interp1d

TZ_LA = 'America/Los_Angeles'
SITES = {
    'Fort Ross': {
        'name': 'Fort Ross',
        'tz': TZ_LA,
        'loc': (38.51265, -123.24647),
        'noaa_station_id': 9416024,
        'nsrdb_site_id': 131123
    },
    'San Diego': {
        'name': 'San Diego',
        'tz': TZ_LA,
        'loc': (32.648372, -117.165832),
        'noaa_station_id': 9410170
    },
    'Santa Barbara': {
        'name': 'Santa Barbara',
        'tz': TZ_LA,
        'loc': (34.41968, -119.71602),
        'noaa_station_id': 9411340
    }
}

# MONTH_COLORS = {
#     1: 'violet',
#     4: 'gray',
#     5: 'darkred',
#     6: 'red',
#     7: 'orange',
#     8: 'gold',
#     9: 'lightgreen',
#     10: 'green',
#     11: 'blue',
#     12: 'darkblue',
#     12: 'magenta'
# }

MONTH_COLORS = {
    1: 'gray',
    4: 'darkred',
    5: 'red',
    6: 'orange',
    7: 'gold',
    8: 'lightgreen',
    9: 'green',
    10: 'blue',
    11: 'darkblue',
    12: 'magenta'
}


def get_nsrdb_data(data_year, datum, site_idx, site_timezone):
    """Get the full year of ghi data for this site from NSRDB.
    Args:
        data_year (String): e.g. 2016
        site_idx (int): NSRDB site index, see yearly_ghi.ipynb
        site_timezone (String): timezone string, e.g. America/Los_Angeles

    Returns:
        data_year (pandas.core.Series): NSRDB year of that datum
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
            print(f'Saved {cached_data_path}.')
            pickle.dump((ghi_series), file)

    return ghi_series


def get_hot_rocks_data():
    file_path = 'external/hot-rocks/supplementary_fort_ross_temps.csv'
    data = pd.read_csv(file_path, parse_dates=['dt'], date_format='%m/%d/%y %H:%M')

    # had a bit of difficulty with the lack of timezones in the data, have to manually indicate no daylight savings time here
    data['dt'] = pd.DatetimeIndex(data['dt']).tz_localize('America/Los_Angeles', ambiguous=False)
    data.set_index('dt', inplace=True)
    data.sort_index(inplace=True)
    return data


def noaa_date_format(pd_date):
    return pd_date.strftime('%Y%m%d')


def get_month_padded(year, month):
    # these padding and formatting methods for the noaa api are a bit jank,
    # but they work for now.
    start_of_month = pd.to_datetime(f'{year}-{month}')
    end_of_month = start_of_month + pd.offsets.MonthEnd()
    begin_date = (start_of_month - pd.Timedelta(days=1))
    end_date = (end_of_month + pd.Timedelta(days=1))
    return noaa_date_format(begin_date), noaa_date_format(end_date)


def get_year_padded(year):
    end_of_prev = pd.to_datetime(f'{year-1}-12-31')
    start_of_next = pd.to_datetime(f'{year+1}-01-01')
    return noaa_date_format(end_of_prev), noaa_date_format(start_of_next)


def get_noaa_tide_preds(site, date_range):
    begin_date, end_date = date_range

    params = {
        'product': 'predictions',
        'application': 'NOS.COOPS.TAC.WL',
        'begin_date': begin_date,
        'end_date': end_date,
        'datum': 'MLLW',  # is this reasonable? https://tidesandcurrents.noaa.gov/datum_options.html
        'station': site['noaa_station_id'],
        'time_zone': 'lst_ldt',
        'units': 'english',
        'interval': 'hilo',
        'format': 'json'
    }

    url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'
    tide_api_response = requests.get(url, params=params)

    if tide_api_response.status_code != 200:
        raise Exception(f"Failed to get NOAA tide data for specified dates; error code {tide_api_response.status_code}")

    tide_predictions_df = pd.DataFrame(tide_api_response.json()['predictions'])

    # make sure the pandas dataframe includes the tide data timezone.
    # right now we don't have a great single source of truth for site timezones,
    # we're just assuming that lst_ldt for this station matches up with our hardcoded site timezone in utils.
    tide_index = pd.DatetimeIndex(tide_predictions_df['t']).tz_localize(site['tz'])
    tide_series = pd.Series(data=tide_predictions_df['v'].values, index=tide_index, dtype=float)
    return tide_series


def interpolate_tide_preds(tide_series, desired_time_index):
    """Use cubic interpolation to reconstruct a high-res tide curve from hilo predictions."""
    tide_timestamps_numeric = mdates.date2num(tide_series.index)
    interpolator = interp1d(tide_timestamps_numeric,
                            tide_series, kind='cubic', fill_value='extrapolate')

    tide_high_res_numeric = interpolator(mdates.date2num(desired_time_index))
    tide_high_res = pd.Series(
        data=tide_high_res_numeric, index=desired_time_index)
    return tide_high_res


def normalize_series(series) -> pd.Series:
    min_val, max_val = series.min(), series.max()
    return (series - min_val) / (max_val - min_val)