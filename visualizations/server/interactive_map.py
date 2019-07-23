from colorcet import fire
import pandas as pd
from pyproj import Transformer

import holoviews as hv
import holoviews.operation.datashader as hd

# Set rendering options
hd.shade.cmap = fire
hv.extension("bokeh")
renderer = hv.renderer('bokeh')

# Read the address file
df = pd.read_csv('../../data/belgium_addresses.csv',
                 usecols=['EPSG:31370_x', 'EPSG:31370_y'])

# Set column names for easy access
df.columns = ['x', 'y']

# Calculate range
x_range = (df['x'].min(), df['x'].max())
y_range = (df['y'].min(), df['y'].max())

# Calculate data aspect ratio
data_aspect = (y_range[1] - y_range[0]) / (x_range[1] - x_range[0])

# Setup a datashaded holoview layout
points = hv.Points(df[['x', 'y']].values)
shaded = hd.datashade(points).opts(bgcolor='black', xaxis=None, yaxis=None)
spreaded = hd.dynspread(shaded, threshold=0.01, max_px=2, how='over').opts(
    aspect=16/8, data_aspect=data_aspect, responsive=True)

# Add to page
doc = renderer.server_doc(spreaded)
doc.title = 'Address Interactive Map'
