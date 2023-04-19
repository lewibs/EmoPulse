import files
import csv

class DataReader():
    #FIELDS
    _name = "name"
    _path = "path"
    
    #CONSTRUCTOR
    def __init__(self, name):
        self._name = name
        self.requestFilePath()

    #METHODS
    def requestFilePath(self):
        self._path = files.makeFileRequester(self._name)()

    def readFile(self):
        # opening the CSV file
        # with open('Giants.csv', mode ='r')as file:
        
        # # reading the CSV file
        # csvFile = csv.reader(file)
        
        # # displaying the contents of the CSV file
        # for lines in csvFile:
        #         print(lines)
