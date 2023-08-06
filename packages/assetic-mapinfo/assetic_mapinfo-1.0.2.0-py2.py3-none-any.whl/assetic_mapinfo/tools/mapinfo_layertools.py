# coding: utf-8
"""
    assetic.layertools  (layertools.py)
    Tools to assist with using arcgis integration with assetic
"""
from __future__ import absolute_import

import json
import os.path
from typing import List, Any

import osgeo
import six
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo.ogr import Layer, Feature

import assetic
from assetic import AssetToolsCompleteAssetRepresentation
from assetic.tools.shared import LayerToolsBase, ConfigBase
from assetic.tools.shared.progress_tracker import ProgressTracker
from assetic.tools.static_def.enums import Result


class MapInfoLayerTools(LayerToolsBase):
    """
    Class to manage processes that relate to a GIS layer

    layerconfig arg is not mandatory and during testing is not passed in.
    """

    def __init__(self, config: ConfigBase = None):
        super().__init__(config)
        # Enable GDAL/OGR exceptions
        gdal.UseExceptions()

    def get_rows(self, lyr: Layer, fields, query=None):
        """

        expects lyr object to be iterable and return dicts
        of {col: val}.

        :param lyr:
        :param fields:
        :param query:
        :return:
        """
        return self.get_rows_from_layer(lyr)

    def get_rows_from_layer(self, layer: Layer) -> List:
        """
        Retrieves all of the rows from a given layer.

        :param layer:
        :return:
        """

        field_names = [field.name for field in layer.schema]

        rows = []

        for feature in layer:

            # start by adding the feature object to our row dictionary,
            # so we can update the feature with any new information
            row = {"_feature": feature}

            # iterate over all of the field names and retrieve the values
            for i in range(0, len(field_names)):
                # get field value of feature
                row[field_names[i]] = feature.GetField(field_names[i])

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
            try:
                centroid = geometry.Centroid()
                geojson = self.get_geom_geojson(4326, geometry, centroid)
            except AttributeError:
                # if no geometry is defined for the feature, set to None
                geojson = None

            if geojson and geojson != "":
                row["geom_geojson"] = geojson
            else:
                row["geom_geojson"] = None

            rows.append(row)

        if len(rows) == 0:
            self.logger.info(f"No rows in layer '{layer.GetName()}' to process.")
        else:
            self.logger.info(f"Found {len(rows)} features to process.")

        return rows

    def _fetch_records_from_layer(self, tabfile_path):
        """
        Get list of rows from tab file, and appends important information
        back to each row.

        :param tabfile_path: the file and path of tab fille
        :return: dataframe and alias with TAB data
        """
        # table_ds = None
        # feature_df = None
        table_alias = ""
        rows = []
        field_names = []

        self.messager.new_message(f"Tab file to fetch {tabfile_path}")
        try:
            if tabfile_path and os.path.isfile(tabfile_path):
                ogr.UseExceptions()
                table_ds = ogr.Open(tabfile_path)
                if table_ds:
                    # fetch entire table into DataFrame
                    table_lr = table_ds.GetLayer()
                    if table_lr:
                        table_alias = table_lr.GetName()
                        field_names = [
                            field.name for field in table_lr.schema]
                        self.logger.debug(f"layer: {', '.join(field_names)}")
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
                            geojson = self.get_geom_geojson(4326, geometry,
                                                            centroid)
                            if geojson and geojson != "":
                                row["geom_geojson"] = geojson
                            else:
                                row["geom_geojson"] = None

                            rows.append(row)
                        field_names.append("_geometry_length_")
                        field_names.append("_geometry_area_")
                        field_names.append("geom_geojson")
                else:
                    self.messager.new_message("Tab file not opened")
            else:
                self.logger.error(f"Failed to find table: {tabfile_path}")
        except Exception as e:
            self.logger.error("Failed to read table: {}".format(e))

        return rows, field_names, table_alias

    @staticmethod
    def get_field_names(layer: Layer) -> List:
        """
        A method to return the field names of the passed in layer,
        while also appending extra fields that the integration requires.

        :param layer:
        :return:
        """

        field_names = [field.name for field in layer.schema]

        field_names.extend(["_geometry_length_", "_geometry_area_", "geom_geojson"])

        return field_names

    def create_assets(self, lyr: Layer, lyrname=None, query=None):
        """
        For the given layer create new assets for the selected features only if
        features have no assetic guid.

        :param lyr: is the layer to process as a tab file, usually a
        tmp copy of a selection set
        :param lyrname: optionally set layer name, else get table alias
        as name
        :param query: optionally apply query filter
        returns: A list of records with rowid, asset ids to update selection
        """
        if self._configuration_missing():
            return

        if isinstance(lyr, str):
            # passed in value is the filepath to the tabfile, not the actual layer
            if os.path.isfile(lyr) is False:
                msg = (f"Path to tabfile [{lyr}] does not exist. Unable to "
                       "open it.")
                self.messager.new_message(msg)
                return

            table = ogr.Open(lyr, 1)
            lyr = table.GetLayer()

        rows = self.get_rows_from_layer(lyr)

        if len(rows) == 0:
            return

        # get configuration for layer
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(
            lyr, lyrname, "create")

        self.logger.debug("Got layer config from xml")

        if lyr_config is None:
            self.logger.error("Returning early as layerfile has been "
                              "misconfigured. See log output.")
            return

        prog = ProgressTracker(self.messager)

        processed_ids = []
        for i, row in enumerate(rows):
            self.logger.debug(f"Attempting to create asset for row {i}")

            # attempt to create asset, components, dimensions
            result_code, idn = self._new_asset(row, lyr_config, fields)

            prog.add(result_code)
            if result_code in [Result.SUCCESS, Result.PARTIAL]:
                self._update_feature_with_asset_id(lyr, row, "asset_id", idn)
                processed_ids.append(idn)

        prog.calculate()
        msg = prog.display_asset_creation_summary(lyrname)

        # self._mi_common_util.do('Note \"{0}\"'.format(msg)) # todo how do I integrate this

        return processed_ids

    @staticmethod
    def _update_feature_with_asset_id(lyr: Layer, row: dict, assetid_field: str,
                                      idn: dict) -> None:
        """
        Updates the row with asset ID.

        :param lyr: TabFile Layer object
        :param row: dict of row attributes, must contain the "_feature"
        key containing the OGR Feature object (to allow update)
        :param assetid_field: The name of the asset ID field in the row
        :param idn: the IDN dictionary containing the asset ID of the created
        object
        :return: None - modifies in place
        """
        # retrieve the ogr feature object from the row
        feature = row["_feature"]  # type: Feature
        feature.SetField(assetid_field, idn["assetic_ids"]["asset_id"])
        lyr.SetFeature(feature)

    def individually_update_rows(self, rows: List[dict], lyr_config: dict,
                                 fields: List[str], lyrname: str) -> None:
        """
        Iterates over the rows of the layerfile and updates each asset
        using API calls.

        :param rows: <List[dict]> a list of dicts where keys are the
        column names and values are cell contents
        :param lyr_config: <dict> dict defining the relationship
        between xml nodes and the layer's column values
        :param fields: <List[str]> a list of column names from the layer
        :param lyrname: The name of the layer, use for messaging
        :return:
        """

        total = len(rows)

        prog = ProgressTracker(self.messager)

        for i, row in enumerate(rows):
            success_code = self._update_asset(row, lyr_config, fields)

            prog.display_row_progress(lyrname, i, total)
            prog.add(success_code)

        prog.display_asset_update_summary(lyrname)

    def update_assets(self, lyr: Layer, lyrname: str = None, query: str = None):
        """
        For the given layer update assets for the selected features only
        where features have an assetic guid/asset id.
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        :param lyrname
        :param query: optional attribute query to get selection
        """
        if self._configuration_missing():
            return

        if isinstance(lyr, str):
            # passed in value is the filepath to the tabfile, not the actual layer
            if os.path.isfile(lyr) is False:
                msg = (f"Path to tabfile [{lyr}] does not exist. Unable to "
                       "open it.")
                self.messager.new_message(msg)
                return

            table = ogr.Open(lyr, 1)
            lyr = table.GetLayer()

        self.logger.debug("create_asset. file={0}".format(lyr))

        rows = self.get_rows_from_layer(lyr)

        if len(rows) == 0:
            self.logger.info(f"No data found to process for {lyrname}")
            return

        self.logger.info(f"Found {len(rows)} features to process")

        # get configuration for layer
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(
            lyr, lyrname, "update")

        if lyr_config is None:
            return

        if len(rows) > self._bulk_threshold:
            chk, valid_rows = self.bulk_update_rows(
                rows, lyrname, lyr_config)
        else:
            self.individually_update_rows(rows, lyr_config, fields
                                          , lyrname=lyrname)

    def display_in_assetic(self, lyr, tab_file, layer_name=None):
        """
        Open Assetic and display the first selected feature in layer
        Use config to determine if Asset or FL
        :param lyr: The layer find selected features.  Not layer name,
        layer object
        """

        # is it an asset layer?
        for j in self._assetconfig:
            if j["layer"] == layer_name:
                self.display_asset(tab_file, layer_name)
        else:
            lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(
                lyr, lyr.getName(), "display")
            if lyr_config:
                self.display_fl(lyr, lyr_config, idfield)

    def display_asset(self, lyr: str, layer_name: str, lyr_config=None,
                      idfield=None):
        """
        Open assetic and display the first selected feature in layer

        :param lyr: source mapinfo file
        :param layer_name: the name of the layer
        :param lyr_config: the config read from the XML config file
        :param idfield: the name of the GIS field with the assetic
        asset id or guid
        :return:
        """

        if isinstance(lyr, str):
            # passed in value is the filepath to the tabfile, not the actual layer
            if os.path.isfile(lyr) is False:
                msg = (f"Path to tabfile [{lyr}] does not exist. Unable to "
                       "open it.")
                self.messager.new_message(msg)
                return

            table = ogr.Open(lyr, 0)
            lyr = table.GetLayer()

        # get table file as a rows matching field list
        rows = self.get_rows_from_layer(lyr)

        if (rows is None) or (len(rows) == 0):
            self.logger.info(f"No data found to process for {lyr}")
            return

        num_rows = len(rows)
        self.logger.info(f"Found {num_rows} features to process")

        # get configuration for layer
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(
            lyr, layer_name, "display")

        self.logger.debug("Got layer config from xml")

        if lyr_config is None:
            self.logger.error("Returning early as layerfile has been "
                              "misconfigured. See log output.")
            return []

        self.logger.debug("Layer: {0}, id field: {1}".format(
            layer_name, idfield))

        assetid = None
        if idfield in rows[0]:
            assetid = rows[0][idfield]

        if (assetid is None) or (assetid.strip() == ""):
            msg = "Asset ID or Asset GUID is NULL.\nUnable to display asset"
            self.messager.new_message(msg)
            self.logger.warning(str(msg))
            return

        self.logger.debug(f"Selected Asset to display: [{assetid}]")

        # Now launch Assetic
        self.apihelper.launch_assetic_asset(assetid)

    def display_fl(self, lyr, lyr_config=None, idfield=None):
        """
        Open assetic and display the first selected feature in layer
        :param lyr: The layer find selected assets. Not layer name,layer object
        :param lyr_config: config for layer as read from XML
        :param idfield: the assetic ID field
        :return:
        """
        # get layer config details
        if not lyr_config:
            lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(
                lyr, lyr.GetName(), "display")
        if not lyr_config:
            return

        self.logger.debug("Layer: {0}, id field: {1}".format(
            lyr.name, idfield))

        fl_id = None
        for feat in lyr:
            fl_id = feat[idfield]
            break

        if fl_id is None or fl_id.strip() == "":
            msg = "Functional Location ID or GUID is NULL.\nUnable to " \
                  "display Functional Location"
            self.messager.new_message(msg)
            self.logger.warning(str(msg))
            return

        self.logger.debug(
            "Selected Functional Location to display: [{0}]".format(fl_id))

        # Now launch Assetic
        self.apihelper.launch_assetic_functional_location(fl_id)

    def _new_asset(self, row: dict, lyr_config: dict, fields: str):
        """
        Create a new asset for the given search result row

        :param row: a layer search result feature, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :returns: Boolean True if success, else False
        """

        complete_asset_obj = self.get_asset_obj_for_row(
            row, lyr_config, fields)

        # will return the generated assetic ids along with the row id to
        # allow the selection query to be updated becuase we are working
        # with a copy of the table
        id_to_update = {
            "rowid": row["_feature"].GetFID(),
            "assetic_ids": {}
        }

        self.logger.info("Start processing row")

        # Add calculated output fields to field list so that they are
        # considered valid
        all_calc_output_fields = lyr_config["all_calc_output_fields"]

        if all_calc_output_fields:
            fields = list(set(all_calc_output_fields + fields))

        # alias core fields for readability
        corefields = lyr_config["corefields"]

        is_new_asset = self.is_new_asset(corefields, fields, complete_asset_obj)

        if is_new_asset is None:
            # fields not defined in xml config file
            return Result.FAILURE, id_to_update
        elif is_new_asset is False:
            return Result.SKIP, id_to_update

        # set status
        complete_asset_obj.asset_representation.status = \
            lyr_config["creation_status"]

        # Create new asset
        asset_repr = self.assettools.create_complete_asset(complete_asset_obj)

        if asset_repr is None:
            # this occurs when the asset creation has failed
            # components/dimensions - no attempt was made to create
            self.messager.new_message("Asset Not Created - Check log")

            return Result.FAILURE, id_to_update

        # apply asset guid and/or assetid
        if "id" in corefields and corefields["id"] in row.keys():
            # row[corefields["id"]] = asset_repr.asset_representation.id
            # feature.SetField2(
            #    corefields["id"], asset_repr.asset_representation.id)
            id_to_update["assetic_ids"][corefields["id"]] = \
                asset_repr.asset_representation.id

        if "asset_id" in corefields and corefields["asset_id"] in row.keys():
            # row[corefields["asset_id"]] = \
            #    asset_repr.asset_representation.asset_id
            # feature.SetField2(
            #    corefields["asset_id"]
            #    , asset_repr.asset_representation.asset_id)
            id_to_update["assetic_ids"][corefields["asset_id"]] = \
                asset_repr.asset_representation.asset_id

        # apply component id
        for component_dim_obj in asset_repr.components:
            for component_config in lyr_config["components"]:
                component_type = None
                if "component_type" in component_config["attributes"]:
                    component_type = component_config["attributes"][
                        "component_type"]
                elif "component_type" in component_config["defaults"]:
                    component_type = component_config["defaults"][
                        "component_type"]

                # Apply the component GUID to the feature
                if ("id" in component_config["attributes"]) and \
                        (component_type == component_dim_obj.
                                component_representation.component_type) and \
                        component_config["attributes"]["id"] in row.keys():
                    # row[component_config["attributes"]["id"]] = \
                    #    component_dim_obj.component_representation.id
                    # feature.SetField2(
                    #    component_config["attributes"]["id"]
                    #    , component_dim_obj.component_representation.id)
                    id_to_update["assetic_ids"][component_config[
                        "attributes"]["id"]] = \
                        component_dim_obj.component_representation.id

                # Apply the component friendly id to the feature
                if "name" in component_config["attributes"] and \
                        component_type \
                        == component_dim_obj.component_representation \
                        .component_type and \
                        component_config["attributes"]["name"] in row.keys():
                    # row[component_config["attributes"]["name"]] = \
                    #    component_dim_obj.component_representation.name
                    # feature.SetField2(
                    #    component_config["attributes"]["name"]
                    #    , component_dim_obj.component_representation.name)
                    id_to_update["assetic_ids"][component_config[
                        "attributes"]["name"]] = \
                        component_dim_obj.component_representation.name

        # apply FL ids to feature
        if asset_repr.functional_location_representation:
            fl_resp = asset_repr.functional_location_representation
            fl_conf = lyr_config["functionallocation"]
            # apply guid if there is a field for it
            if "id" in fl_conf and fl_conf["id"] in row.keys():
                # row[fl_conf["id"]] = fl_resp.id
                id_to_update["assetic_ids"][fl_conf["id"]] = fl_resp.id
            # apply friendly id if there is a field for it
            if "functional_location_id" in fl_conf and \
                    fl_conf["functional_location_id"] in row.keys():
                # row[fl_conf["functional_location_id"]] = \
                #    fl_resp.functional_location_id
                id_to_update["assetic_ids"][fl_conf[
                    "functional_location_id"]] = fl_resp.functional_location_id

        addr, geojson = self.set_assetic_spatial_attributes(row, lyr_config, fields)

        if addr or geojson:
            chk = self.assettools.set_asset_address_spatial(
                asset_repr.asset_representation.id, geojson, addr)
            if chk > 0:
                e = ("Error attempting creation of complete asset - "
                     "asset creation successful but failed during creation "
                     "of spatial data. See log.")
                self.logger.error(e)

                return Result.PARTIAL, id_to_update

        if asset_repr.error_code in [2, 4, 16]:
            # component (2), or dimension (4) or Fl (16) error
            return Result.PARTIAL, id_to_update

        return Result.SUCCESS, id_to_update

    def upload_features(self, row, complete_asset_obj, lyr_config, fields):
        # type: (dict, AssetToolsCompleteAssetRepresentation, dict, List[str]) -> bool
        """
        Uploads the address and point data against the asset defined
        in the complete_asset_obj.

        :param row: row representing a layer row
        :param complete_asset_obj: object representing asset with attached
        components, dimensions, functiona location, etc.
        :param lyr_config: customer-defined configuration found in xml file
        :param fields:
        """

        # get address details
        addr = assetic.CustomAddress()
        # get address fields the attribute fields of the feature
        for k, v in six.iteritems(
                lyr_config["addressfields"]):
            if k in addr.to_dict() and v in fields:
                setattr(addr, k, row[v])
        # get address defaults
        for k, v in six.iteritems(
                lyr_config["addressdefaults"]):
            if k in addr.to_dict():
                setattr(addr, k, v)

        geojson = None
        if "geom_geojson" in row:
            geojson = row["geom_geojson"]
        chk = self.assettools.set_asset_address_spatial(
            complete_asset_obj.asset_representation.id, geojson, addr)
        if chk > 0:
            self.messager.new_message(
                "Error Updating Asset Address/Location:{0}, Asset GUID={1}"
                "".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))
            return False

        return True

    def get_geom_wkt(self, outsrid, geometry):
        """
        Get the well known text for a geometry in 4326 projection
        :param outsrid: The projection EPSG code to export WKT as (integer)
        :param geometry: The input geometry
        :returns: wkt string of geometry in the specified projection
        """
        ...

    def get_geom_geojson(self, out_srid, geometry, centroid=None):
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
            self.logger.warning("Unable to reproject feature")
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

    def decommission_asset(self, assetid, lyr_config, comment=None):
        """
        Set the status of an asset to decommisioned
        :param assetid: The asset GUID (TODO support friendly ID)
        :param lyr_config: config details for layer
        :param comment: A comment to accompany the decommision
        :returns: 0=no error, >0 = error
        """

        return 1

    def create_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and creates functional locations defined in
        the data.

        Returns the number of successful and failed functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if self._configuration_missing():
            return

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(
            lyr, lyr.GetName(), "create")

        if lyr_config is None and fields is None:
            self.messager.new_message(
                "Unable to process functional location layer '{0}' due to "
                "missing configuration".format(lyr.name))
            # return indication that nothing was processed
            return 0, 0

        has_lyr_fl_type = 'functional_location_type' in fields

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']

        prog = ProgressTracker(self.messager)

        rows = self.get_rows_from_layer(lyr)

        for row in rows:

            if has_lyr_fl_type:
                # many fltypes in a single layer
                fltype = row[fl_corefields['functional_location_type']]
            else:
                # single fltype per layer
                fltype = fl_coredefaults['functional_location_type']

            flid = row[fl_corefields['functional_location_id']]

            if flid in ['', None]:
                # no FL ID defined. attempt to retrieve by name and type
                flrepr = self.fltools.get_functional_location_by_name_and_type(
                    row[fl_corefields['functional_location_name']]
                    , fltype)
            else:
                # FL ID defined. attempt to retrieve by ID
                # if FL doesn't exist we assume that autoid generation
                # is off which is why the ID is already set in the layer
                flrepr = self.fltools.get_functional_location_by_id(flid)

            if flrepr is not None:
                # FL already exists!
                self.messager.new_message(
                    "Functional Location {0} already exists".format(
                        flrepr.functional_location_name
                    ))
                prog.add(Result.SKIP)
                continue

            # Doesn't appear to be an existing FL so create.
            flrepr = self._create_fl_from_row(
                row, fl_corefields, fltype, attrs, def_attrs)

            if flrepr is None:
                # Error creating FL
                prog.add(Result.FAILURE)
                continue

            # update row with new information - ID, GUID, etc.
            updfields = [fl_corefields[f] for f in [
                'functional_location_id', 'id'] if f in fl_corefields]
            rev = {v: k for k, v in six.iteritems(fl_corefields)}
            for f in updfields:
                row[fields.index(f)] = (flrepr.__getattribute__(rev[f]))

            prog.add(Result.SUCCESS)

        prog.calculate()
        prog.display_functional_location_creation_summary(lyr.GetName())

        return prog.cnt_pass, prog.cnt_fail

    def update_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and updates functional locations defined in
        the data.

        Returns the number of successful and failed updates of functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if self._configuration_missing():
            return

        prog = ProgressTracker(self.messager)

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(lyr, "update")
        if lyr_config is None and fields is None:
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing configuration".format(lyr.name)
            self.messager.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return prog.cnt_pass, prog.cnt_fail

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        has_lyr_fl_type = False
        if 'functional_location_type' in fl_corefields:
            has_lyr_fl_type = True
        elif 'functional_location_type' not in fl_coredefaults:
            # need to have functional location type
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing functional location type".format(lyr.name)
            self.messager.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return prog.cnt_pass, prog.cnt_fail

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']
        all_attr_fields = attrs.keys() + def_attrs.keys()

        rows = self.get_rows_from_layer(lyr)
        for row in rows:

            if has_lyr_fl_type:
                # many fltypes in a single layer
                fltype = row[fl_corefields['functional_location_type']]
            else:
                # single fltype per layer defined in defaults
                fltype = fl_coredefaults['functional_location_type']

            flid = row[fl_corefields['functional_location_id']]

            fl_guid = None
            if "id" in fl_corefields and fl_corefields['id'] in row:
                fl_guid = row[fl_corefields['id']]

            if flid in ['', None] and fl_guid in ['', None]:
                # no FL ID defined. attempt to retrieve by name and type
                flrepr = self.fltools.get_functional_location_by_name_and_type(
                    row[fl_corefields['functional_location_name']]
                    , fltype, all_attr_fields)
            else:
                # FL ID defined. attempt to retrieve by ID
                if fl_guid:
                    flrepr = self.fltools.get_functional_location_by_id(
                        fl_guid, all_attr_fields)
                else:
                    flrepr = self.fltools.get_functional_location_by_id(
                        flid, all_attr_fields)
            if flrepr is None:
                # No FL found so move to next record
                self.messager.new_message(
                    "Unable to retrieve Functional Location {0} for "
                    "update".format(
                        row[fl_corefields['functional_location_name']]
                    ))
                prog.add(Result.FAILURE)
                continue

            # FL exists, check if the attributes are different
            # and then post if they are
            row_attrs = self._retrieve_fl_attrs_from_row(row, attrs,
                                                         def_attrs)

            if row_attrs != flrepr.attributes or \
                    flrepr.functional_location_name != row[
                fl_corefields['functional_location_name']]:
                # e.g. something has changed so update attributes with GIS
                # attributes, and name in case it changed (not allow
                # change to FL type or id)
                flrepr.attributes = row_attrs
                flrepr.functional_location_name = row[
                    fl_corefields['functional_location_name']]
                flepr = self.fltools.update_functional_location(flrepr)
                if flepr:
                    prog.add(Result.SUCCESS)
                else:
                    prog.add(Result.FAILURE)

            else:
                # indicate success, just don't attempt update
                prog.add(Result.SUCCESS)

        prog.calculate()
        prog.display_functional_location_creation_summary(lyr.GetName())

        return prog.cnt_pass, prog.cnt_fail
