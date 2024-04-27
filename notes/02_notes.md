

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

## Next Steps
What do we really care about?
I'd like to be able to compare two places. how do I do that?


Are we building a "model that identifies heat waves"?
- well, no, because a definition of heat wave has never included tide before.
- if we ignore tides for a sec can we do that?

do we care about radiation from times other than peak sun?
 - could use a touch of clarification about which factors are important.
 - sun exposure/absorption, air temp, water temp, how does it all come together to be bad for organisms?

