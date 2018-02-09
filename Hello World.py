from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
class HelloWorld(App):
	def build (self):
		layout = BoxLayout()
		layout.add_widget(Button(text="Hello There :)"))
		return layout
HelloWorld().run()