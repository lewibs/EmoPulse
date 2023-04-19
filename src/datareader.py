import abc

class DataReader(abc.ABC):
    #FIELDS
    @property
    @abc.abstractmethod
    def path(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass
    
    #CONSTRUCTOR
    @abc.abstractmethod
    def __init__(self):
        pass

    #METHODS
    @abc.abstractmethod
    def requestFilePath(self):
        pass