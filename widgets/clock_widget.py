import datetime

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout


class ClockWidget(StackLayout):
    def __init__(
            self,
            font,
            font_size=(120, 50),
            date_format="%d.%m.%Y",
            time_format="%H:%M"):
        """Displays time using the datetime module

        Arguments:
            font {str} -- font file located in 'fonts/' folder

        Keyword Arguments:
            font_size {tuple} -- (default: {(120, 50)})
            date_format {str} -- datetime format (default: {"%d.%m.%Y"})
            time_format {str} -- datetime format (default: {"%H:%M"})
        """

        super(ClockWidget, self).__init__()
        self.orientation = "lr-bt"
        self.time_format = time_format
        self.date_format = date_format

        self.hour_min = Label(font_name=f"fonts/{font}",
                              font_size=font_size[0],
                              valign="bottom",
                              size_hint=(1, .6))

        self.date_year = Label(font_name=f"fonts/{font}",
                               font_size=font_size[1],
                               valign="bottom",
                               size_hint=(1, .2))

        self.date_year.bind(texture_size=self.date_year.setter("size"))
        self.hour_min.bind(texture_size=self.hour_min.setter("size"))

        self.add_widget(self.date_year)
        self.add_widget(self.hour_min)
        self.refresh = Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        time = datetime.datetime.now()
        self.hour_min.text = time.strftime(self.time_format)
        self.date_year.text = time.strftime(self.date_format)

    def stop(self):
        """Stops the kivy.Clock instance"""
        self.refresh.cancel()
