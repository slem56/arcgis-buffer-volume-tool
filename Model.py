"""
Automated ArcGIS workflow to:
- Filter features within a mask
- Perform IDW interpolation
- Extract raster by mask
- Calculate surface volume
- Log output volume and area for each buffer distance

Created using ArcGIS ModelBuilder and modified for automation.
"""
import arcpy
from arcpy.sa import *
import os

base_path = "path/to/data"

def Model(Buffer = 0):  # Model
    print("start " + str(Buffer))

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")

    output_file_location = os.path.join(base_path, "output.txt")

    with open(output_file_location, "a") as output_file:
        
        depths = os.path.join(base_path, "depths.shp")
        area_mask = os.path.join(base_path, "area_mask.shp")
        features = os.path.join(base_path, "features.shp")

        # Process: Make Feature Layer (Make Feature Layer) (management)
        Output_Layer = "depths_Layer"
        arcpy.management.MakeFeatureLayer(in_features=depths, out_layer=Output_Layer)

        # Process: Select Layer By Location (Select Layer By Location) (management)
        depths_2_, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[Output_Layer], overlap_type="COMPLETELY_WITHIN", select_features=area_mask)

        # Process: Select (Select) (analysis)
        features_Select = os.path.join(base_path, "features_Select")
        arcpy.analysis.Select(in_features=features, out_feature_class=features_Select, where_clause="CHAN_TYPE = 'SUPPLY' Or CHAN_TYPE = 'ESCAPE'")

        # Process: Select Layer By Location (2) (Select Layer By Location) (management)
        depths_3_, Output_Layer_Names_2_, Count_2_ = arcpy.management.SelectLayerByLocation(in_layer=[depths_2_], overlap_type="WITHIN_A_DISTANCE", select_features=features_Select, search_distance=Buffer, selection_type="REMOVE_FROM_SELECTION")

        # Process: IDW (IDW) (sa)
        Idw_depths = os.path.join(base_path, "Idw_depths")
        IDW = Idw_depths
        Idw_depths = arcpy.sa.Idw(depths_3_, "RD03alt", "204.600412805364", 2, "VARIABLE 12", "")
        Idw_depths.save(IDW)

        # Process: Extract by Mask (Extract by Mask) (sa)
        Output_raster = os.path.join(base_path, "Extract_Idw")
        Extract_by_Mask = Output_raster
        Output_raster = arcpy.sa.ExtractByMask(Idw_depths, area_mask, "INSIDE")
        Output_raster.save(Extract_by_Mask)

        # Process: Surface Volume (Surface Volume) (3d)
        VOL_2_txt = os.path.join(base_path, "VOL_2.txt")
        arcpy.ddd.SurfaceVolume(in_surface=Output_raster, out_text_file=VOL_2_txt, reference_plane="BELOW")
        
        with open(VOL_2_txt, "r") as volume_file_txt:
            volume_file = volume_file_txt.read()
            volume_file = volume_file.split()
            volume = volume_file[-1].strip()
            area = volume_file[-3].replace(",","").strip()

        output_file.write(f"{Buffer} {volume} {area}\n")
    

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="path/to/scratchWorkspace", workspace="path/to/workspace"):
        Buffer = 0
        max_buffer = 500
        while Buffer < max_buffer:
            Model(Buffer)
            Buffer += 10
            print(str(Buffer/max_buffer*100) + "%")
