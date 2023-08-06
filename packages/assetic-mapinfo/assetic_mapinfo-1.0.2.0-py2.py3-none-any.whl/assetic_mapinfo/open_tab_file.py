from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import osgeo
import os.path
import json

#lassetID = 248843
tab_path = r"C:\Projects\Nillumbik\Ancillary.TAB"

def fetch_records_from_table(tab_path):
    """
    Get dataframe from tab file
    :param tab_path: the file and path of tab fille
    :return: dataframe and alias with TAB data
    """
    # table_ds = None
    # feature_df = None
    table_alias = ""
    rows = []
    field_names = []
    table_lr = None

    try:
        if tab_path and os.path.isfile(tab_path):
            ogr.UseExceptions()
            table_ds = ogr.Open(tab_path)
            if table_ds:
                # fetch entire table into DataFrame
                table_lr = table_ds.GetLayer()
                if table_lr:
                    table_alias = table_lr.GetName()
                    field_names = [
                        field.name for field in table_lr.schema]
                    print(f"layer: {', '.join(field_names)}")
                    for feature in table_lr:
                        row = dict()
                        for i in range(0, len(field_names)):
                            # get field value of feature
                            row[field_names[i]] = \
                                feature.GetField(field_names[i])

                        # get the geometry
                        geometry = feature.GetGeometryRef()

                        # Include length and area from geometry
                        row["_geometry_length_"] = None
                        try:
                            row["_geometry_length_"] = geometry.Length()
                        except Exception:
                            pass
                        row["_geometry_area_"] = None
                        try:
                            row["_geometry_area_"] = geometry.GetArea()
                        except Exception:
                            pass

                        # include geoJSON for geometry and the centroid
                        centroid = geometry.Centroid()
                        geojson = get_geom_geojson(4326, geometry,
                                                        centroid)
                        if geojson and geojson != "":
                            row["geom_geojson"] = geojson
                        else:
                            row["geom_geojson"] = None

                        rows.append(row)
                    field_names.append("_geometry_length_")
                    field_names.append("_geometry_area_")
                    field_names.append("geom_geojson")
                    # processed the features
                    table_lr = None
                table_ds = None
            else:
                print("Tab file not opened")
        else:
            print(f"Failed to find table: {tab_path}")
    except Exception as e:
        print("Failed to read table: {}".format(e))

    return rows, field_names, table_alias


def get_geom_geojson(out_srid, geometry, centroid=None):
    """
    Get the geojson for a geometry in 4326 projection
    :param out_srid: The projection EPSG code to export WKT as (integer)
    :param geometry: The input geometry
    :param centroid: The geometry centroid, use for polygons in case polygon
    orientation is wrong.  Optional
    :returns: wkt string of geometry in the specified projection
    """

    # define output spatial reference
    to_sr = osr.SpatialReference()
    to_sr.ImportFromEPSG(out_srid)
    if int(osgeo.__version__[0]) >= 3:
        # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
        to_sr.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    # define input spatial reference from geom
    from_sr = geometry.GetSpatialReference()
    # set transformation
    transform = osr.CoordinateTransformation(from_sr, to_sr)

    # apply transformation
    chk = geometry.Transform(transform)
    if chk != 0:
        # didn't transform
        print("Unable to reproject feature")
        return ""

    geojsonstr = geometry.ExportToJson()
    geojson = json.loads(geojsonstr)
    centroid_geojson = None
    if "type" in geojson and geojson["type"].lower() == "polygon":
        # get centroid for polygon in case polygon orientation bad it
        # avoids Assetic Cloud trying to get centroid for bad polygon
        chk = centroid.Transform(transform)
        if chk == 0:
            centroid_geojson_str = centroid.ExportToJson()
            centroid_geojson = json.loads(centroid_geojson_str)
    if "GeometryCollection" not in geojson:
        # Geojson is expected to include collection, but ExportToJson
        # does not include it
        if centroid_geojson:
            fullgeojson = {
                "geometries": [geojson, centroid_geojson]
                , "type": "GeometryCollection"}
        else:
            fullgeojson = {
                "geometries": [geojson]
                , "type": "GeometryCollection"}
    else:
        # not try to include centroid, too messy.  Am not expecting to hit
        # this case unless ExportToJson changes
        fullgeojson = geojson

    return fullgeojson

if __name__ == "__main__":
    fetch_records_from_table(tab_path)