from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit,
    QListWidget, QSplitter, QPushButton, QFileDialog, QMessageBox,
    QScrollArea, QDoubleSpinBox, QSpinBox
)
from PyQt5.QtCore import Qt
import os
from logic.json_loader import save_json, load_json


class ItemBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.loadedItems = {}
        self.filteredItems = {}
        self.activeFile = None

        splitter = QSplitter()

        # 🔍 Left side widget with search + list
        leftWidget = QWidget()
        leftLayout = QVBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search items...")
        self.searchBar.textChanged.connect(self.filter_items)
        leftLayout.addWidget(self.searchBar)

        self.fileList = QListWidget()
        self.fileList.itemDoubleClicked.connect(self.display_item_data)
        leftLayout.addWidget(self.fileList)

        self.addItemBtn = QPushButton("Add New Item")
        self.addItemBtn.clicked.connect(self.create_new_item)
        leftLayout.addWidget(self.addItemBtn)

        leftWidget.setLayout(leftLayout)

        # 🧾 Right side form layout with helpful labels
        formWidget = QWidget()
        formLayout = QVBoxLayout()

        def add_text(label):
            field = QLineEdit()
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(field)
            return field

        def add_spin(label, min_val=0, max_val=1):
            box = QSpinBox()
            box.setRange(min_val, max_val)
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(box)
            return box

        def add_float(label, min_val=0.0, max_val=999999.0, max_override=None):
            box = QDoubleSpinBox()
            box.setRange(min_val, max_val)
            if max_override is not None:
                box.setMaximum(max_override)
            box.setDecimals(2)
            box.setSingleStep(0.1)
            formLayout.addWidget(QLabel(label))
            formLayout.addWidget(box)
            return box

        self.nameEdit = add_text("uniqueName (must match filename)")
        self.typeEdit = add_text("type (from types.xml)")
        self.healthEdit = add_float("health (percent, 100 = full)")
        self.quantityEdit = add_float("quantity (max 1.0, 1.0 = full)", max_override=1.0)
        self.attachmentsEdit = add_text("attachmentUniqueNames (comma-separated names)")
        self.addAttachmentBtn = QPushButton("Add Attachment")
        self.addAttachmentBtn.clicked.connect(self.add_attachment)
        formLayout.addWidget(self.addAttachmentBtn)

        self.isCarBox = add_spin("isCar (0 = no, 1 = yes)", 0, 1)

        self.saveBtn = QPushButton("Save Item")
        self.saveBtn.clicked.connect(self.save_item_json)
        formLayout.addWidget(self.saveBtn)

        formWidget.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(formWidget)

        splitter.addWidget(leftWidget)
        splitter.addWidget(scroll)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(splitter)
        self.setLayout(mainLayout)

    def load_data(self, data, filename=None):
        if filename:
            self.loadedItems[filename] = data
        else:
            self.populate_fields(data)

    def finalize_load(self):
        self.filteredItems = dict(self.loadedItems)
        self.update_file_list()

    def update_file_list(self):
        self.fileList.clear()
        for filename in self.filteredItems:
            self.fileList.addItem(filename)

    def filter_items(self, text):
        text = text.lower()
        self.filteredItems = {
            fname: data
            for fname, data in self.loadedItems.items()
            if text in fname.lower() or text in data.get("uniqueName", "").lower()
        }
        self.update_file_list()

    def display_item_data(self, item):
        filename = item.text()
        self.activeFile = filename
        data = self.loadedItems.get(filename, {})
        self.populate_fields(data)

    def populate_fields(self, data):
        self.nameEdit.setText(data.get("uniqueName", ""))
        self.typeEdit.setText(data.get("type", ""))
        self.healthEdit.setValue(data.get("health", 100.0))
        self.quantityEdit.setValue(min(data.get("quantity", 1.0), 1.0))
        self.attachmentsEdit.setText(", ".join(data.get("attachmentUniqueNames", [])))
        self.isCarBox.setValue(data.get("isCar", 0))

    def get_data(self):
        return {
            "uniqueName": self.nameEdit.text(),
            "type": self.typeEdit.text(),
            "health": self.healthEdit.value(),
            "quantity": min(self.quantityEdit.value(), 1.0),
            "attachmentUniqueNames": [
                name.strip() for name in self.attachmentsEdit.text().split(",") if name.strip()
            ],
            "isCar": self.isCarBox.value()
        }

    def save_item_json(self):
        if not self.activeFile:
            QMessageBox.warning(self, "No File Selected", "Please select an item file to save.")
            return
        data = self.get_data()
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            path = os.path.join(folder, self.activeFile)
            save_json(path, data)
            QMessageBox.information(self, "Saved", f"Item saved:\n{path}")

    def create_new_item(self):
        name = f"new_item_{len(self.loadedItems) + 1}.json"
        default_data = {
            "uniqueName": "",
            "type": "",
            "health": 100.0,
            "quantity": 1.0,
            "attachmentUniqueNames": [],
            "isCar": 0
        }
        self.loadedItems[name] = default_data
        self.filteredItems[name] = default_data
        self.update_file_list()
        self.activeFile = name
        self.populate_fields(default_data)
        self.fileList.setCurrentRow(self.fileList.count() - 1)

    def add_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Item JSON", "", "JSON Files (*.json)")
        if file_path:
            try:
                data = load_json(file_path)
                new_name = data.get("uniqueName", os.path.basename(file_path).replace(".json", ""))
                current_text = self.attachmentsEdit.text()
                names = [name.strip() for name in current_text.split(",") if name.strip()]
                if new_name not in names:
                    names.append(new_name)
                    self.attachmentsEdit.setText(", ".join(names))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not load file:\n{type(e).__name__}: {e}")
