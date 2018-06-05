import httplib2
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout


class TemperatureWidget(StackLayout):
    def __init__(self, url, font, font_size=48, refresh_rate=10):
        super(TemperatureWidget, self).__init__()

        self.orientation = "lr-bt"
        self.url = url

        self.temperature = Label(font_name=f"fonts/{font}",
                                 font_size=font_size,
                                 halign="left",
                                 valign="top",
                                 text="00°C",
                                 size_hint=(1, .20))

        self.humidity = Label(font_name=f"fonts/{font}",
                              font_size=font_size,
                              halign="left",
                              valign="top",
                              text="00%RH",
                              size_hint=(1, .20))

        self.temperature.bind(size=self.temperature.setter('text_size'))
        self.humidity.bind(size=self.humidity.setter('text_size'))

        self.add_widget(self.humidity)
        self.add_widget(self.temperature)

        self.refresh = Clock.schedule_interval(self.read_web, refresh_rate)
        Clock.schedule_once(self.read_web)

    def read_web(self, dt):
        try:
            _, content = httplib2.Http().request(self.url)
            temperature, humidity = content.decode().split(":")
            self.temperature.text = temperature + "°C"
            self.humidity.text = humidity + "%RH"
        except Exception as e:
            # if it failed once its likely to keep failing so we just
            # print the error message and stop updating
            print(e)
            self.temperature.text = ''
            self.humidity.text = ''
            self.refresh.cancel()
