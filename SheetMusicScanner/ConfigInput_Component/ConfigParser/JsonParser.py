#!/usr/bin/env python

"""
JsonParser .....
"""

from ConfigInput_Component.IConfigParser import IConfigParser
from ConfigInput_Component.Config import Config

import json

__author__  = "Daniela Mueller"
__version__ = "0.0.0"
__status__ = "Production"


class JsonParser(IConfigParser):

    def __init__(self, pathToConfig):
        self.__pathToConfig = pathToConfig

    def parse(self):
        """
        Parst das entsprechende File und erstellt die Config.

        Parameters
        ----------

        Returns
        -------
        config : Config
        Die erstellte Config.
        """

        # load the file
        json_file = open(self.__pathToConfig)
        data = json.load(json_file)
        json_file.close()

        return Config(data)

		