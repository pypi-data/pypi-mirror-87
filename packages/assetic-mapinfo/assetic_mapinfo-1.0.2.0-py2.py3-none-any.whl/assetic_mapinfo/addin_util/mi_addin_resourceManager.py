try:
    # import clr
    from MapInfo.Types import IMapBasicApplication
except ImportError:
    valid_mi_environment = False
else:
    valid_mi_environment = True


class StringResourceManager:
    def __init__(self, this_application_instance):
        self._is_mi_environment = valid_mi_environment
        if self._is_mi_environment:
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

    def GetResourceString(self, index_no):
        """
        Use this to get a string value from a mapbasic config
        Requires the MapBasic custom function 'GetResString'
        This is an example of executing a MapBasic function
        :param index_no: The index number (position) of the string in the list
        :return: The string or empty string if not defined
        """
        retStr = ""
        try:
            if self._thisApplication:
                retStr = self._thisApplication.EvaluateMapBasicFunction(
                    "GetResString", [str(index_no)])
        except:
            retStr = ""
        return retStr

    def __del__(self):
        self._thisApplication = None
        pass
