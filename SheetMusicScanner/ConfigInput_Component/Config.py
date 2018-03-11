#!/usr/bin/env python

"""
.....
"""


__author__  = "Daniela Mueller"
__version__ = "0.0.0"
__status__ = "Production"


class Config():

    def __init__(self, data):
        self.__data = data

    def getConfigForComponent(self, component):

        if component in self.__data.keys():
            ret = list

            # Ausgabe eines Strings
            if type(self.__data[component]) == str:
                ret = {component:self.__data[component]}

            # Ausgabe eines einfach genesteden Dictionary
            elif type(self.__data[component]) == dict:
                ret = self.__data[component]

            # Ausgabe einer zweifach genesteden List
            #elif type(self.__data[component]) == list:
               # for x in self.__data[component]:
                  #  for u, v in x.items():
                     #   ret = ret.append(u)
                      #  ret = ret.append(v)



            return ret

        else:
            return False