import datareader
import datetime
import unixFrom

class Daylio(datareader.DataReader):    
    #CONSTRUCTOR
    def __init__(self):
        super().__init__("Daylio")

    def formatRaw(self):
        data = []
        moods = {}

        print("\nWe need to collect the numerical values for what certain emotions mean please try to enter them below:")
        for entry in self._raw:
            updated = {}

            if entry["mood"] not in moods: #check for none rather then not because user might input 0
                value = input(f'Enter value (number) for {entry["mood"]}: ')
                moods[entry["mood"]] = int(value)
            
            full_date_str = entry["\ufefffull_date"]
            time_str = entry["time"]

            # Combine the "full_date" and "time" strings into a single string
            datetime_str = full_date_str + " " + time_str

            # Convert the combined string into a datetime object
            full_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
            full_datetime = unixFrom.datetime(full_datetime)
            
            updated["mood"] = entry["mood"]
            updated["mood_value"] = moods[entry["mood"]]
            updated["weekday"] = entry["weekday"]
            updated["env"] = entry["activities"].split(" | ")
            updated["note"] = entry["note"]
            updated["date"] = full_datetime
            
            data.append(updated)
        print("")

        sorted(data, key=lambda entry: entry["date"])
        self._data = data
        return self._data