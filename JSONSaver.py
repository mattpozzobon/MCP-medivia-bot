import json
import os
from tkinter import ttk


class JSONSaver:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        # Load existing data
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = {}

        # Update existing data with new data
        existing_data.update(data)

        # Save back to file
        with open(self.filename, 'w') as f:
            json.dump(existing_data, f)

    def load(self):
        with open('data.json', 'r') as f:
            return json.load(f)

    def save_values(self, frame):
        entries = {
            'manax1': "",
            'manax2': "",
            'manay': "",
            'healthx1': "",
            'healthx2': "",
            'healthy': "",
            'rune': "",
            'mana_to_cast_rune': "",
            'mana_to_cast_healing': "",
            'health_in_percent': "",
            'healing': "",
            'eatingTimes': "",
            'eatingInterval': "",
        }

        for entry in frame.children.values():
            for name in entries:
                if isinstance(entry, ttk.Entry) and entry.winfo_name() == name:
                    self.save({name: entry.get()})

    def set_values(self, frame):
        data = self.load()
        for entry in frame.children.values():
            for name in data:
                if isinstance(entry, ttk.Entry) and entry.winfo_name() == name:
                    entry.insert(0, data[name])

    def check(self):
        data = self.load()
        count = 0
        for key, value in data.items():
            if value is None or value == "":
                print(f"The checkbox: {key} value is empty.")
                count = count + 1

            elif not self.is_convertible_to_int(value) and key != "rune" and key != "healing":
                print(f"The checkbox: {key} value needs to be an integer")
                count = count + 1

        if count == 0:
            return True
        else:
            return False

    def is_convertible_to_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False