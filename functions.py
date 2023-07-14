import threading
import time
from datetime import datetime
import pyautogui
import pydirectinput as pyDI
from PIL import ImageDraw, Image
import pygetwindow as gw


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_image_pos(name):
    return pyautogui.locateCenterOnScreen(f'images/{name}.jpg', confidence='0.90')


def image_exists(name):
    if pyautogui.locateOnScreen(f'images/{name}.jpg', confidence='0.90') is not None:
        return True


def disable_wasd():
    if image_exists('WASD'):
        wasd_pos = get_image_pos('WASD')
        pyautogui.click(wasd_pos[0], wasd_pos[1])


def is_focused():
    window_title = "Medivia"
    return gw.getActiveWindowTitle() == window_title


def get_status_position():
    top_left = (865, 374)
    bottom_right = (935, 425)
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]
    screenshot = pyautogui.screenshot(region=(top_left[0], top_left[1], width, height))
    image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    target_color = (72, 72, 72)
    beside_color = (93, 93, 93)
    mana = -1
    health = -1

    try:
        for x in range(image.width):
            for y in range(image.height):
                pixel_color = image.getpixel((x, y))
                if pixel_color == target_color:
                    if beside_color == image.getpixel((x + 1, y)):
                        #draw = ImageDraw.Draw(screenshot)
                        #draw.line([(x, y), (x, y)], fill="red", width=1)
                        #screenshot.show()

                        count = 0
                        for i in range(0, 39):
                            pixel_color = image.getpixel(((x + 1) + i, y + 6))
                            if pixel_color[2] > 200:
                                count = count + 1
                            else:
                                break
                        mana = int((count / 39) * 100)

                        count = 0
                        for i in range(0, 39):
                            pixel_color = image.getpixel(((x + 1) + i, y + 2))
                            if pixel_color[1] > 200:
                                count = count + 1
                            else:
                                break
                        health = int((count / 39) * 100)

        return health, mana
    except:
        return health, mana


def display(current_mana=0, current_health=0, time=0, cast_time=0, status_time=0):
    health = f"{bcolors.OKGREEN}{str(current_health)}{bcolors.ENDC}"
    mana = f"{bcolors.OKBLUE}{str(current_mana)}{bcolors.ENDC}"
    runtime = f"{str(format(time, '.1f'))}"
    cast_time = f"{str(format(cast_time, '.1f'))}"
    status_time = f"{str(format(status_time, '.1f'))}"
    print(f"\rhealth: {health}% | mana: {mana}% | main-thread: {runtime} | cast-thread: {cast_time} | status-thread: {status_time} n:{threading.active_count()}", end="")


def eat(now, data):
    if not is_focused():
        return now

    current_time = datetime.now()
    if (current_time - now).total_seconds() >= int(data['eatingInterval'])*60:
        if image_exists('mushroom'):
            image = get_image_pos('mushroom')
            for i in range(int(data['eatingTimes'])):
                pyautogui.rightClick(image[0], image[1])
        return current_time
    else:
        return now


def cast(spell_type, data, current_mana=0, current_health=0):
    if not is_focused():
        return

    disable_wasd()

    if spell_type == "rune":
        if current_mana >= int(data['mana_to_cast_rune']):
            current_time = datetime.now().strftime("%H:%M")
            print("Cast at:", current_time)
            for i in range(20):
                pyautogui.write(data['rune'])
                pyDI.press('enter')
                time.sleep(0.2)

    if spell_type == "heal":
        if 1 <= current_health <= int(data['health_in_percent']) and current_mana >= int(data['mana_to_cast_healing']):
            pyautogui.write(data['healing'])
            pyDI.press('enter')


def screenshot(x1, y1, x2, y2):
    screenshot = pyautogui.screenshot()
    draw = ImageDraw.Draw(screenshot)
    draw.line([(x1, y1), (x2, y2)], fill="red", width=1)
    screenshot.show()