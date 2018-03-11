__author__  = "Christian Dufter"
__version__ = "0.0.1"
__status__ = "Ready"

class TSingleton(type):
    """
    TSingleton ist ein "Template" zur Realisierung von Singletonklassen und verhindert mehrmalige instanziierung einer Klasse.
    Klassen die ein Singleton sein sollen, müssen diese als metaclass angeben

    :Attributes:
        _instances      Protected member, in welcher die Instanz gespeichert wird.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Wenn die eigentliche Singletonklasse aufgerufen wird, biegt diese Funktion den Aufruf auf die gespeicherte Instanz um.
        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:

            cls._instances[cls] = super(TSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
		
		