import json
import boosted
import daylio
import copy
import array

INDENT = 4

#i dont feel great about this
#for one why am i using a class to do this when it would do better in fp
class DataManager():
    _meta = {}
    _dates = {}
    _emotions = []
    _activities = []

    def __init__(self):
        self.save()

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
                
                date = entry["start"].strftime("%Y-%m-%d")
                
                if date in self._dates:
                    self._dates[date].append(entry)
                else:
                    self._dates[date] = [entry]

            return self._dates

    def getActivities(self):
        if len(self._activities):
            return self._activities
        else:
            for date in self.getDates():
                for activity in self.getDates()[date]:
                    self._activities.append(activity)
            return self._activities
            

    def getEmotions(self):
        if len(self._emotions):
            return self._emotions
        else:
            for activity in self.getActivities():
                self._emotions.extend(activity["emotions"])
            return self._emotions

    

    def calculateHabitStability(self, habit):
        print(f"\n{habit} stability:")
        missed = 0
        for date in self.getDates():
            logged = False
            for log in self.getDates()[date]:
                if log["activity"] == habit:
                    logged = True
                    #calculate stability here?
            
            if not logged:
                missed += 1

        print(f"you missed {missed} days\n")

        

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

            json.dump(printable, f, indent=INDENT)
        
        with open("meta.json", "w") as f:
            json.dump(self.getMeta(), f, indent=INDENT)
