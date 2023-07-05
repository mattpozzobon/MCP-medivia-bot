import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import PhotoImage
import pyautogui
from JSONSaver import JSONSaver
from bot import Bot
from frames import first_frame, second_frame, third_frame, forth_frame
from pynput import keyboard
import pygetwindow as gw
import simpleaudio as sa


class Ui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MCP v.1.0")
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Variables
        self.bot = Bot()
        self.botRunning = False
        self.botThread = threading.Thread(target=self.bot.run, args=())
        self.saver = JSONSaver('data.json')
        self.has_been_checked = False

        # Create frames
        self.first_frame = self.create_first_frame()
        self.second_frame = self.create_second_frame()
        self.third_frame = self.create_third_frame()
        self.create_forth_frame()

        # Set values
        self.saver.set_values(self.first_frame)
        self.saver.set_values(self.second_frame)
        self.saver.set_values(self.third_frame)

        # Create label and image
        self.create_home_label_image("Press HOME to start", 10)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()

        self.update()
        self.root.mainloop()

    def on_press(self, key):
        try:
            if key == keyboard.Key.home:
                self.function_to_run()
        except AttributeError:
            pass

    def show_blinking_image(self, flag):
        name = "MCP v.1.0"
        window = gw.getWindowsWithTitle(name)[0].isActive

        image = "off"
        if flag:
            image = "on"
            wave_obj = sa.WaveObject.from_wave_file('sounds/switch.wav')
            play_obj = wave_obj.play()
            play_obj.wait_done()

        if not window:
            top = tk.Toplevel(self.root)
            top.overrideredirect(1)  # Remove window decorations
            top.wm_attributes("-topmost", 1)  # Make window stay on top

            # Load the image
            img = tk.PhotoImage(file=f"images/{image}.png")  # Use gif image
            top.geometry("%dx%d+0+0" % (img.width(), img.height()))  # Set window size to image size

            # Create the label with the image
            label = tk.Label(top, image=img)
            label.image = img  # Keep a reference to the image
            label.pack()

            # Update window dimensions
            top.update_idletasks()

            # Center the window on the screen
            x = (self.root.winfo_screenwidth() - top.winfo_width()) // 2
            y = (self.root.winfo_screenheight() - top.winfo_height()) // 2
            top.geometry(f"+{x}+{y}")

            # Show the window for a moment then destroy it
            top.after(500, top.destroy)  # 500ms = 0.5s

    def function_to_run(self):
        if self.botRunning:
            self.bot.stop()
            self.botRunning = False
        else:
            self.saver.save_values(self.first_frame)
            self.saver.save_values(self.second_frame)
            self.saver.save_values(self.third_frame)

            if self.saver.check():
                self.has_been_checked = True
                if not self.botRunning:
                    self.bot.setData(self.saver.load())
                    self.bot.start()
                    self.botRunning = True
        self.show_blinking_image(self.botRunning)

    def update(self):
        x, y = pyautogui.position()
        label = self.second_frame.children['mousePosition']
        label.config(text=f'X: {x}, Y: {y}')
        if self.botRunning:
            img = PhotoImage(file="images/on.png")
        else:
            img = PhotoImage(file="images/off.png")
        self.image_label_home.config(image=img)
        self.image_label_home.image = img
        self.root.after(1, self.update)

    def create_first_frame(self):
        return first_frame(self.frame)

    def create_second_frame(self):
        return second_frame(self.frame)

    def create_third_frame(self):
        return third_frame(self.frame)

    def create_forth_frame(self):
        forth_frame(self.frame)

    def create_home_label_image(self, text, row):
        ttk.Label(self.frame, text=text).grid(row=row, column=0)
        img = PhotoImage(file="images/off.png")
        self.image_label_home = ttk.Label(self.frame, image=img)
        self.image_label_home.grid(row=row, column=1)


ui = Ui()