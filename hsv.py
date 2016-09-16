import flotilla
import time
import colorsys

class Main:

    def __init__(self):
        self.client = flotilla.Client()
        while not self.client.ready:
            pass

    def start(self):
        self._connect()
        try:
            print('start learning')
            self._learn()
            print('ready')
            while True:
                self._loop()
        except KeyboardInterrupt:
            self.client.stop()
            print('end')

    def _require(self, modules):
        module_list = []
        for i, module in enumerate(modules):
            module_list.append(self.client.first(module))

        for i, module in enumerate(modules):
            if module_list[i] is None:
                print('Require a {} module'.format(module))

        for i, module in enumerate(modules):
            while module_list[i] is None:
                module_list[i] = self.client.first(module)

        return module_list

    def _connect(self):
        (self.color, self.light) = self._require([flotilla.Colour, flotilla.Light])

    def _learn(self):
        pass

    def _loop(self):
        if self.light.light < 500:

            c = self.color.clear

            normalize = lambda x: min(max(0.0, x / c), 1.0)

            r = normalize(self.color.red)
            g = normalize(self.color.green)
            b = normalize(self.color.blue)

            hls = colorsys.rgb_to_hls(r, g, b)
            hsv = colorsys.rgb_to_hsv(r, g, b)

            f = lambda x: '{:.2f},{:.2f},{:.2f}'.format(x[0], x[1], x[2])

            print('{} -> {} : {}'.format(f([r, g, b]), f(hls), f(hsv)))

            h = hls[0]
            if h < 0.04:
                print('red')
            elif h < 0.12:
                print('orange')
            elif h < 0.25:
                print('yellow')
            elif h < 0.42:
                print('green')
            elif h < 0.58:
                print('cyan')
            elif h < 0.75:
                print('blue')
            elif h < 0.92:
                print('magenta')
            else:
                print('red')

        time.sleep(0.2)

if __name__ == '__main__':
    main = Main()
    main.start()

