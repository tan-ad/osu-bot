import numpy as np
import cv2, time
from threading import Thread
from mss import mss
import mouse

note_queue = []


note_separation = 5
time_delay = 0.25

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5



def find_notes(img):
    for x in range(len(img)):
        for y in range(len(img[0])):
            if img[x][y][0] < 60 and img[x][y][1] < 60 and img[x][y][2] > 160:
                new_note = True
                for note in note_queue:
                    if distance((x, y), note) <= note_separation:
                        new_note = False
                        break
                if new_note:
                    note_queue.append((x, y, time.time() + time_delay, time.time() + time_delay + 0.01))


def image_processing():
    global slider_present, slider_location
    bounding_box = {'top': 0, 'left': 0, 'width': 800, 'height': 600}
    sct = mss()
    while True:
        img_sct = np.array(sct.grab(bounding_box))
        img_sct = cv2.resize(img_sct, (80, 60))
        find_notes(img_sct)
        cv2.imshow('screen', img_sct)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

def input_execution():
    while True:
        if len(note_queue) > 0:
            if time.time() > note_queue[0][2]:
                mouse.move(note_queue[0][1]*10, note_queue[0][0]*10)
                mouse.click()
            if time.time() > note_queue[0][3]:
                note_queue.pop(0)
        time.sleep(0.001)


if __name__ == '__main__':
    input()
    time.sleep(1)
    Thread(target=input_execution).start()
    Thread(target=image_processing).start()