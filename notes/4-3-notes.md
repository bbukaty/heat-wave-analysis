

psm_scale_factor is 1 for all years in NSRDB.
checked with this script:
```
for year in [str(year) for year in range(1998, 2024)]:
    nsrdb_year = h5pyd.File(f"/nrel/nsrdb/v3/nsrdb_{year}.h5", 'r')
    ghi = nsrdb_year['ghi']
    print(ghi.attrs["psm_scale_factor"])
```


Fort Ross Monthly Calendar Query
https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9416024&units=standard&bdate=20160601&edate=20160630&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=monthlychart


ask tide scientist if MLLW datum is reasonable

historical ghi does capture cloudiness, what are the implications of that