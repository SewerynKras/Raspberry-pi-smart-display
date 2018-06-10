# FIXME: Emojis
import json
import os.path
import threading

import google.auth.transport.requests
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.app import App


class AssistantBlock(BoxLayout):

    def __init__(self, text, font, font_size=20,
                 size_hint=(1, None), picture=True):
        super(AssistantBlock, self).__init__()
        self.orientation = 'horizontal'
        self.size_hint = size_hint
        if picture:
            img = Image(source='icons/Assistant_logo.png',
                        size_hint=(.1, None))
        else:
            img = Label(text='', size_hint=(.1, None))
        txt = Label(
            font_size=font_size,
            text=text,
            font_name=f'fonts/{font}',
            size_hint=(.7, None),
            text_size=(self.size[0] * 4, None),
            valign='bottom',
            halign='left')
        self.add_widget(img)
        self.add_widget(txt)


class UserBlock(BoxLayout):

    def __init__(self, text, font, font_size=20, size_hint=(1, None)):
        super(UserBlock, self).__init__()
        self.orientation = 'horizontal'
        self.size_hint = size_hint
        blank_left = Label(text='', size_hint=(.3, None))
        txt = Label(
            font_size=font_size,
            font_name=f'fonts/{font}',
            text=text,
            size_hint=(.7, None),
            valign='top',
            halign='right',
            text_size=(self.size[0] * 4, None))
        self.add_widget(blank_left)
        self.add_widget(txt)


class AssistantWidget(StackLayout):

    def __init__(self, font, device_model_id):
        super(AssistantWidget, self).__init__()
        self.orientation = "lr-tb"
        self.last_block = False
        self.font = font
        self.timer = 0
        self.model_id = device_model_id
        Clock.schedule_once(self.activate)

    @mainthread
    def begin_new_conversation(self):
        self.clear_widgets()
        Clock.schedule_interval(self.check_timer, 1)
        self.timer = 0
        self.last_block = False
        block = AssistantBlock(text="Hi, how can I help?", font=self.font)
        self.add_widget(block)

    @mainthread
    def add_block(self, type, text):
        self.timer = 0
        if len(self.children) > 6:
            self.clear_widgets()
        if type == 'ASSISTANT':
            block = AssistantBlock(
                text=f" {text}", font=self.font, picture=self.last_block)
            self.last_block = False
        elif type == 'USER':
            self.last_block = True
            block = UserBlock(text=text, font=self.font)
        self.add_widget(block)

    @mainthread
    def check_timer(self, dt):
        self.timer += 1
        if self.timer > 60:
            self.clear_widgets()
            self.timer = 0
            self.last_block = True
            Clock.unschedule(self.check_timer)

    def process_device_actions(self, event, device_id):
        if 'inputs' in event.args:
            for i in event.args['inputs']:
                if i['intent'] == 'action.devices.EXECUTE':
                    for c in i['payload']['commands']:
                        for device in c['devices']:
                            if device['id'] == device_id:
                                if 'execution' in c:
                                    for e in c['execution']:
                                        if 'params' in e:
                                            yield e['command'], e['params']
                                        else:
                                            yield e['command'], None

    @mainthread
    def process_event(self, event, device_id):
        if event.type == EventType.ON_CONVERSATION_TURN_STARTED \
                and self.timer == 0:
            self.begin_new_conversation()
        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
            self.add_block(text=event.args['text'], type="USER")

        if event.type == EventType.ON_RENDER_RESPONSE:
            self.add_block(text=event.args['text'], type='ASSISTANT')
        # TODO: Add code that does something here
        if event.type == EventType.ON_DEVICE_ACTION:
            print(event)
            for command, params \
                    in self.process_device_actions(event, device_id):
                print('Do command', command, 'with params', str(params))
            if command == "action.devices.commands.OnOff":
                if params['on']:
                    print("Turn on!")
                else:
                    print("Turn off!")

    def activate(self, dt):
        threading.Thread(
            target=self.start_assistant, args=(self.model_id,)).start()

    def start_assistant(self, device_model_id):

        with open(os.path.join(
                os.path.expanduser('~/.config'), 'google-oauthlib-tool',
                'credentials.json'), 'r') as f:
            credentials = google.oauth2.credentials.Credentials(
                token=None, **json.load(f))

        with Assistant(credentials, device_model_id) as assistant:
            events = assistant.start()
            for event in events:
                self.process_event(event, assistant.device_id)


if __name__ == "__main__":
    class myApp(App):
        def build(self):
            ly = AssistantWidget("mirror-LED")
            return ly
    a = myApp()
    a.run()
