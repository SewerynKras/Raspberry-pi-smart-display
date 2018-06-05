from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from weather import Unit, Weather


class WeatherWidget(BoxLayout):
    def __init__(
            self,
            city_name,
            font,
            font_size={"temperature": 65, "condition": 35, "high_low": 20},
            refresh_rate=120,
            unit="CELSIUS"):
        super(WeatherWidget, self).__init__()

        self.orientation = "horizontal"
        self.padding = 1
        self.city = city_name
        self.unit = unit

        self.picture = Image(size_hint=(.4, 1))

        self.info_layout = BoxLayout(size_hint=(.5, 1))
        self.info_layout.orientation = "vertical"

        self.temperature = Label(font_name=f"fonts/{font}",
                                 font_size=font_size["temperature"],
                                 size_hint=(1, .5),
                                 )

        self.condition = Label(font_name=f"fonts/{font}",
                               font_size=font_size["condition"],
                               size_hint=(1, .25),
                               )

        self.top_low = Label(font_name=f"fonts/{font}",
                             font_size=font_size["high_low"],
                             size_hint=(1, .25),
                             )

        self.info_layout.add_widget(self.temperature)
        self.info_layout.add_widget(self.top_low)
        self.info_layout.add_widget(self.condition)

        self.add_widget(self.picture)
        self.add_widget(self.info_layout)

        self.refresh = Clock.schedule_interval(self.update, refresh_rate)
        Clock.schedule_once(self.update)

    def update(self, *args):
        if self.unit.lower() == "celsius":
            weather = Weather(unit=Unit.CELSIUS)
            symbol = "°C"
        elif self.unit.lower() == "fahrenheit":
            weather = Weather(unit=Unit.FAHRENHEIT)
            symbol = "°F"
        try:
            forecast = weather.lookup_by_location(self.city)
            self.picture.source = f"icons/{forecast.condition.code}.png"
            self.temperature.text = f"{forecast.condition.temp}{symbol}"
            self.condition.text = f"{forecast.condition.text}"
            self.top_low.text = f"{forecast.forecast[0].high}{symbol}" + \
                "  |  " + f"{forecast.forecast[0].low}{symbol}"
        except Exception as e:
            print(e)
