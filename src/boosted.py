import datareader
import csv
from  datetime import datetime

class Boosted(datareader.DataReader):    
    #CONSTRUCTOR
    def __init__(self):
        super().__init__("Boosted")

    def formatRaw(self):
            data = []

            for entry in self._raw:
                    
                # Combine the date and time fields into a single string
                start_time_str = entry['Date'] + ' ' + entry['Start time']
                end_time_str = entry['Date'] + ' ' + entry['End time']

                # Create datetime objects in the specified timezone
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %I:%M:%S %p')
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d %I:%M:%S %p')

                updated = {}
                updated["start"] = start_time
                updated["end"] = end_time
                updated["activity"] = entry["Project name"].strip()
                updated["duration"] = entry["Duration"]

                data.append(updated)
        
            sorted(data, key=lambda entry: entry["start"])
            self._data = data
            return self._data
    
    def getEntryAt(self, time):
        print("test")