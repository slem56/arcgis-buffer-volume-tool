import arcpy
from arcpy.sa import *
import os

def Model(Buffer, depths, channels, area_mask, data_dir):  # Modified Model function
    """
    Performs a geospatial volume calculation using ArcPy by excluding depth data near specified channel features.

    Args:
        Buffer (str | float): The buffer distance (e.g., "100 Meters") used to exclude depth points located near 'SUPPLY' or 'ESCAPE' channels.
        depths (str): Path to the depth shapefile.
        channels (str): Path to the channels shapefile.
        area_mask (str): Path to the area mask shapefile.
        data_dir (str): Directory where data is stored and outputs will be saved.

    Returns:
        bool: True upon successful execution.
    """
    print(f"Start model with buffer = {Buffer}")

    arcpy.env.overwriteOutput = True
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")

    output_file_location = os.path.join(data_dir, "output.txt")
    # Write header if file doesn't exist or is empty
    if not os.path.exists(output_file_location) or os.stat(output_file_location).st_size == 0:
        with open(output_file_location, "w") as output_file:
            output_file.write("Buffer Volume\n")

    with open(output_file_location, "a") as output_file:
        
        # Make Feature Layer
        Output_Layer = "depths_Layer"
        arcpy.management.MakeFeatureLayer(in_features=depths, out_layer=Output_Layer)

        # Select depths within area mask
        depths_2_, _, _ = arcpy.management.SelectLayerByLocation(
            in_layer=[Output_Layer], overlap_type="COMPLETELY_WITHIN", select_features=area_mask)

        # Select SUPPLY and ESCAPE channels
        channels_Select = "channels_Select"
        arcpy.analysis.Select(
            in_features=channels,
            out_feature_class=channels_Select,
            where_clause="CHAN_TYPE = 'SUPPLY' Or CHAN_TYPE = 'ESCAPE'"
        )

        # Remove depths within buffer of selected channels
        depths_3_, _, _ = arcpy.management.SelectLayerByLocation(
            in_layer=[depths_2_],
            overlap_type="WITHIN_A_DISTANCE",
            select_features=channels_Select,
            search_distance=Buffer,
            selection_type="REMOVE_FROM_SELECTION"
        )

        # IDW interpolation
        Idw_output = "Idw_depths"
        Idw_raster = arcpy.sa.Idw(depths_3_, "depth", "204.600412805364", 2, "VARIABLE 12", "")
        Idw_raster.save(Idw_output)

        # Extract by mask
        Extract_output = "Extract_Idw"
        Extracted_raster = arcpy.sa.ExtractByMask(Idw_raster, area_mask, "INSIDE")
        Extracted_raster.save(Extract_output)

        # Surface volume calculation
        VOL_2_txt = os.path.join(data_dir, "VOL_2.txt")
        arcpy.ddd.SurfaceVolume(in_surface=Extracted_raster, out_text_file=VOL_2_txt, reference_plane="BELOW")

        with open(VOL_2_txt, "r") as volume_file_txt:
            volume_file = volume_file_txt.read().split()
            volume = volume_file[-1].strip()

        output_file.write(f"{Buffer} {volume}\n")

    return True


if __name__ == '__main__':
    # Set global environment settings
    with arcpy.EnvManager(scratchWorkspace="path/to/scratchWorkspace", workspace="path/to/workspace"):
        data_dir = "path/to/data"
        depths = os.path.join(data_dir, "depths.shp")
        channels = os.path.join(data_dir, "channels.shp")
        area_mask = os.path.join(data_dir, "area_mask.shp")

        Buffer = 0
        max_buffer = 500
        while Buffer < max_buffer:
            Model(Buffer, depths, channels, area_mask, data_dir)
            Buffer += 10
            print(f"{Buffer / max_buffer * 100} %")
