import files
import csv

class DataReader():
    #FIELDS
    _name = None
    _path = None
    _raw = None
    _data = None
    
    #CONSTRUCTOR
    def __init__(self, name):
        self._name = name
        self.requestFilePath()
        self.getRaw()
        self.formatRaw()

    #METHODS
    def requestFilePath(self):
        self._path = files.makeFileRequester(self._name)()
        return self._path

    def getRaw(self):
        data = []
        # opening the CSV file
        with open(self._path, mode ='r', encoding='utf-8') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            head = next(csvFile)
            
            for line in csvFile:
                entry = {}

                for i in range(0, len(head)):
                    entry[head[i]] = line[i]

                data.append(entry)

        self._raw = data
        return self._raw

    #responsible for assigning a sorted array of data
    def formatRaw(self):
        pass