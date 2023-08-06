"""
field_calculations.py
custom methods that apply calculations for the given inputs
"""
import logging

from assetic.tools.shared import CalculationTools


class FieldCalculations(CalculationTools):
    def __init__(self):
        super(CalculationTools, self).__init__()
        self.logger = logging.getLogger(__name__)

    def get_road_id(self, row, input_fields, layer_name):
        """
        Return a string that has prefixed the given field
        :param row: The data row from the GIS dictionary
        :param input_fields: The fields the static method needs
        :param layer_name: The name of the layer being processed
        """
        if len(input_fields) > 0 and input_fields[0] in row:
            return "RD{0}".format(row[input_fields[0]])
        else:
            raise ValueError("Missing expected dictionary for get_road_id")

    def get_road_name(self, row, input_fields, layer_name):
        """
        Return a string that has prefixed the given field
        :param row: The data row from the GIS dictionary
        :param input_fields: The fields the static method needs
        :param layer_name: The name of the layer being processed
        """
        if len(input_fields) > 2 and input_fields[0] in row and \
                input_fields[1] in row and input_fields[2] in row:
            return "{0} - {1} to {2}".format(
                row[input_fields[0]], row[input_fields[1]]
                , row[input_fields[2]])
        else:
            raise ValueError("Missing expected dictionary for get_road_name")
