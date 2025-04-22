# Automated ArcGIS Surface Volume Model

## Description

This is an ArcGIS automation tool that filters channels affecting the watertable depth and calculates surface volume from interpolated depth data. The tool uses a series of buffer distances to filter out nearby channels (specifically `SUPPLY` or `ESCAPE` channels) and helps identify the optimal buffer distance for accurate water table depth analysis.  

Originally created using ArcGIS ModelBuilder, the tool has been modified for automation using Python and ArcPy.

## Key Features

- **Watertable Depth Interpolation**: Uses Inverse Distance Weighting (IDW) to interpolate watertable depths from shapefile point data.
- **Channel Influence Filtering**: Filters out depths located within a given buffer of `SUPPLY` and `ESCAPE` channel features.
- **Masking & Clipping**: Uses a spatial mask to ensure only relevant areas are analyzed.
- **Surface Volume Calculation**: Computes the surface volume below the interpolated depth surface.
- **Automated Buffer Testing**: Loops through multiple buffer distances to evaluate their impact and logs the results.

## Output

The tool creates a text file (`output.txt`) inside the specified `data_dir`. This file contains two columns:
- **Buffer**: The buffer distance in map units (e.g., meters)
- **Volume**: The corresponding volume calculated from the depth interpolation.

If the output file does not exist or is empty when the tool is run, a heading row (`Buffer Volume`) is automatically written at the top.

### Example Output

```
Buffer Volume
0 1916113334
10 1755721866
20 1762712317
```
