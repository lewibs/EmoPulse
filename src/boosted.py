import files
import datareader

class Boosted(datareader.DataReader):
    #FIELDS
    @property
    def path(self, path):
        self._path = path

    @property
    def name(self, name):
        self._name = name
    
    #CONSTRUCTOR
    def __init__(self):
        self._name = "Boosted"
        self.requestFilePath()

    #METHODS
    def requestFilePath(self):
        self.path = files.makeFileRequester(self.name)()