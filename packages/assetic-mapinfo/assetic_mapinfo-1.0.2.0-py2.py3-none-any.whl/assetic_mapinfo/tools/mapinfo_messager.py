from assetic.tools.shared.messager_base import MessagerBase
from assetic_mapinfo import CommonUtil


class MapInfoMessager(MessagerBase):
    def __init__(self):
        super().__init__()

        self._common = CommonUtil()

    def new_message(self, msg, *args):
        try:
            self._common.sprint(msg)
        except NameError:
            # this is for development
            print(msg)
