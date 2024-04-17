

psm_scale_factor is 1 for all years in NSRDB.
checked with this script:
```
for year in [str(year) for year in range(1998, 2024)]:
    nsrdb_year = h5pyd.File(f"/nrel/nsrdb/v3/nsrdb_{year}.h5", 'r')
    ghi = nsrdb_year['ghi']
    print(ghi.attrs["psm_scale_factor"])
```

unused now that I'm using pandas functionality more effectively.
def crop_data(data, time_series, data_year, month=None):
    if month:
        start_timestamp = pd.to_datetime(f'{data_year}-{str(month).zfill(2)}-01').tz_localize(time_series.tz)
        end_timestamp = start_timestamp + pd.offsets.MonthEnd(1)
        end_timestamp = end_timestamp.replace(hour=23, minute=59, second=59)
    else:
        # crop to year
        start_timestamp = pd.Timestamp('2016-01-01 00:00:00', tz=time_series.tz)
        end_timestamp = pd.Timestamp('2016-12-31 12:59:59', tz=time_series.tz)
    print(f'cropping data within start: {start_timestamp}, end: {end_timestamp}')

    mask = (time_series >= start_timestamp) & (time_series <= end_timestamp)
    return data[mask], time_series[mask]


Fort Ross Monthly Calendar Query
https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9416024&units=standard&bdate=20160601&edate=20160630&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=monthlychart


ask tide scientist if MLLW datum is reasonable

historical ghi does capture cloudiness, what are the implications of that

cubic interpolation for tides is ok?

tide-normalized ghi:
low low tide should be 1? fine if it's above 1
what should be 0 exactly? high tide?
probably just a cutoff of what we consider intertidal. tide gets even higher, still 0 sun.

highest observed tide datum would be ideal but fort ross, for example, doesn't seem to offer that datum

so for now I settled on just min and max over the month/year