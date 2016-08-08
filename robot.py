
import flotilla
import time
import random

class Robot:
    def __init__(self):
        self._client = flotilla.Client(
        requires = {
            'three': flotilla.Joystick,
            'four':  flotilla.Motor,
            'five':  flotilla.Motor,
            'six':   flotilla.Matrix
        })

        while not self._client.ready:
            pass

        self._joystick = self._client.channel_three
        self._left = self._client.channel_four
        self._right = self._client.channel_five
        self._matrix = self._client.channel_six

        self._right.stop()
        self._left.stop()

        self._brightness = 20
        self._matrix.set_brightness(self._brightness)

    def run(self):
        try:
            while True:
                self._loop()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self._client.stop()

    def _loop(self):
        speed = 0
        direction = 0
        x = self._joystick.x
        y = self._joystick.y
        if y < 448:
            speed = int((512 - y ) / 16)
        elif y > 576:
            speed = -int((y - 512) / 16)

        if x < 448:
            direction = int((512 - x) / 16)
        elif x > 576:
            direction = -int((x - 512) / 16)

        right = speed - direction
        left = -speed - direction

        if left < -31:
            left = -31
        elif left > 31:
            left = 31

        if right < -31:
            right = -31
        elif right > 31:
            right = 31

        if right == 0:
            self._right.stop()
        else:
            self._right.speed = right
            self._right.update()

        if left == 0:
            self._left.stop()
        else:
            self._left.speed = left
            self._left.update()


        self._matrix.clear()

        if speed == 0 and direction == 0:
            if self._brightness > 1:
                self._brightness = self._brightness - 1
                self._matrix.set_pixel(4, 4, True)
                self._matrix.set_pixel(4, 3, True)
                self._matrix.set_pixel(3, 4, True)
                self._matrix.set_pixel(3, 3, True)
            else:
                for x in range(8):
                    for y in range(8):
                        on = random.random() < 0.2
                        self._matrix.set_pixel(x, y, on)

        else:
            self._brightness = 40

            x = 4 - int(direction / 8)
            y = int(speed / 8) + 4

            if x < 1:
                x = 1
            if x > 7:
                x = 7
            if y < 1:
                y = 1
            if y > 7:
                y = 7

            self._matrix.set_pixel(x,   y,   True)
            self._matrix.set_pixel(x,   y-1, True)
            self._matrix.set_pixel(x-1, y,   True)
            self._matrix.set_pixel(x-1, y-1, True)

        self._matrix.set_brightness(self._brightness)
        self._matrix.update()

if __name__ == '__main__':
    robot = Robot()
    robot.run()

