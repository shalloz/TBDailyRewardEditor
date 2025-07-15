# logic/data_models.py

class Reward:
    def __init__(self, uniqueName="", level=1, uniqueItemNames=None):
        self.uniqueName = uniqueName
        self.isLoaded = 0
        self.version = "1"
        self.level = level
        self.canTakenTimes = -1
        self.items = []  # Placeholder for future item object support
        self.uniqueItemNames = uniqueItemNames if uniqueItemNames else []

    def to_dict(self):
        return {
            "uniqueName": self.uniqueName,
            "isLoaded": self.isLoaded,
            "version": self.version,
            "level": self.level,
            "canTakenTimes": self.canTakenTimes,
            "items": self.items,
            "uniqueItemNames": self.uniqueItemNames
        }

    @staticmethod
    def from_dict(data):
        return Reward(
            uniqueName=data.get("uniqueName", ""),
            level=data.get("level", 1),
            uniqueItemNames=data.get("uniqueItemNames", [])
        )


class Condition:
    def __init__(self, level=1, onlineTimeRequiredInMinutes=0):
        self.level = level
        self.onlineTimeRequiredInMinutes = onlineTimeRequiredInMinutes
        self.version = "7"
        self.displayName = f"#Level {level}"
        self.canTakenOnlyOnce = 0

    def to_dict(self):
        return {
            "uniqueName": f"Default_Level_Condition_{self.level}",
            "level": self.level,
            "onlineTimeRequiredInMinutes": self.onlineTimeRequiredInMinutes,
            "playerKillsRequiredCount": -1,
            "headshotKillsRequiredCount": -1,
            "distanceTravelledRequiredInMeters": -1,
            "canReTakenAfterPeriodOfDaysRealTime": -1,
            "canTakenOnlyOnce": self.canTakenOnlyOnce,
            "animalsKillsRequiredCount": -1,
            "animalKills": {},
            "infectedKillsRequiredCount": -1,
            "zombieKills": {},
            "aiKillsRequiredCount": -1,
            "aiHeadShotKillsRequiredCount": -1,
            "version": self.version,
            "displayName": self.displayName
        }

    @staticmethod
    def from_dict(data):
        return Condition(
            level=data.get("level", 1),
            onlineTimeRequiredInMinutes=data.get("onlineTimeRequiredInMinutes", 0)
        )


class Item:
    def __init__(self, uniqueName="", type_="", quantity=1.0, health=100.0):
        self.uniqueName = uniqueName
        self.type = type_
        self.quantity = quantity
        self.health = health
        self.attachmentUniqueNames = []
        self.isCar = 0

    def to_dict(self):
        return {
            "uniqueName": self.uniqueName,
            "type": self.type,
            "quantity": self.quantity,
            "health": self.health,
            "attachmentUniqueNames": self.attachmentUniqueNames,
            "isCar": self.isCar
        }

    @staticmethod
    def from_dict(data):
        return Item(
            uniqueName=data.get("uniqueName", ""),
            type_=data.get("type", ""),
            quantity=data.get("quantity", 1.0),
            health=data.get("health", 100.0)
        )
