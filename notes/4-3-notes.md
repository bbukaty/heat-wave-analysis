

## Tide Prediction for Arbitrary Lat/Long Unsolved
- it looks like we don't have a good "global tide index" or a model we can consult for any given lat long?  
- private enterprises, e.g. aquatera, stormglass.io, seem to have sprouted up as a result  
- actually, what about FES2014 model? looks a bit involved to set up but possibly what we want

## Solar Radiation Data is Patchy Worldwide

NSRDB International coverage diagram:  
https://nsrdb.nrel.gov/data-sets/international-data

- 2019-present for everywhere but europe/africa
- but maybe we can get that from PVGIS-SARAH2?  
https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/pvgis-user-manual_en#ref-3-choosing-solar-radiation-database

- explanation of the non-satellite reanalysis database called PVGIS-ERA5  
https://joint-research-centre.ec.europa.eu/preliminary-description-new-reanalysis-based-data-pvgis_en


# Context; Possible Metrics to Develop

"a heat wave is a period where the temperature was [a standard deviation above the mean] for 5 days in a row"?

what is "a place at risk of heat stress"?
- a place where intertidal irradiation is high[?]
- a place where low tide frequently[?] intersects with high temperatures

how would you compare the heat stress risk of two different locations?
- shallower slope, "beaching"?
- hotter temperatures
- tides that are more regular, i.e. not semidiurnal?

temperatures are similar but one place more frequently has low tide line up with peak sun

_proportion_ of yearly ghi that was absorbed at low tide


## Metric 1: Tide-Scaled Radiation Absorption
At this location, what percent of solar radiation [in the summer months]? was absorbed by the intertidal zone that day/month/year?

"At Fort Ross in 2016, 28% of solar radiation in the summer months of 2016 was absorbed by the intertidal zone, compared to 32% in Point Reyes."


## Approach 2: Tide-Thresholded Radiation Absorption
At this location, what percent of solar radiation was absorbed when the tide was below [low tide datum]?

"At Fort Ross in 2016, 28% of solar radiation in the summer months of 2016 was absorbed with the tide below the [low tide datum], compared to 32% in Point Reyes."

## Approach Notes
- Neither approach takes intertidal slope into account.

## Technical Notes
2 days, hot then cloudy:
```python
raw_ghi = [0, 0, 200, 400, 600, 650, 600, 300, 50, 0, 0, 0, 100, 100, 200, 300, 300, 300, 50, 0, 0]

daily_total_ghi = [2800, ..., 2800, 1350, ..., 1350]

proportion_daily_ghi = raw_ghi / daily_total_ghi

# sanity check:
# sum of proportion_daily_ghi over a day should == 1

# normalized with min/max of current data (a year, probably)
normalized_inverse_tide = [0.1, 0.2, 0.3, 0.2, 0.3, 0.5, 0.3, ...,]

proportion_daily_ghi_in_intertidal = proportion_daily_ghi * normalized_inverse_tide

# sum of that over the day should be some substantial proportion of 1
```
### Thresholded version:

```python
proportion_daily_ghi = 
```
start with `proportion_daily_ghi`

calculate `tide_below_threshold_mask = tide_values < low_tide_threshold`
 - what is `low_tide_threshold`? probably a yearly value, so `tide_values` above should be for the whole year

`ghi_absorbed_at_low_tide = proportion_daily_ghi & tide_below_threshold_mask`

`proportion_daily_ghi_below_tide_threshold = 

```python
# same as before
proportion_daily_ghi = raw_ghi / daily_total_ghi

tide_below_threshold_mask = tide_values < low_tide_threshold
# where do we get above threshold? probably a yearly value, so `tide_values` below should be for the whole year

tide_thresholded_ghi = proportion_daily_ghi & tide_below_threshold_mask

thresholded_ghi_absorbed_per_day = aggregate(tide_thresholded_ghi, num_values_in_day)

# those daily values should also be some substantial proportion of 1.
# I would expect them to be a bit lower than the scaled version under the assumption that we count less radiation with the hard cutoff.
```

## No Wait
shouldn't be proportion style.

Total thresholded ghi in summer months each year, averaged across years of data.