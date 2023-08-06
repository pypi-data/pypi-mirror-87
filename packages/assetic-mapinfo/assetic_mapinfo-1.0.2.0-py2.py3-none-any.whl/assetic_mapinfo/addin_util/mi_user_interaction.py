try:
    import clr
    from MapInfo.Types import IMapBasicApplication, NotificationObject\
        , IMapInfoPro, NotificationType
    from System.Windows import Point
    clr.AddReference("System.Windows.Forms")
except ImportError:
    valid_mi_environment = False
else:
    valid_mi_environment = True

import threading

class UserInteraction:
    """
    Tools to interact with user in MapInfo Pro
    """
    def __init__(self, this_application_instance, imapinfopro):
        self._is_mi_environment = valid_mi_environment
        if self._is_mi_environment:
            self._pro = imapinfopro
            self.this_application_instance = this_application_instance
            self._thisApplication = IMapBasicApplication(
                this_application_instance)
            if not self._thisApplication:
                raise Exception("Incorrect Application Instance!")

    @property
    def is_mi_environment(self):
        # type: () -> bool
        """
        Is python running in a valid mapinfo environment with loaded libraries
        :return: Boolean
        """
        return self._is_mi_environment

    # def notify(self, message, title):
    #     """
    #     This will create a thread to run the 'notify' popup window in MapInfo
    #     :param message: The message to display
    #     :param title: The title of the pop-up
    #     """
    #     popup = threading.Thread(self.mi_notify(message, title))
    #     popup.start()
    #     popup.join()

    def notify(self, message, title=None):
        """
        This will create a 'notify' popup window in MapInfo
        :param message: The message to display
        :param title: The title of the pop-up
        """
        if not title:
            title = "Assetic addin"
        try:
            notify_obj = NotificationObject()
            if notify_obj:
                notify_obj.Title = title
                notify_obj.Message = message
                notify_obj.Type = NotificationType.Info
                notify_obj.TimeToShow = 10000
                notify_obj.NotificationLocation = Point(-1, -1)
                self._pro.ShowNotification(notify_obj)
        except Exception as e:
            print("Failed to execute: {}".format(e))
        """ from Enums.def
        Define Notify_None 0  
        Define Notify_Error 1  
        Define Notify_Warning 2  
        Define Notify_Info 3  
        Define Notify_Custom 4
        """