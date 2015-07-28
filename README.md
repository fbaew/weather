# weather

Build a toolkit of weather scripts for retrieving eg
- radar images
- satellite images
- forecasts
- current and historical conditions

Currently, we have
- radar.py : get the day's radar images for Strathmore weather radar
- satellite.py : get the day's satellite images.

In both cases, we will only grab images that we don't already have. Also, we only grab images from today.
The two scripts are nearly identical, and will soon be combined.


It would be nice if we automatically produced gifs of every hour of activity, or something...

Imagemagick might help:
convert radar_img/* radar.gif
