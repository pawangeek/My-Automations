from PIL import ImageGrab
import time
import threading
import pynput.mouse as ms
import pynput.keyboard as kb
from pynput.keyboard import Key, Controller

keyboard = Controller()


class Autoshot(threading.Thread):

    def __init__(self, pImage, defined, pCords, clickCount):
        super(Autoshot, self).__init__()

        self.pImage = pImage
        self.defined = defined
        self.pCords = pCords
        self.clickCount = clickCount

    def area_select(self):
        def on_click(x, y, button, pressed):

            if pressed:

                if self.clickCount == 0:
                    self.pCords[0], self.pCords[1] = x, y

                elif self.clickCount == 1:
                    self.pCords[2], self.pCords[3] = x, y

                    self.defined = True
                    self.clickCount = 0
                    return False
                self.clickCount += 1

        with ms.Listener(on_click=on_click) as listener:
            listener.join()

    def keyPress(self):

        def on_press(key):
            i = 10

        def on_release(key):
            if key == Key.f4:
                Autoshot.area_select(self)
                Autoshot.capture(self)
                return False

        with kb.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def capture(self):

        if self.defined:
            current_time = time.strftime("%H%M%S", time.localtime())
            self.pImage = ImageGrab.grab(bbox=(self.pCords[0], self.pCords[1], self.pCords[2], self.pCords[3]))
            self.pImage.save(current_time+".jpg", 'JPEG')

        else:
            print('error')


if __name__ == '__main__':

    while True:
        r = Autoshot(None, False, [0, 0, 0, 0], 0)
        r.keyPress()