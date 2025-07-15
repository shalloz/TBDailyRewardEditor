# TBDailyRewardEditor

A custom-built editor for managing Daily Reward configurations in DayZ mods.

This tool streamlines the editing and creation of JSON files used for:
- 🎁 Reward Levels
- ⚙️ Conditions
- 📦 Item Templates

Designed with clarity, modular structure, and ease-of-use in mind, TBDailyRewardEditor allows community admins and modders to create, tweak, and organize their reward progression files without digging through folders or manually editing JSON.

---

## 🧰 Features

- 🖼️ Modern GUI layout with three dedicated tabs: Items, Conditions, and Rewards
- 💾 Integrated Save buttons on each form panel
- 🧠 Helpful inline guidance for all editable fields
- 🧱 Add new entries directly inside the app (items, conditions, reward levels)
- 🧭 Automatically parses existing files from your selected folders
- 🖱️ Mouse-wheel scroll support for large forms
- 🚫 Prevents accidental data loss by preserving untouched keys during saves

---

## 🔧 Installation

### Requirements:
- Python 3.8+
- PyQt5

### Setup:

```bash
pip install -r requirements.txt
python gui/main_window.py

🗂️ Folder Structure
TBDailyRewardEditor/
├── gui/
│   └── Editor_Widgets/
│       ├── item_browser.py
│       ├── condition_editor.py
│       └── reward_editor.py
├── logic/
│   └── json_loader.py
├── requirements.txt
├── README.md

✍️ Credits
Built and maintained by shalloz — founder of the LegendsEndDayZServers.

All JSON formats, rules, and schema logic follow the official documentation provided by the original mod developer of TBDailyRewards

🗃️ License
None

