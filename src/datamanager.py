import json
import boosted
import daylio
import copy

class DataManager():
    _data = []

    def __init__(self):
        boostedManager = boosted.Boosted()
        daylioManager = daylio.Daylio()

        #combine data
        self._data = {}
        for entry in boostedManager._data:
            entry["emotions"] = []

            for emotion in daylioManager._data:
                if entry["start"] <= emotion["date"] and entry["end"] >= emotion["date"]:
                    entry["emotions"].append(emotion)
            
            date = entry["start"].strftime("%Y-%m-%d")
            
            if date in self._data:
                self._data[date].append(entry)
            else:
                self._data[date] = [entry]

    def writeData(self, filename):
        with open(f'{filename}.json', "w") as f:
            printable = copy.deepcopy(self._data)

            lostEntries = 0
            lostEmotions = 0
            lostDates = 0
            for date in printable:
                try:
                    for entry in printable[date]:
                        try:
                            entry["start"] = entry["start"].strftime("%Y-%m-%d %H:%M:%S")
                            entry["end"] = entry["end"].strftime("%Y-%m-%d %H:%M:%S")

                            for emotion in entry["emotions"]:
                                try:
                                    emotion["date"] = emotion["date"].strftime("%Y-%m-%d %H:%M:%S")
                                except:
                                    lostEmotions += 1
                        except:
                            lostEntries += 1
                except:
                    lostDates += 1
            
            print("\nI may have had some issues converting data")
            print(f"dates lost: {lostDates}")
            print(f"entries lost: {lostEntries}")
            print(f"emotions lost: {lostEmotions}\n")

            json.dump(printable, f, indent=4)
