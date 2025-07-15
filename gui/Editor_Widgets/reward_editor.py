from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QSpinBox,
    QListWidget, QPushButton, QFileDialog, QSplitter,
    QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt
import os
from logic.json_loader import load_json, save_json


class RewardEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.loadedRewards = {}
        self.activeFile = None

        splitter = QSplitter()

        # 🔍 Left panel: reward level list
        self.fileList = QListWidget()
        self.fileList.itemDoubleClicked.connect(self.display_reward_data)

        leftPanel = QWidget()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.fileList)

        self.addBtn = QPushButton("Add Reward Level")
        self.addBtn.clicked.connect(self.create_new_reward)
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

        def add_spin(label, min_val=0, max_val=9999):
            box = QSpinBox()
            box.setRange(min_val, max_val)
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(box)
            return box

        self.nameEdit = add_text("uniqueName (must match filename without .json)")
        self.versionEdit = add_text("version (internal - do not modify)")
        self.isLoadedBox = add_spin("isLoaded (used internally - always 0)", 0, 1)
        self.levelBox = add_spin("level (reward level index)", 1, 999)
        self.canTakenTimesBox = add_spin("canTakenTimes (-1 = unlimited, >0 = max claim times)", -1, 9999)

        self.itemList = QListWidget()
        formLayout.addWidget(QLabel("uniqueItemNames (list of item uniqueNames)"))
        formLayout.addWidget(self.itemList)

        self.addItemBtn = QPushButton("Add Item Name")
        self.addItemBtn.clicked.connect(self.add_item_name)
        formLayout.addWidget(self.addItemBtn)

        self.saveBtn = QPushButton("Save Reward Level")
        self.saveBtn.clicked.connect(self.save_reward_json)
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

    def add_item_name(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Item JSON", "", "JSON Files (*.json)")
        if path:
            data = load_json(path)
            name = data.get("uniqueName", os.path.basename(path).replace(".json", ""))
            if name:
                existing = [self.itemList.item(i).text() for i in range(self.itemList.count())]
                if name not in existing:
                    self.itemList.addItem(name)

    def load_data(self, data, filename=None):
        if filename:
            self.loadedRewards[filename] = data
            self.fileList.addItem(filename)
        else:
            self.populate_fields(data)

    def display_reward_data(self, item):
        filename = item.text()
        self.activeFile = filename
        data = self.loadedRewards.get(filename, {})
        self.populate_fields(data)

    def populate_fields(self, data):
        self.nameEdit.setText(data.get("uniqueName", ""))
        self.versionEdit.setText(data.get("version", ""))
        self.isLoadedBox.setValue(data.get("isLoaded", 0))
        self.levelBox.setValue(data.get("level", 1))
        self.canTakenTimesBox.setValue(data.get("canTakenTimes", -1))
        self.itemList.clear()
        for name in data.get("uniqueItemNames", []):
            self.itemList.addItem(name)

    def get_data(self):
        return {
            "uniqueName": self.nameEdit.text(),
            "version": self.versionEdit.text(),
            "isLoaded": self.isLoadedBox.value(),
            "level": self.levelBox.value(),
            "canTakenTimes": self.canTakenTimesBox.value(),
            "uniqueItemNames": [self.itemList.item(i).text() for i in range(self.itemList.count())],
            "items": []
        }

    def save_reward_json(self):
        if not self.activeFile:
            QMessageBox.warning(self, "No File Selected", "Please select a reward file to save.")
            return
        data = self.get_data()
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            path = os.path.join(folder, self.activeFile)
            save_json(path, data)
            QMessageBox.information(self, "Saved", f"File saved:\n{path}")

    def create_new_reward(self):
        name = f"new_reward_{len(self.loadedRewards) + 1}.json"
        default_data = {
            "uniqueName": "",
            "version": "7",
            "isLoaded": 0,
            "level": 1,
            "canTakenTimes": -1,
            "uniqueItemNames": [],
            "items": []
        }
        self.loadedRewards[name] = default_data
        self.fileList.addItem(name)
        self.activeFile = name
        self.populate_fields(default_data)
        self.fileList.setCurrentRow(self.fileList.count() - 1)
