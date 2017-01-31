import flotilla
import pyo
import time

class Envelope:
    def __init__(self, env):
        self.env = env
        self.playing = False

class Synth:

    def __init__(self):
        self.client = flotilla.Client()

        while not self.client.ready:
            pass

    def connect_item(self, type, name):
        item = None
        print('Connecting {}...'.format(name))
        while item is None:
            item = self.client.first(type)
        print('...done')
        return item

    def connect(self):
        self.slider = self.connect_item(flotilla.Slider, 'slider')
        self.dial = self.connect_item(flotilla.Dial, 'dial')
        self.touch = self.connect_item(flotilla.Touch, 'touch')
        self.rainbow = self.connect_item(flotilla.Rainbow, 'rainbow')

        self.server = pyo.Server(sr=48000, duplex=0)
        self.server.setOutputDevice(9)
        self.server.boot()
        self.server.start()

        self.sine = pyo.Sine()
        self.lfo = pyo.LFO(mul=self.sine).out()

        self.env1 = Envelope(pyo.Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.7, mul=0.8))
        self.lfo1 = pyo.LFO(mul=self.env1.env, freq=440, type=4).out()

        self.env2 = Envelope(pyo.Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.7, mul=0.8))
        self.lfo2 = pyo.LFO(mul=self.env2.env, freq=523, type=4).out()

        self.env3 = Envelope(pyo.Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.7, mul=0.8))
        self.lfo3 = pyo.LFO(mul=self.env3.env, freq=659, type=4).out()

        self.env4 = Envelope(pyo.Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.7, mul=0.8))
        self.lfo4 = pyo.LFO(mul=self.env4.env, freq=880, type=4).out()

        self.pat = pyo.Pattern(Synth.metro, time=0.5, arg=self).play()
        self.beat = 0

    def metro(self):
        self.beat = self.beat + 1
        if self.beat >= 4:
            self.beat = 0
        self.rainbow.set_all(0, 0, 0)
        self.rainbow.set_pixel(self.beat, 64 * self.beat, 128, 192 - 64 * self.beat)
        self.rainbow.update()

    def run(self):
        self.connect()
        try:
            while True:
                self.loop()
                time.sleep(0.01)
        except KeyboardInterrupt:
            print('Shutting down...')
            self.client.stop()
            print('... flotilla')
            self.server.stop()
            print('... stop pyo')
            self.server.shutdown()
            print('... shutdown pyo')

    def loop(self):
        f = self.dial.position / 50.0 + 0.001
        if f != self.sine.freq:
            self.sine.setFreq(f)

        f = self.slider.position * 2 + 100
        if f != self.lfo.freq:
            if f <= 100:
                self.lfo.setMul(0)
            elif self.lfo.mul == 0:
                self.lfo.setMul(self.sine)
            self.lfo.setFreq(f)

        self.eval_touch(self.env1, self.touch.one)
        self.eval_touch(self.env2, self.touch.two)
        self.eval_touch(self.env3, self.touch.three)
        self.eval_touch(self.env4, self.touch.four)

    def eval_touch(self, env, touch):
        if touch:
            if not env.playing:
                env.env.play()
                env.playing = True
        else:
            if env.playing:
                env.env.stop()
                env.playing = False

if __name__ == '__main__':
    synth = Synth()
    synth.run()
    print('...done')

