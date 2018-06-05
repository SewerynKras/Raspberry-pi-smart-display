# -*- coding: utf-8 -*-
import json

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import GPIO_control as gpio
from assistant_widget import AssistantWidget
from clock_widget import ClockWidget
from temperature_widget import TemperatureWidget
from weather_widget import WeatherWidget


class GUI(FloatLayout):
    def __init__(self):
        super(GUI, self).__init__()

        config = open('config.json', "r")
        cfg = json.load(config)
        config.close()

        self.timeout = 0
        self.timeout_limit = cfg['timeout']
        self.widgets = []
        if cfg['pir_sensor']:
            self.pir = gpio.Device(cfg['pin']['PIR'], "input")

        self.control_screen = False
        if cfg['screen_relay']:
            self.control_screen = True
            self.screen = gpio.Device(
                cfg['pin']['SCREEN'], "output", n_open=False, initial_state=1)

        if cfg['weather_widget']:
            self.weather = WeatherWidget(cfg['city_name'], cfg['weather_font'])
            self.weather.size_hint = (.3, .10)
            self.weather.pos_hint = {"right": .3, "y": .25}
            self.widgets.append(self.weather)

        if cfg['temperature_widget']:
            self.temp_humi = TemperatureWidget(
                cfg['url'], cfg['temperature_font'])
            self.temp_humi.size_hint = (.2, .3)
            self.temp_humi.pos_hint = {"right": .47, "y": 0}
            self.widgets.append(self.temp_humi)

        if cfg['clock_widget']:
            self.clock = ClockWidget(cfg['clock_font'])
            self.clock.size_hint = (.2, .2)
            self.clock.pos_hint = {"right": .24, "y": 0}
            self.widgets.append(self.clock)

        if cfg['assistant_widget']:
            self.conversation = AssistantWidget(
                cfg['assistant_font'], cfg['device_model_id'])
            self.conversation.size_hint = (.45, .8)
            self.conversation.pos_hint = {"right": 1, "y": 0}
            self.widgets.append(self.conversation)

        if cfg['timeout'] > 0:
            Clock.schedule_interval(self.check_pir, .3)

        for widget in self.widgets:
            self.add_widget(widget)

    def check_pir(self, *args):

        if not self.pir.get_state():
            self.timeout += 1
            if self.timeout > self.timeout_limit and \
                    self.control_screen is True:
                self.screen.turn_off()

            if self.children:
                for widget in self.widgets:
                    self.remove_widget(widget)

        else:

            self.timeout = 0
            if not self.children:
                for widget in self.widgets:
                    self.add_widget(widget)
            if self.control_screen is True:
                self.screen.turn_on()


class MIRRORApp(App):

    def build(self):
        lt = GUI()
        return lt

    def on_stop(self):
        gpio.clean()


if __name__ == '__main__':
    MIRRORApp().run()
