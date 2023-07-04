import re
import sys
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
from functions import screenshot


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="white")
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def remove_ansi_escape_codes(s):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        str = remove_ansi_escape_codes(str)
        if self.widget.get("1.0", tk.END).strip() != '':
            str = '\n' + str
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass  # This flush method is needed for file-like object.


def first_frame(frame):
    inner_frame = ttk.Frame(frame, padding="10 10 10 10", borderwidth=2, relief="groove")
    inner_frame.grid(row=0, column=0, sticky='nsew')

    # NAME LABEL
    ttk.Label(inner_frame, text="Rune and Healing configuration").grid(row=0, column=0, sticky='nw')

    # SPELL
    ttk.Label(inner_frame, text="Rune").grid(row=1, column=0, sticky='ew', padx=10)
    ttk.Entry(inner_frame, name="rune").grid(row=2, column=0, sticky='ew', padx=10)

    ttk.Label(inner_frame, text="Mana in % necessary to cast").grid(row=1, column=1, sticky='w', padx=10)
    ttk.Entry(inner_frame, name="mana_to_cast_rune").grid(row=2, column=1, sticky='ew', padx=10)

    label_tooltip_rune = ttk.Label(inner_frame, text="?")
    label_tooltip_rune.grid(row=2, column=2, sticky='w', padx=0)
    ToolTip(label_tooltip_rune, "'Rune' is the name of the rune you want to craft \n 'mana %' is the necessary percentage to cast the rune for your character")

    # HEAL
    ttk.Label(inner_frame, text="Healing").grid(row=3, column=0, sticky='w', padx=10)
    ttk.Entry(inner_frame, name="healing").grid(row=4, column=0, sticky='ew', padx=10)

    ttk.Label(inner_frame, text="Health in % to cast").grid(row=3, column=1, sticky='w', padx=10)
    ttk.Entry(inner_frame, name="health_in_percent").grid(row=4, column=1, sticky='ew', padx=10)

    ttk.Label(inner_frame, text="Mana in % necessary to cast").grid(row=3, column=2, sticky='w', padx=10)
    ttk.Entry(inner_frame, name="mana_to_cast_healing").grid(row=4, column=2, sticky='ew', padx=10)

    label_tooltip_heal = ttk.Label(inner_frame, text="?")
    label_tooltip_heal.grid(row=4, column=3, sticky='w', padx=0)
    ToolTip(label_tooltip_heal,"'Healing' name of the healing spell \n 'health in % to cast', the % of health you want the spell to be cast \n 'Mana in % necessary to cast', the % of mana necessary to cast the spell")
    return inner_frame


def debug(x1, x2, y):
    print(f"{x1}-{x2}-{y}")
    screenshot(int(x1), int(y), int(x2), int(y))


def second_frame(frame):
    inner_frame = ttk.Frame(frame, padding="10 10 10 10", borderwidth=2, relief="solid")
    inner_frame.grid(row=1, column=0, pady=10, sticky='nsew')


    # NAME LABEL
    ttk.Label(inner_frame, text="Set up coordinates for tracking").grid(row=0, column=0, sticky='nw')

    # HEALTH X1
    ttk.Label(inner_frame, text="Health X1 coordinate").grid(row=1, column=0, sticky='ew', padx=10)
    healthx1 = ttk.Entry(inner_frame, name="healthx1")
    healthx1.grid(row=2, column=0, sticky='ew', padx=10)

    # HEALTH X2
    ttk.Label(inner_frame, text="Health X2 coordinate").grid(row=1, column=1, sticky='ew', padx=10)
    healthx2 = ttk.Entry(inner_frame, name="healthx2")
    healthx2.grid(row=2, column=1, sticky='ew', padx=10)

    # HEALTH Y
    ttk.Label(inner_frame, text="Health Y coordinate").grid(row=1, column=2, sticky='ew', padx=10)
    healthy = ttk.Entry(inner_frame, name="healthy")
    healthy.grid(row=2, column=2, sticky='ew', padx=10)

    #DEBUG HEALTH
    b1 = ttk.Button(inner_frame, text="Check Health positions are correct", command=lambda: debug(healthx1.get(), healthx2.get(), healthy.get()))
    b1.grid(row=2, column=3, sticky='ew', padx=10)

    # MANA X1
    ttk.Label(inner_frame, text="Mana X1 coordinate").grid(row=3, column=0, sticky='sw', padx=10)
    manax1 = ttk.Entry(inner_frame, name="manax1")
    manax1.grid(row=4, column=0, sticky='nw', padx=10)

    # MANA X2
    ttk.Label(inner_frame, text="Mana X2 coordinate").grid(row=3, column=1, sticky='ew', padx=10)
    manax2 = ttk.Entry(inner_frame, name="manax2")
    manax2.grid(row=4, column=1, sticky='ew', padx=10)

    # MANA Y
    ttk.Label(inner_frame, text="Mana Y coordinate").grid(row=3, column=2, sticky='ew', padx=10)
    manay = ttk.Entry(inner_frame, name="manay")
    manay.grid(row=4, column=2, sticky='ew', padx=10)

    # DEBUG MANA
    b2 = ttk.Button(inner_frame, text="Check Mana positions are correct", command=lambda: debug(manax1.get(), manax2.get(), manay.get()))
    b2.grid(row=4, column=3, sticky='ew', padx=10)

    ttk.Label(inner_frame, text="Mouse Position:", name="mousePosition").grid(row=5, column=0, sticky='ws', padx=10, pady=5)

    return inner_frame


def third_frame(frame):
    inner_frame = ttk.Frame(frame, padding="10 10 10 10", borderwidth=2, relief="solid")
    inner_frame.grid(row=3, column=0, pady=10, sticky='nsew')

    options = ["Mushroom"]

    # FOOD OPTIONS
    ttk.Label(inner_frame, text="Food").grid(row=0, column=0, sticky='nw')
    dropdown = ttk.Combobox(inner_frame, values=options)
    dropdown.grid(row=1, column=0, sticky='nw')
    dropdown.set(options[0])
    dropdown.bind("<<ComboboxSelected>>", dropdown.get())

    # EATING INTERVAL
    ttk.Label(inner_frame, text="Eating interval in minutes").grid(row=0, column=1, sticky='ew', padx=10)
    eatingInterval = ttk.Entry(inner_frame, name="eatingInterval")
    eatingInterval.grid(row=1, column=1, sticky='ew', padx=10)

    # EATING TIMES
    ttk.Label(inner_frame, text="Eating times").grid(row=0, column=2, sticky='ew', padx=10)
    eatingTimes = ttk.Entry(inner_frame, name="eatingTimes")
    eatingTimes.grid(row=1, column=2, sticky='ew', padx=10)
    return inner_frame


def forth_frame(frame):
    inner_frame = ttk.Frame(frame, padding="10 10 10 10", borderwidth=2, relief="solid")
    inner_frame.grid(row=8, column=0, pady=10, sticky='nsew')

    # NAME LABEL
    ttk.Label(inner_frame, text="Live track of player information").grid(row=0, column=0, sticky='nw')

    # OUTPUT
    text = tk.Text(inner_frame, height=3, width=90)
    text.grid(row=8, column=0, columnspan=3, sticky='nsew', pady=5)  # Changed pack to grid


    ## sys.stdout = TextRedirector(text)
    ##sys.stderr = TextRedirector(text)
