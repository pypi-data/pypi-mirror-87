import os
import assetic_mapinfo

appdata = os.environ.get("APPDATA")
inifile = os.path.abspath(appdata + "\\Assetic\\assetic.ini")
xmlfile = os.path.abspath(
            appdata + "\\Assetic\\mapinfo_edit_config.xml")
logfile = None

tmp_table_file = os.path.abspath(appdata +
                                 "\\Assetic\\mapinfo_tmp\\tmp_selection.TAB")

assetic_mapinfo.Initialise(xmlfile, inifile, logfile, "DEBUG")

logger = assetic_mapinfo.config.asseticsdk.logger

tools = assetic_mapinfo.MapInfoLayerTools()

user_interaction = assetic_mapinfo.UserInteraction(None, None)
print(user_interaction.is_mi_environment)
#processed_ids = tools.create_asset(tmp_table_file
#                                   , "list_transport_segments_hobart")
#print(processed_ids)
tools.display_asset(tmp_table_file, "list_transport_segments_hobart")
