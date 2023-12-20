from ctypes import windll, Structure, c_long, byref
import time
import cv2
import mss
import numpy as np
import pyautogui

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}

def right_click():
    pyautogui.mouseDown(button='right')
    time.sleep(0.01)
    pyautogui.mouseUp(button='right')

def image_match(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8  # Настройте порог в соответствии с вашими требованиями
    if max_val >= threshold:
        return max_loc
    return None

# Загрузка изображения-шаблона с использованием сырой строки или двойного обратного слеша
template_img_path = r"D:\Desktop\Python\test.png"
template_img = cv2.imread(template_img_path, cv2.IMREAD_UNCHANGED)

title = "Нахождение объекта"
sct = mss.mss()

print("Начало через 7 секунд, настройте удочку!")
time.sleep(7)
print("Начало...")

right_click()
print("Тестовый клик")
last_time = time.time()

while True:
    if time.time() - last_time < 2:
        continue

    cur = queryMousePosition()
    mon = {"top": cur['y'] - 50, "left": cur['x'] - 50, "width": 100, "height": 100}  # Настройте размер области по вашему усмотрению
    img = np.asarray(sct.grab(mon))

    match_location = image_match(img, template_img)

    if match_location is not None:
        print("Обнаружено изображение-шаблон! Выполняется правый клик...")
        right_click()
        time.sleep(1)
        last_time = time.time()
        right_click()
