import RPi.GPIO as GPIO
from picamera2 import Picamera2
from adafruit_servokit import ServoKit
from gtts import gTTS
import pygame
import time
import predict
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

model = load_model("Resnet50_False_hyperband.h5")

with open("labels.txt", "r", encoding="utf-8") as file:
    labels = file.read().splitlines()
with open("prices.txt", "r", encoding="utf-8") as file:
    prices = file.read().splitlines()

kit = ServoKit(channels=12)

#btn1 = 17
#btn2 = 2
#btn3 = 3
#rst = 0

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(rst, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera2()
total_price = 0

def take_picture():
    image_path = "./predict.jpg"
    camera.capture(image_path)
    return image_path

def speak(text):
    tts = gTTS(text=text, lang='ko')
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.quit()
    
def braille(num, digit):
    if num == 0:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 2].angle = 135
        kit.servo[digit + 3].angle = 135
    elif num == 1:
        kit.servo[digit + 1].angle = 135
    elif num == 2:
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 3].angle = 135
    elif num == 3:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 1].angle = 135
    elif num == 4:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 2].angle = 135
    elif num == 5:
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 2].angle = 135
    elif num == 6:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 3].angle = 135
    elif num == 7:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 2].angle = 135
        kit.servo[digit + 3].angle = 135
    elif num == 8:
        kit.servo[digit + 1].angle = 135
        kit.servo[digit + 2].angle = 135
        kit.servo[digit + 3].angle = 135
    else:
        kit.servo[digit + 0].angle = 135
        kit.servo[digit + 3].angle = 135    
        



print("시작")
picture = take_picture()
img = predict.predict()
prediction = model.predict(img)
result = np.argmax(prediction)
speak(labels[result])
print(labels[result])

total_price += prices[result]
print(prices[result])
mill = total_price // 100
thou = (total_price % 100) // 10
hund = total_price % 10
braille(mill, 0)
braille(thou, 4)
braille(hund, 8)
time.sleep(100)
for i in range(12):
    kit.servo[i].angle = 30


"""
try:
    while 1:
        picture = take_picture()
        result = predict.predict()
        speak(labels[result])            
        time.sleep(0.5)


finally:
    GPIO.cleanup()
    camera.close()
"""