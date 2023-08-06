try:
    # import clr
    from mi_common_util import CommonUtil
    from mi_addin_util import AddinUtil
    from MapInfo.Types import IAddInCustomFrame, WindowType, FrameType, InactiveLayoutContent
    from System.Text import StringBuilder
    from System.Xml import XmlWriter, XmlWriterSettings, ConformanceLevel, XmlReader
    from System.Windows.Markup import XamlDesignerSerializationManager, XamlWriterMode, XamlReader, XamlWriter
    from System.IO import TextWriter, File, StringReader, TextReader
except ImportError:
    valid_mi_environment = False
else:
    valid_mi_environment = True


class LayoutCustomFrameUtil:
    def __init__(self):
        self._is_mi_environment = valid_mi_environment

    @property
    def is_mi_environment(self):
        # type: () -> bool
        """
        Is python running in a valid mapinfo environment with loaded libraries
        :return: Boolean
        """
        return self._is_mi_environment

    @staticmethod
    def add_custom_frame_to_layout(customFrame, layoutdesigner):
        if layoutdesigner and customFrame:
            customFrameControl = layoutdesigner.AddFrameControl(customFrame, FrameType.CustomFrame)
            if customFrameControl:
                customFrame.WrapperControl = customFrameControl
                customFrameControl.SetContent(AddinUtil.create_dockable_user_control(customFrame.ControlContent))
                customFrameControl.SetInactiveContent(InactiveLayoutContent(customFrame.ControlContent))

    @staticmethod
    def windowinfo_to_layout_designer(iwindowinfo):
        if iwindowinfo and iwindowinfo.WindowType == WindowType.LayoutWindow:
            return iwindowinfo.GetDocumentControl()
        return None

    @staticmethod
    def serialize_frame(iaddin_custom_frame_instance, file_full_name):
        done = False
        try:
            done = LayoutCustomFrameUtil.__serialize_to_xml__(iaddin_custom_frame_instance, file_full_name)
        except:
            done = False
        
        return done

    @staticmethod
    def deserialize_frame(file_full_name):
        iaddin_custom_frame_instance = None
        try:
            iaddin_custom_frame_instance = LayoutCustomFrameUtil.__deserialize_from_xml(file_full_name)
        except:
            iaddin_custom_frame_instance = None

        return iaddin_custom_frame_instance

    
    @staticmethod
    def __serialize_to_xml__(iaddin_custom_frame_instance, file_full_name):
        done = False
        try:
            sb = StringBuilder()
            xml_writer_settings = XmlWriterSettings()
            xml_writer_settings.Indent = True
            xml_writer_settings.ConformanceLevel = ConformanceLevel.Fragment
            xml_writer_settings.OmitXmlDeclaration = True
            writer = None
            try:
                writer = XmlWriter.Create(sb, xml_writer_settings)
                if writer:
                    mgr = XamlDesignerSerializationManager(writer)
                    if mgr:
                        mgr.XamlWriterMode = XamlWriterMode.Expression
                        XamlWriter.Save(iaddin_custom_frame_instance, mgr)
                        filewriter = None
                        try:
                            filewriter = File.CreateText(file_full_name)
                            if filewriter:
                                filewriter.Write(sb.ToString())
                                done = True
                        finally:
                            if filewriter:
                                filewriter.Dispose()
                                filewriter = None
            finally:
                if writer:
                    writer.Dispose()
                    writer = None
        except Exception as e:
            CommonUtil.sprint("Failed to serialize: {}".format(e)) 
            done = False

        return done

    
    @staticmethod
    def __deserialize_from_xml(file_full_name):
        iaddin_custom_frame_instance = None
        try:
            filereader = None
            try:
                filereader = File.OpenText(file_full_name)
                if filereader:
                    content = filereader.ReadToEnd()
                    stringreader = StringReader(content)
                    xmlreader = None
                    try:
                        xmlreader = XmlReader.Create(stringreader)
                        if xmlreader:
                            iaddin_custom_frame_instance = XamlReader.Load(xmlreader)
                    finally:
                        if xmlreader:
                            xmlreader.Dispose()
                            xmlreader = None
            finally:
                if filereader:
                    filereader.Dispose()
                    filereader = None
        except Exception as e:
            CommonUtil.sprint("Failed to desrialize: {}".format(e)) 
            iaddin_custom_frame_instance = None

        return iaddin_custom_frame_instance
