from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton,
    QHBoxLayout, QStatusBar
)
from gui.Editor_Widgets.reward_editor import RewardEditor
from gui.Editor_Widgets.condition_editor import ConditionEditor
from gui.Editor_Widgets.item_browser import ItemBrowser
from utils.file_dialogs import (
    open_json_file, select_folder, get_all_json_files
)
from logic.json_loader import load_json, save_json
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DayZ Reward JSON Editor")
        self.setMinimumSize(800, 600)
        self.currentFilePath = None

        self.tabWidget = QTabWidget()
        self.rewardEditor = RewardEditor()
        self.conditionEditor = ConditionEditor()
        self.itemBrowser = ItemBrowser()

        self.tabWidget.addTab(self.rewardEditor, "Reward Levels")
        self.tabWidget.addTab(self.conditionEditor, "Level Conditions")
        self.tabWidget.addTab(self.itemBrowser, "Items")

        # 👇 Only one top button now — “Load Folder”
        loadFolderBtn = QPushButton("Load Folder")
        loadFolderBtn.clicked.connect(self.load_folder)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(loadFolderBtn)

        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.tabWidget)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def save_file(self):
        # Optional — can be triggered from inside any widget later
        if self.currentFilePath:
            currentTab = self.tabWidget.currentWidget()
            data = currentTab.get_data()
            save_json(self.currentFilePath, data)
            self.statusBar.showMessage("File saved!", 3000)

    def load_folder(self):
        root = select_folder(self)
        if root:
            folders = {
                "RewardLevels": self.rewardEditor,
                "LevelConditions": self.conditionEditor,
                "Items": self.itemBrowser
            }

            success = {"RewardLevels": 0, "LevelConditions": 0, "Items": 0}
            error_count = 0

            for folder_name, editor in folders.items():
                subfolder_path = os.path.join(root, folder_name)
                if not os.path.isdir(subfolder_path):
                    print(f"[Warning] Missing folder: {folder_name}")
                    continue

                json_files = get_all_json_files(subfolder_path)
                for path in json_files:
                    try:
                        data = load_json(path)
                        filename = os.path.basename(path)
                        editor.load_data(data, filename=filename)
                        success[folder_name] += 1
                    except Exception as e:
                        print(f"[Error] Failed to load: {path}")
                        print(f"        → {type(e).__name__}: {e}")
                        error_count += 1

            self.itemBrowser.finalize_load()

            msg = (
                f"Loaded {success['RewardLevels']} rewards, "
                f"{success['LevelConditions']} conditions, "
                f"{success['Items']} items — {error_count} error(s)"
            )
            self.statusBar.showMessage(msg, 6000)
            print(msg)
