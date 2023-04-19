import abc
import files

class DataReader(abc.ABC):
    #FIELDS
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    @abc.abstractmethod
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    #CONSTRUCTOR
    @abc.abstractmethod
    def __init__(self):
        #do this
        #self.name = "name of thing"
        #self.requestFilePath()
        pass

    #METHODS
    def requestFilePath(self):
        self.path = files.makeFileRequester(self.name)()