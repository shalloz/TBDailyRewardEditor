
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, json

class RewardEditorApp(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title("TBDailyReward Config Editor")
        self.geometry("900x600")
        self.config_dir = ""
        self.rewards = []
        self._setup_ui()

    def _setup_ui(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True)

        self.reward_tab = ttk.Frame(self.tabs)
        self.item_tab = ttk.Frame(self.tabs)
        self.condition_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.reward_tab, text='Reward Levels')
        self.tabs.add(self.item_tab, text='Items')
        self.tabs.add(self.condition_tab, text='Level Conditions')

        # Reward Tab
        self.reward_listbox = tk.Listbox(self.reward_tab)
        self.reward_listbox.pack(side='left', fill='both', expand=True)

        self.load_button = ttk.Button(self.reward_tab, text='Reload', command=self.load_rewards)
        self.load_button.pack(side='right', padx=10, pady=10)

        # Menu
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Config Folder", command=self.load_config_folder)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def load_config_folder(self):
        folder = filedialog.askdirectory(title="Select config folder")
        if folder:
            self.config_dir = folder
            self.load_rewards()
            messagebox.showinfo("Folder Loaded", f"Loaded: {folder}")

    def load_rewards(self):
        self.reward_listbox.delete(0, tk.END)
        rewards_path = os.path.join(self.config_dir, "RewardLevels")
        if os.path.exists(rewards_path):
            for file in os.listdir(rewards_path):
                if file.endswith(".json"):
                    self.reward_listbox.insert(tk.END, file)
        else:
            messagebox.showwarning("Missing", "RewardLevels folder not found in selected config folder.")

if __name__ == '__main__':
    app = RewardEditorApp()
    app.mainloop()

