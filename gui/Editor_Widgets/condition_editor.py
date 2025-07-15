from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QSpinBox,
    QListWidget, QSplitter, QPushButton, QFileDialog,
    QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt
import os
from logic.json_loader import save_json


class ConditionEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.loadedConditions = {}
        self.activeFile = None

        splitter = QSplitter()

        # 🔍 Left panel: condition list
        self.fileList = QListWidget()
        self.fileList.itemDoubleClicked.connect(self.display_condition_data)

        leftPanel = QWidget()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.fileList)

        self.addBtn = QPushButton("Add Level Condition")
        self.addBtn.clicked.connect(self.create_new_condition)
        leftLayout.addWidget(self.addBtn)

        leftPanel.setLayout(leftLayout)

        # 🧾 Right panel: scrollable form with help text
        formWidget = QWidget()
        formLayout = QVBoxLayout()

        def add_text(label):
            field = QLineEdit()
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(field)
            return field

        def add_spin(label, min_val=-1, max_val=999999):
            box = QSpinBox()
            box.setRange(min_val, max_val)
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(box)
            return box

        self.nameEdit = add_text("uniqueName (must match filename without .json)")
        self.displayNameEdit = add_text("displayName (button label for this level)")
        self.versionEdit = add_text("version (internal - do not change)")
        self.levelBox = add_spin("level (condition level number)", 1)
        self.onlineTimeBox = add_spin("onlineTimeRequiredInMinutes (minutes online or -1 to disable)")
        self.playerKillsBox = add_spin("playerKillsRequiredCount (non-headshot kills or -1 to disable)")
        self.headshotKillsBox = add_spin("headshotKillsRequiredCount (required headshot kills or -1)")
        self.distanceBox = add_spin("distanceTravelledRequiredInMeters (meters to travel or -1)")
        self.daysUntilRetakeBox = add_spin("canReTakenAfterPeriodOfDaysRealTime (days until retake or -1)")
        self.onceOnlyBox = add_spin("canTakenOnlyOnce (0 = multiple times, 1 = once)", 0, 1)
        self.animalKillsCount = add_spin("animalsKillsRequiredCount (-1 = disable, overrides animalKills)")
        self.infectedKillsCount = add_spin("infectedKillsRequiredCount (-1 = disable, overrides zombieKills)")
        self.aiKillsCount = add_spin("aiKillsRequiredCount (-1 = disable)")
        self.aiHeadshotsCount = add_spin("aiHeadShotKillsRequiredCount (-1 = disable)")

        self.saveBtn = QPushButton("Save Reward Condition")
        self.saveBtn.clicked.connect(self.save_condition_json)
        formLayout.addWidget(self.saveBtn)

        formWidget.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(formWidget)

        splitter.addWidget(leftPanel)
        splitter.addWidget(scroll)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(splitter)
        self.setLayout(mainLayout)

    def load_data(self, data, filename=None):
        if filename:
            self.loadedConditions[filename] = data
            self.fileList.addItem(filename)
        else:
            self.populate_fields(data)

    def display_condition_data(self, item):
        filename = item.text()
        self.activeFile = filename
        data = self.loadedConditions.get(filename, {})
        self.populate_fields(data)

    def populate_fields(self, data):
        self.nameEdit.setText(data.get("uniqueName", ""))
        self.displayNameEdit.setText(data.get("displayName", ""))
        self.versionEdit.setText(data.get("version", ""))
        self.levelBox.setValue(data.get("level", 1))
        self.onlineTimeBox.setValue(data.get("onlineTimeRequiredInMinutes", -1))
        self.playerKillsBox.setValue(data.get("playerKillsRequiredCount", -1))
        self.headshotKillsBox.setValue(data.get("headshotKillsRequiredCount", -1))
        self.distanceBox.setValue(data.get("distanceTravelledRequiredInMeters", -1))
        self.daysUntilRetakeBox.setValue(data.get("canReTakenAfterPeriodOfDaysRealTime", -1))
        self.onceOnlyBox.setValue(data.get("canTakenOnlyOnce", 0))
        self.animalKillsCount.setValue(data.get("animalsKillsRequiredCount", -1))
        self.infectedKillsCount.setValue(data.get("infectedKillsRequiredCount", -1))
        self.aiKillsCount.setValue(data.get("aiKillsRequiredCount", -1))
        self.aiHeadshotsCount.setValue(data.get("aiHeadShotKillsRequiredCount", -1))

    def get_data(self):
        return {
            "uniqueName": self.nameEdit.text(),
            "displayName": self.displayNameEdit.text(),
            "version": self.versionEdit.text(),
            "level": self.levelBox.value(),
            "onlineTimeRequiredInMinutes": self.onlineTimeBox.value(),
            "playerKillsRequiredCount": self.playerKillsBox.value(),
            "headshotKillsRequiredCount": self.headshotKillsBox.value(),
            "distanceTravelledRequiredInMeters": self.distanceBox.value(),
            "canReTakenAfterPeriodOfDaysRealTime": self.daysUntilRetakeBox.value(),
            "canTakenOnlyOnce": self.onceOnlyBox.value(),
            "animalsKillsRequiredCount": self.animalKillsCount.value(),
            "animalKills": {},
            "infectedKillsRequiredCount": self.infectedKillsCount.value(),
            "zombieKills": {},
            "aiKillsRequiredCount": self.aiKillsCount.value(),
            "aiHeadShotKillsRequiredCount": self.aiHeadshotsCount.value()
        }

    def save_condition_json(self):
        if not self.activeFile:
            QMessageBox.warning(self, "No File Selected", "Please select a condition file to save.")
            return
        data = self.get_data()
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            path = os.path.join(folder, self.activeFile)
            save_json(path, data)
            QMessageBox.information(self, "Saved", f"File saved:\n{path}")

    def create_new_condition(self):
        name = f"new_condition_{len(self.loadedConditions) + 1}.json"
        default_data = {
            "uniqueName": "",
            "displayName": "",
            "version": "7",
            "level": 1,
            "onlineTimeRequiredInMinutes": -1,
            "playerKillsRequiredCount": -1,
            "headshotKillsRequiredCount": -1,
            "distanceTravelledRequiredInMeters": -1,
            "canReTakenAfterPeriodOfDaysRealTime": -1,
            "canTakenOnlyOnce": 0,
            "animalsKillsRequiredCount": -1,
            "animalKills": {},
            "infectedKillsRequiredCount": -1,
            "zombieKills": {},
            "aiKillsRequiredCount": -1,
            "aiHeadShotKillsRequiredCount": -1,
            "isLoaded": 0
        }
        self.loadedConditions[name] = default_data
        self.fileList.addItem(name)
        self.activeFile = name
        self.populate_fields(default_data)
        self.fileList.setCurrentRow(self.fileList.count() - 1)
