from PIL import ImageGrab
import time
import threading
import pynput.mouse as ms
import pynput.keyboard as kb
from pynput.keyboard import Key, Controller

start_key = Key.f3
exit_key = Key.f4
keyboard = Controller()

t = time.localtime()
current_time = time.strftime("%H%M%S", t)


class Autoshot(threading.Thread):

    pImage = None
    defined = False
    pCords = [0, 0, 0, 0]
    clickCount = 0


    def area_select():
        def on_click(x, y, button, pressed):

            if pressed:
                print('({0}, {1})'.format(x, y))
                if Autoshot.clickCount == 0:
                    Autoshot.pCords[0] = x
                    Autoshot.pCords[1] = y
                elif Autoshot.clickCount == 1:
                    Autoshot.pCords[2] = x
                    Autoshot.pCords[3] = y
                    Autoshot.defined = True
                    print('')
                    Autoshot.clickCount = 0
                    return False
                Autoshot.clickCount += 1

        with ms.Listener(on_click=on_click) as listener:
            listener.join()

    def keyPress():

        print('UP ARROW')

        def on_press(key):
            i = 10

        def on_release(key):
            if key == Key.up:
                print('Pressed\n')
                Autoshot.area_select()
                Autoshot.capture()

                return False

        with kb.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def capture():

        if Autoshot.defined:
            Autoshot.pImage = ImageGrab.grab(bbox=(Autoshot.pCords[0], Autoshot.pCords[1],
                                                    Autoshot.pCords[2], Autoshot.pCords[3]))

            Autoshot.pImage.save(current_time+".png")
        else:
            print('please define an area')

if __name__ == '__main__':
    Autoshot.keyPress()