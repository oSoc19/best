from colorcet import fire
import pandas as pd
import numpy as np
from pyproj import Transformer

import holoviews as hv
import holoviews.operation.datashader as hd

# Set rendering options
hd.shade.cmap = ['#5454cc']
hv.extension("bokeh")
renderer = hv.renderer('bokeh')

# Read the address file
df = pd.read_csv('../../data/belgium_addresses.csv',
                 usecols=['EPSG:31370_x', 'EPSG:31370_y'])

# Convert to web coordinator to match the tiles
web_co_trans = Transformer.from_crs(31370, 3857)
x_id = df.columns.get_loc('EPSG:31370_x')
y_id = df.columns.get_loc('EPSG:31370_y')

x_vals = np.zeros(len(df))
y_vals = np.zeros(len(df))
for i, row in enumerate(df.values):
    proj = web_co_trans.transform(row[x_id], row[y_id])
    x_vals[i] = proj[0]
    y_vals[i] = proj[1]

df['x'] = x_vals
df['y'] = y_vals

# Calculate range
x_range = (df['x'].min(), df['x'].max())
y_range = (df['y'].min(), df['y'].max())

# Calculate data aspect ratio
data_aspect = (y_range[1] - y_range[0]) / (x_range[1] - x_range[0])

# Setup a datashaded holoview layout
points = hv.Points(df[['x', 'y']].values)
shaded = hd.datashade(points).opts(xaxis=None, yaxis=None)
spreaded = hd.dynspread(shaded, threshold=0.01, max_px=2, how='over').opts(
    aspect=16/8, data_aspect=data_aspect, responsive=True)
# Add tiles
tiles = hv.element.tiles.CartoLight()
comb = tiles * spreaded

# Add to page
doc = renderer.server_doc(comb)
doc.title = 'Address Interactive Map'
