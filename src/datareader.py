import files
import csv
from  datetime import datetime

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
                
                # Combine the date and time fields into a single string
                start_time_str = entry['Date'] + ' ' + entry['Start time']
                end_time_str = entry['Date'] + ' ' + entry['End time']

                # Create datetime objects in the specified timezone
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %I:%M:%S %p')
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d %I:%M:%S %p')

                # Print the resulting datetime objects
                print(start_time)
                print(end_time)

            return data
