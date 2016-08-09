
import flotilla
import time

class WeatherStation:

    def _clamp(value, bottom, top):
        return min(top, max(bottom, value))

    def _offset(value, bottom, top):
        value = WeatherStation._clamp(value, bottom, top)
        return int(255 * ((bottom - value) / (top - bottom)))

    def _temperature_color(temperature):
        if temperature < -10:
            return (0, 0, 255)

        elif temperature < 0:
            off = WeatherStation._offset(-10, 0, temperature)
            return (0, off, 255)

        elif temperature < 10:
            off = WeatherStation._offset(0, 10, temperature)
            return (0, 255, 255-off)

        elif temperature < 20:
            off = WeatherStation._offset(10, 20, temperature)
            return (off, 255, 0)

        elif temperature < 30:
            off = WeatherStation._offset(20, 30, temperature)
            return (255, 255-off, 0)

        else:
            return (255, 0, 0)


    def __init__(self):
        self._client = flotilla.Client()

        while not self._client.ready:
            pass

    def _connect(self):

        self._light = self._client.first(flotilla.Light)
        self._weather = self._client.first(flotilla.Weather)
        self._rainbow = self._client.first(flotilla.Rainbow)

        if self._light is None:
            print('Needs a light module')

        if self._weather is None:
            print('Needs a weather module')

        if self._rainbow is None:
            print('Needs a rainbow module')

        while self._light is None:
            self._light = self._client.first(flotilla.Light)

        while self._weather is None:
            self._weather = self._client.first(flotilla.Weather)

        while self._rainbow is None:
            self._rainbow = self._client.first(flotilla.Rainbow)

    def run(self):
        self._connect()
        try:
            while True:
                self._loop()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self._client.stop()

    def _loop(self):
        temperature = self._weather.temperature
        (r, g, b) = WeatherStation._temperature_color(temperature)
        self._rainbow.set_pixel(0, r, g, b)

        light = self._light.light
        if light < 96:
            self._rainbow.set_pixel(4, 128, 32, 0)
        else:
            self._rainbow.set_pixel(4, 0, 0, 0)

        self._rainbow.update()

if __name__ == '__main__':
    weather_station = WeatherStation()
    weather_station.run()
