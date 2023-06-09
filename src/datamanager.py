import json
import boosted
import daylio
import copy
import numpy
import unixFrom
import dateStringFrom

INDENT = 4
NOTKNOWN = "unknown"

class DataManager():
    _meta = {}
    _dates = {}
    _emotions = []
    _activities = []

    def __init__(self):
        self.save()

        for activity in self.getActivityTypes():
            self.generateReportForActivity(activity)

        for emotionType in self.getEmotionTypes():
            self.generateReportForEmotion(emotionType)

    def generateReportForEmotion(self, emotion):
        emotions = self.getEmotions()
        currentEmotions = self.filterForEmotion(emotion)
        emotionValue = currentEmotions[0]["mood_value"]

        print(f"\n{emotionValue}: {emotion}")
        print(f"entries: {len(currentEmotions)}")
        print(f"frequency: {((len(currentEmotions) / len(emotions)) * 100):.4}%")

        print("\nThe top environment items for this emotion are:")
        triggers = self.getEnvsForEmotion(emotion)
        for trigger in triggers[:5]:
            print(f"{trigger[0]} occurs {trigger[1]:.4}% of the time")
        print("")

        print("\nThe top trigger items for this emotion are:")
        triggers = self.getEnvsForEmotion(emotion)
        for trigger in triggers[:5]:
            print(f"{trigger[0]} occurs {trigger[1]:.4}% of the time")
        print("")

    def getEntryTriggersForEmotion(self, search):
        def sortByDate(entry): 
            return entry["date"]
        
        emotions = self.getEmotions()
        sorted(emotions, key=sortByDate)

        data = {}
        last = None
        for emotion in emotions:
            if last is not None:
                if emotion["mood"] == search and last["mood"] != search:
                    for trigger in emotion["env"]:
                        if trigger == '':
                            trigger = NOTKNOWN
                        
                        if trigger in data:
                            data[trigger] += 1
                        else:
                            data[trigger] = 1

            last = emotion

        sum = 0
        for key in data:
            sum += data[key]

        for key in data:
            data[key] = (data[key] / sum) * 100

        res = []
        for key in data:
            res.append([key, data[key]])

        def sort(val):
            return val[1]
        sorted(res, key=sort)
        return res

    # def getExitTriggersForEmotion(self, search):

    def getEnvsForEmotion(self, search):
        data = {}
        emotions = self.filterForEmotion(search)
    
        for emotion in emotions:
            for trigger in emotion["env"]:
                if trigger == '':
                    trigger = NOTKNOWN

                if trigger in data:
                    data[trigger] += 1 
                else:
                    data[trigger] = 1

        sum = 0
        for key in data:
            sum += data[key]

        for key in data:
            data[key] = (data[key] / sum) * 100
        
        res = []
        for key in data:
            res.append([key, data[key]])

        def secondInArr(x):
            return x[1]
        
        sorted(res, key=secondInArr)
        return res


    def generateReportForActivity(self, activity):
        print(f"\n{activity}:")

        print(f"Average duration: {dateStringFrom.unixDelta(self.calculateAverageActivityDuration(activity))}")
        print(f"Average time per day: {dateStringFrom.unixDelta(self.calculateAverageActivityTimePerDay(activity))}\n")

        edges = self.calculateAverageEdgeTimes(activity)
        def standardXtime(type):
            time = dateStringFrom.unixDelta(edges[type]["average"])
            std = dateStringFrom.unixDelta(edges[type]["std"])
            print(f"Standard activity {type} time: {time} ± {std}")

        standardXtime("start")
        standardXtime("mid")
        standardXtime("end")
        print("")

        print("")

    def getMeta(self):
        if len(self._meta):
            return self._meta
        else:
            dates = set()
            date_entries = 0
            activities = set()
            activity_entries = 0
            emotion_moods = set()
            emotion_envs = set()
            emotion_entries = 0

            for date in self.getDates():
                dates.add(date)
                date_entries += 1

            for activity in self.getActivities():
                activity_entries += 1
                activities.add(activity["activity"])

            for emotion in self.getEmotions():
                emotion_entries += 1

                for env in emotion['env']:
                    emotion_envs.add(env)

                emotion_moods.add(emotion["mood"])

            self._meta["dates"] = list(dates)
            self._meta["date_entries"] = date_entries
            self._meta["activities"] = list(activities)
            self._meta["activity_entries"] = activity_entries
            self._meta["emotion_moods"] = list(emotion_moods)
            self._meta["emotion_envs"] = list(emotion_envs)
            self._meta["emotion_entries"] = emotion_entries
            return self._meta

    def getDates(self):
        if len(self._dates):
            return self._dates
        else:
            boostedManager = boosted.Boosted()
            daylioManager = daylio.Daylio()

            for entry in boostedManager._data:
                entry["emotions"] = []

                for emotion in daylioManager._data:
                    if entry["start"] <= emotion["date"] and entry["end"] >= emotion["date"]:
                        entry["emotions"].append(emotion)
                
                date = unixFrom.roundToDay(entry["start"])
                
                if date in self._dates:
                    self._dates[date].append(entry)
                else:
                    self._dates[date] = [entry]

            return self._dates

    def getActivityTypes(self):
        return self.getMeta()["activities"]

    def getActivities(self):
        if len(self._activities):
            return self._activities
        else:
            for date in self.getDates():
                for activity in self.getDates()[date]:
                    self._activities.append(activity)

            sorted(self._activities, key=lambda entry: entry["start"])

            # now we want to clean up the data when it rolls over
            # midnight and make those one activity
            activities = []
            last = self._activities[0]
            for activity in self._activities[1:]:
                if last["activity"] == activity["activity"]: 
                    last["end"] = activity["end"]
                    last["duration"] += activity["duration"]
                else:
                    last = activity
                    activities.append(last)
            
            self._activities = activities
            return self._activities
    
    def getEmotions(self):
        if len(self._emotions):
            return self._emotions
        else:
            for activity in self.getActivities():
                self._emotions.extend(activity["emotions"])
            return self._emotions
    
    def getEmotionTypes(self):
        return self.getMeta()["emotion_moods"]
    
    def filterForEmotion(self, search):
        emotions = []
        for emotion in self.getEmotions():
            if emotion["mood"] == search:
                emotions.append(emotion)
        return emotions

    def getDateCounts(self):
        return self.getMeta()["date_entries"]

    def countActivities(self, search, minDuration=0):
        total = 0
        for activity in self.getActivities():
            if activity["activity"] == search:
                d = activity["duration"]
                if d > minDuration:
                    total += 1

        return total

    def calculateTotalActivityDuration(self, search, minDuration=0):
        duration = 0

        for activity in self.getActivities():
            if activity["activity"] == search:
                d = activity["duration"]
                
                if d > minDuration:
                    duration += d


        return duration

    def calculateAverageActivityDuration(self, search, minDuration=0): 
        #2O(n) but whatever the code is more readable and less repeated
        return self.calculateTotalActivityDuration(search, minDuration)/self.countActivities(search, minDuration)

    def calculateAverageActivityTimePerDay(self, search, minDuration=0):
        return self.calculateTotalActivityDuration(search, minDuration) / self.getDateCounts()

    def getEdgeTimes(self, search, minDuration=0):
        edges = []
        for activity in self.getActivities():
            if activity["activity"] == search:
                d = activity["duration"]
                if d > minDuration:
                    edges.append({
                        "start": activity["start"],
                        "end": activity["end"],
                        "mid": (activity["end"] - activity["start"])

                    })

        return edges
    
    # this needs to be reworked the std is really funky because of the rollover issue at midnight
    def calculateAverageEdgeTimes(self, search, minDuration=0):
        edges = self.getEdgeTimes(search, minDuration)
        start = [unixFrom.stampInDay(edge["start"]) for edge in edges]
        mid = [unixFrom.stampInDay(edge["mid"]) for edge in edges]
        end = [unixFrom.stampInDay(edge["end"]) for edge in edges]

        edges = {
            "start": {
                "average": numpy.mean(start),
                "std": numpy.std(start)
            },
            "end": {
                "average": numpy.mean(end),
                "std": numpy.std(end)
            },
            "mid": {
                "average": numpy.mean(mid),
                "std": numpy.std(mid)
            }
        }

        return edges


    def save(self):
        with open('data.json', "w") as f:
            printable = copy.deepcopy(self.getDates())

            lostEntries = 0
            lostEmotions = 0
            lostDates = 0
            for date in printable:
                try:
                    for entry in printable[date]:
                        try:
                            entry["start"] = dateStringFrom.unix(entry["start"])
                            entry["end"] = dateStringFrom.unix(entry["end"])
                            entry["duration"] = dateStringFrom.unixDelta(entry["duration"])

                            for emotion in entry["emotions"]:
                                try:
                                    emotion["date"] = dateStringFrom.unix(emotion["date"])
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

            json.dump(printable, f, indent=INDENT)
        
        with open("meta.json", "w") as f:
            printable = copy.deepcopy(self.getMeta())
            printable["dates"] = [dateStringFrom.unixDay(date) for date in printable["dates"]]

            json.dump(printable, f, indent=INDENT)
