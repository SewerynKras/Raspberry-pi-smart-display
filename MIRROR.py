# -*- coding: utf-8 -*-
import json

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import GPIO_control as gpio
from widgets.assistant_widget import AssistantWidget
from widgets.clock_widget import ClockWidget
from widgets.temperature_widget import TemperatureWidget
from widgets.weather_widget import WeatherWidget

class GUI(FloatLayout):
    def __init__(self):
        super(GUI, self).__init__()

        config = open('config.json', "r")
        cfg = json.load(config)
        config.close()

        self.timeout = 0
        self.timeout_limit = cfg['GPIO']['timeout']
        self.widgets = []

        if cfg["GPIO"]['pir_sensor'] is True:
            self.pir = gpio.Device(
                cfg["GPIO"]['pin']['PIR'],
                "input")

        if self.timeout_limit > 0:
            Clock.schedule_interval(self.check_pir, .3)

        if cfg['GPIO']['screen_relay']:
            self.control_screen = True
            self.screen = gpio.Device(
                cfg['GPIO']['pin']['SCREEN'],
                "output", n_open=False,
                initial_state=1)
        else:
            self.control_screen = False

        if cfg['clock_widget']['include'] is True:
            self.clock = ClockWidget(cfg['clock_widget']['font'])
            self.clock.size_hint = cfg['clock_widget']['size']
            self.clock.pos_hint = cfg['clock_widget']['position']
            self.widgets.append(self.clock)

        if cfg['weather_widget']['include'] is True:
            self.weather = WeatherWidget(
                cfg['weather_widget']['city_name'],
                cfg['weather_widget']['font'])
            self.weather.size_hint = cfg['weather_widget']['size']
            self.weather.pos_hint = cfg['weather_widget']['position']
            self.widgets.append(self.weather)

        if cfg['assistant_widget']['include'] is True:
            self.conversation = AssistantWidget(
                cfg['assistant_widget']['font'],
                cfg['assistant_widget']['device_model_id'])
            self.conversation.size_hint = cfg['assistant_widget']['size']
            self.conversation.pos_hint = cfg['assistant_widget']['position']
            self.widgets.append(self.conversation)

        if cfg['temperature_widget']['include'] is True:
            self.temp_humi = TemperatureWidget(
                cfg['temperature_widget']['url'],
                cfg['temperature_widget']['font'])
            self.temp_humi.size_hint = cfg['temperature_widget']['size']
            self.temp_humi.pos_hint = cfg['temperature_widget']['position']
            self.widgets.append(self.temp_humi)

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
