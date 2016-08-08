
import flotilla
import time

class Robot:
    def __init__(self):
        self._client = flotilla.Client(
        requires = {
            'three': flotilla.Joystick,
            'four': flotilla.Motor,
            'five':   flotilla.Motor
        })

        while not self._client.ready:
            pass

        self._joystick = self._client.channel_three
        self._left = self._client.channel_four
        self._right = self._client.channel_five

        self._right.stop()
        self._left.stop()

    def run(self):
        try:
            while True:
                self._loop()
                time.sleep(0.1)
        except:
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

        print('speed = {}, direction = {} -> ({}, {})'.format(speed, direction, left, right))

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

if __name__ == '__main__':
    robot = Robot()
    robot.run()

