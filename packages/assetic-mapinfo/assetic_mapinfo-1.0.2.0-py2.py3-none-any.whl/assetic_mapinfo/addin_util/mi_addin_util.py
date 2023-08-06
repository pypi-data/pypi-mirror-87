import_error = None
valid_mi_environment = True
try:
    from .mi_common_util import CommonUtil

    import clr
    clr.AddReference(r"WindowsBase")
    clr.AddReference(r"wpf\PresentationFramework")
    clr.AddReference(r"wpf\System.Windows.Presentation")

    from System import Action, Predicate, Object
    from System.AddIn.Pipeline import FrameworkElementAdapters
    from System.Windows.Markup import XamlReader
    from System.Windows import LogicalTreeHelper, PresentationSource
    from System.IO import StreamReader
    from System.Windows.Input import Key, Keyboard, TraversalRequest, FocusNavigationDirection, ApplicationCommands, KeyEventArgs
    from System.Windows.Media.Imaging import BitmapImage, BitmapCacheOption, BitmapCreateOptions
    from System.Collections.Generic import KeyValuePair, List

    from MapInfo.Types import IMapInfoPro, CommandAdapters, MapInfoRibbonToolTip, NativeHandleContractInsulator
    from MapInfo.AddIns.Common import DelegateCommand
except ImportError as ex:
    valid_mi_environment = False
    import_error = ex


class AddinUtil:
    def __init__(self):
        self._is_mi_environment = valid_mi_environment
        self._import_error = import_error

    @property
    def is_mi_environment(self):
        # type: () -> bool
        """
        Is python running in a valid mapinfo environment with loaded libraries
        :return: Boolean
        """
        return self._is_mi_environment

    @property
    def import_error_msg(self):
        # type: () -> string
        """
        What was the import error?
        :return: string
        """
        return self._import_error

    @staticmethod
    def image_path_to_bitmap(fname):
        try:
            if fname:
                bitmap = BitmapImage()
                bitmap.BeginInit()
                bitmap.UriSource = CommonUtil.path_to_uri(fname)
                bitmap.CacheOption = BitmapCacheOption.OnLoad
                bitmap.CreateOptions = BitmapCreateOptions.DelayCreation
                bitmap.EndInit()
                bitmap.Freeze()
                return bitmap
        except:
            pass

    @staticmethod
    def create_tooltip(tooltip_description, tooltip_text, tooltip_disabled_text):
        toolTip = MapInfoRibbonToolTip()
        toolTip.ToolTipDescription = tooltip_description
        toolTip.ToolTipText = tooltip_text
        toolTip.ToolTipDisabledText = tooltip_disabled_text
        return toolTip
    
    @staticmethod
    def create_user_control(filename):
        userControl = None
        try:
            s = None
            if filename:
                s = StreamReader(filename)
                userControl = XamlReader.Load(s.BaseStream)
        except Exception as e:
            CommonUtil.sprint("Failed to Create UserControl: {}".format(e))
        finally:
            if s:
                s.Close()
                s.Dispose()
        return userControl
    
    @staticmethod
    def get_dockable_user_control_properties(d):
        propList = None
        try:
            if d:
                propList = List[KeyValuePair[str, str]]()
                for _, value in enumerate(d):
                    pair = KeyValuePair[str, str](value,d[value])
                    propList.Add(pair)
        except Exception as e:
            CommonUtil.sprint("Failed to Create Properties: {}".format(e))
        return propList

    @staticmethod
    def create_dockable_user_control(user_control):
        if user_control:
            uc = NativeHandleContractInsulator(FrameworkElementAdapters.ViewToContractAdapter(user_control))
            uc.Name = user_control.Name
            return uc
        else:
            return None

    @staticmethod
    def create_command(execute_callback, can_execute_callback = None):
        if execute_callback and can_execute_callback:
            return CommandAdapters.ViewToContractAdapter(DelegateCommand(Action[Object](execute_callback), Predicate[Object](can_execute_callback)))
        else:
            return CommandAdapters.ViewToContractAdapter(DelegateCommand(Action[Object](execute_callback)))
    
    @staticmethod
    def find_logical_control(parent, name):
        for child in LogicalTreeHelper.GetChildren(parent) :
            if child.Name == name:
                return child
        return AddinUtil.find_logical_control(child, name)

    @staticmethod
    def handle_default_keypress(user_control, key):
        handled = False
        target = Keyboard.FocusedElement
        if not target:
            if key == Key.Tab:
                user_control.MoveFocus(TraversalRequest(FocusNavigationDirection.First))
                if Keyboard.FocusedElement:
                    handled = True
            return handled
        
        handled = True

        if key == Key.X and (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl)):
            ApplicationCommands.Cut.Execute(None, target)
        elif key == Key.C and (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl)):
            ApplicationCommands.Copy.Execute(None, target)
        elif key == Key.V and (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl)):
            ApplicationCommands.Paste.Execute(None, target)
        elif key == Key.U and (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl)):
            ApplicationCommands.Undo.Execute(None, target)
        elif key == Key.R and (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl)):
            ApplicationCommands.Redo.Execute(None, target)
        elif ((key == Key.Left) and (key == Key.Right) and (key == Key.Up) and (key == Key.Down) and (key== Key.Home) and (key == Key.End) and (key == Key.Home)):
            try:
                visual = PresentationSource.FromVisual(target)
                if visual:
                    arg = KeyEventArgs(Keyboard.PrimaryDevice, visual, 0, key)
                    if arg:
                        arg.RoutedEvent = Keyboard.KeyDownEvent
                        target.RaiseEvent(arg)
            except:
                pass
        elif key == Key.Tab:
            try:
                request = None
                if Keyboard.IsKeyDown(Key.LeftShift) or Keyboard.IsKeyDown(Key.RightShift):
                    request = TraversalRequest(FocusNavigationDirection.Previous)
                else:
                    request = TraversalRequest(FocusNavigationDirection.Next)
                if Keyboard.FocusedElement:
                    Keyboard.FocusedElement.MoveFocus(request)
            except:
                pass
        else:
            handled = False
        
        return handled

