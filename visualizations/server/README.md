# Running the interactive map
This directory contains scripts to visualize an interactive map of the address data.
The map can be controlled, panned and zoomed. 

There are two flavours available:

**Heatmap (interactive_map.py)**: Visualizes the density of the addresses as heatmap.

**Viewer (interactive_map_alt.py)**: Visualizes all the addresses with a tile background.

## Prerequisites
This visualization requires Python 3 and pip to be installed.

The script assumes you have saved the address file named `belgium_addresses.csv` in the directory `data/` in the root of the repository. See the other readmes on how to use the scripts to generate this file. 

## Installation
Install the dependencies via pip.

```bash
pip install -r requirements.txt
```

## Deployment
To run the map locally:
```bash
bokeh serve --show interactive_map.py
# or
bokeh serve --show interactive_map_alt.py
```

To deploy on a server you can consult the guide on deploying bokeh visualizations: https://bokeh.pydata.org/en/latest/docs/user_guide/server.html