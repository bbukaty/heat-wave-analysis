

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

cubic interpolation for tides is ok?

tide-normalized ghi:
low low tide should be 1? fine if it's above 1
what should be 0 exactly? high tide?
probably just a cutoff of what we consider intertidal. tide gets even higher, still 0 sun.

highest observed tide datum would be ideal but fort ross, for example, doesn't seem to offer that datum

so for now I settled on just min and max over the month/year