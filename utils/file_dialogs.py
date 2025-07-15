# utils/file_dialogs.py

from PyQt5.QtWidgets import QFileDialog
import os

def open_json_file(parent=None):
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "Select JSON File",
        "",
        "JSON Files (*.json)"
    )
    return path if path else None

def open_multiple_json_files(parent=None):
    paths, _ = QFileDialog.getOpenFileNames(
        parent,
        "Select JSON Files",
        "",
        "JSON Files (*.json)"
    )
    return paths if paths else []

def select_folder(parent=None):
    return QFileDialog.getExistingDirectory(parent, "Select Folder")

def get_all_json_files(folder):
    json_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files
