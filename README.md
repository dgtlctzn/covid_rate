# Rate of Covid-19 by Country
Tracking the rate of Covid-19 on a Raspberry Pi

The rate of Covid of 22 countries is determined from total cases divided by country population. The data is wrangled with Pandas. The script is run every 12 hours and stores the rates by country in a .csv. Sources for Covid counts are found here:

www.wikipedia.org/wiki/COVID-19_pandemic

And country populations here:

www.worldometers.info/world-population/population-by-country/

## Analysis
Jupyter notebooks is used to graph Covid rates over time. 

The first notebook graphs 19 countries using matplotlib. The second notebook takes the Covid rate of the U.S. and applies both linear and third order polynomial regression to investigate the trends in the rate. Root Mean Squared Error is calculated to give a comparison of linear and polynomial best fit lines.
