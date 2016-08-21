import flotilla
import time

from sklearn.tree import DecisionTreeClassifier

class Colors:
    Red = 0
    Green = 1
    Blue = 2
    Yellow = 3
    Orange = 4
    Purple = 5
    Unknown = 6

    name = {
        Red     : 'Red',
        Green   : 'Green',
        Blue    : 'Blue',
        Yellow  : 'Yellow',
        Orange  : 'Orange',
        Purple  : 'Purple',
        Unknown : 'Unknown'
    }

X = [
    #red
    [0.455,0.288,0.329],
    [0.434,0.264,0.293],
    [0.503,0.281,0.316],
    [0.466,0.285,0.324],
    [0.481,0.285,0.319],
    [0.506,0.272,0.307],
    [0.483,0.287,0.323],
    [0.379,0.217,0.250],

    #green
    [0.359,0.363,0.336],
    [0.330,0.385,0.334],
    [0.334,0.380,0.326],
    [0.277,0.325,0.276],
    [0.345,0.385,0.334],
    [0.326,0.390,0.332],
    [0.321,0.364,0.323],
    [0.336,0.388,0.352],

    #blue
    [0.341,0.316,0.387],
    [0.186,0.194,0.239],
    [0.316,0.332,0.403],
    [0.321,0.332,0.403],
    [0.174,0.182,0.224],
    [0.301,0.319,0.391],
    [0.319,0.332,0.404],
    [0.246,0.256,0.312],

    #yellow
    [0.439,0.337,0.258],
    [0.440,0.354,0.253],
    [0.430,0.364,0.241],
    [0.445,0.354,0.246],
    [0.440,0.360,0.258],
    [0.452,0.359,0.243],
    [0.367,0.299,0.203],
    [0.449,0.362,0.264],

    #orange
    [0.486,0.280,0.298],
    [0.498,0.290,0.289],
    [0.494,0.285,0.285],
    [0.495,0.282,0.278],
    [0.507,0.289,0.291],
    [0.493,0.288,0.291],
    [0.499,0.287,0.288],
    [0.507,0.284,0.287],

    #purple
    [0.381,0.260,0.319],
    [0.410,0.294,0.356],
    [0.372,0.274,0.323],
    [0.424,0.297,0.351],
    [0.426,0.303,0.354],
    [0.401,0.280,0.330],
    [0.352,0.244,0.286],
    [0.424,0.302,0.358],

    #black
#    [0.378,0.321,0.358],
#    [0.374,0.325,0.362],
#    [0.330,0.287,0.317],
#    [0.393,0.359,0.378],
#    [0.361,0.305,0.339],
#    [0.390,0.326,0.356],
#    [0.383,0.319,0.357],
#    [0.343,0.305,0.341],

    #white
#    [0.399,0.344,0.290],
#    [0.404,0.357,0.289],
#    [0.397,0.352,0.292],
#    [0.403,0.351,0.290],
#    [0.406,0.351,0.292],
#    [0.389,0.349,0.289],
#    [0.381,0.356,0.295],
#    [0.386,0.359,0.295]
]

y = [
    Colors.Red,
    Colors.Red,
    Colors.Red,
    Colors.Red,
    Colors.Red,
    Colors.Red,
    Colors.Red,
    Colors.Red,

    Colors.Green,
    Colors.Green,
    Colors.Green,
    Colors.Green,
    Colors.Green,
    Colors.Green,
    Colors.Green,
    Colors.Green,

    Colors.Blue,
    Colors.Blue,
    Colors.Blue,
    Colors.Blue,
    Colors.Blue,
    Colors.Blue,
    Colors.Blue,
    Colors.Blue,

    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,
    Colors.Yellow,

    Colors.Orange,
    Colors.Orange,
    Colors.Orange,
    Colors.Orange,
    Colors.Orange,
    Colors.Orange,
    Colors.Orange,
    Colors.Orange,

    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
    Colors.Purple,
]

class Color:

    def __init__(self):
        self.previous = Colors.Unknown
        self.count = 0

        self.model = DecisionTreeClassifier()

        self.client = flotilla.Client()

        while not self.client.ready:
            pass

    def require(self, modules):
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

    def connect(self):
        (self.color, self.light) = self.require([flotilla.Colour, flotilla.Light])

    def run(self):
        self.connect()
        try:
            self.learn()
            print('Ready')
            while True:
                self.loop()
        except KeyboardInterrupt:
            self.client.stop()

    def learn(self):
        self.model.fit(X, y)

    def loop(self):
        if self.light.light < 500:

            c = self.color.clear

            r = self.color.red / c
            g = self.color.green / c
            b = self.color.blue / c

            color = self.model.predict([[r, g, b]])[0]
            if color != self.previous:
                self.count = 0
                self.previous = color
            else:
                if self.count < 10:
                    self.count = self.count + 1
                elif self.count == 10 :
                    self.count = self.count + 1
                    print(Colors.name[color])

            time.sleep(0.05)

        else:
            self.previous = Colors.Unknown
            time.sleep(0.5)

if __name__ == '__main__':
    app = Color()
    app.run()
