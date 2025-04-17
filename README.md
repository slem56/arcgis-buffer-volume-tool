# Automated ArcGIS Surface Volume Model

## Description

This is an ArcGIS automation tool that filters features affecting the watertable depth and calculates surface volume from interpolated depth data. The tool uses a series of buffer distances to filter out nearby features that affect water table depth and helps identify the optimal buffer distance for accurate water table depth analysis. 

This tool was created using ArcGIS ModelBuilder and modified for automation.

## Key Features
- **Watertable Depth Interpolation**: Uses Inverse Distance Weighting (IDW) to interpolate watertable depths.
- **Feature Filtering**: Removes the influence of features that affect watertable depth, ensuring more accurate results.
- **Surface Volume Calculation**: Calculates the surface volume based on the filtered depth data.
- **Buffer Distance Optimisation**: Identifies the best buffer distance by testing various distances and logging the results.

## Example Output
The output is a .txt file with the buffer and volume. It will look like this:

```
0	1916113334
10	1755721866
20	1762712317
```
