import files
import csv
import datetime

class DataReader():
    #FIELDS
    _name = "name"
    _path = "path"
    
    #CONSTRUCTOR
    def __init__(self, name):
        self._name = name
        self.requestFilePath()
        self.readFile()

    #METHODS
    def requestFilePath(self):
        self._path = files.makeFileRequester(self._name)()

    def readFile(self):
        data = {}
        # opening the CSV file
        with open(self._path, mode ='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            head = next(csvFile)
            for line in csvFile:
                entry = {}
                for i in range(0, len(head)):
                    entry[head[i]] = line[i]
                
                #get unix start
                start = datetime.datetime(entry["date"])

            return data
