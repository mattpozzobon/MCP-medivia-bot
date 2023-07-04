from datetime import datetime
import time
from threading import Thread
from functions import *
import pyautogui


class Bot:
    def __init__(self):
        self.running = False
        self.data = None
        self.eating_time = datetime.now()
        self.mana = -1
        self.health = -1
        self.cast_running_time = time.time()
        self.get_status_running_time = time.time()

    def get_status(self):
        while self.running:
            start_time = time.time()
            self.mana = get_mana(self.data)
            self.health = get_health(self.data)
            end_time = time.time()
            self.get_status_running_time = end_time - start_time
            time.sleep(0.1)

    def cast(self):
        while self.running:
            start_time = time.time()
            cast("rune", self.data, current_mana=self.mana)
            cast("heal", self.data, current_mana=self.mana, current_health=self.health, )
            end_time = time.time()
            self.cast_running_time = end_time - start_time
            time.sleep(0.1)

    def run(self):
        pyautogui.FAILSAFE = False
        get_status_thread = Thread(target=self.get_status, args=())
        cast_thread = Thread(target=self.cast, args=())
        cast_thread.start()
        get_status_thread.start()

        while self.running:
            start_time = time.time()
            self.eating_time = eat(self.eating_time, self.data)
            end_time = time.time()
            time.sleep(0.1)

            display(current_mana=self.mana,
                    current_health=self.health,
                    time=end_time - start_time,
                    cast_time=self.cast_running_time,
                    status_time=self.get_status_running_time)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()
        print("ON")

    def stop(self):
        self.running = False
        self.thread.join()
        print("\nOFF")

    def setData(self, data):
        self.data = data

