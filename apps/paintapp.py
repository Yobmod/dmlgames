from __future__ import annotations
# import kivy
from kivy.app import App
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import dotenv
import os
from random import random
from kivy.input import MotionEvent

env = dotenv.load_dotenv('../.env')
KIVY_DATA_DIR = os.environ.get('KIVY_DATA_DIR') or './data'
# KIVY_MODULES_DIR = os.environ['KIVY_DATA_DIR'] or './modules'


class LoginScreen(GridLayout):
    """"""

    def __init__(self, **kwargs: object) -> None:
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="Username: "))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="Password: "))
        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)

        self.add_widget(Label(text="Two Factor Auth: "))
        self.tfa = TextInput(multiline=False)
        self.add_widget(self.tfa)


class PaintWidget(Widget):

    def on_touch_down(self, touch: MotionEvent) -> None:
        # print(touch)
        with self.canvas:
            color = (random(), 1.0, 1.0)
            Color(*color, mode='hsv')  # default mode='rgb'
            # color = (random(), random(), random())
            # Color(*color, mode='rgb')  # default mode='rgb'
            d = 30.0
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch: MotionEvent) -> None:
        # print(touch)
        touch.ud["line"].points += (touch.x, touch.y)

    def on_touch_up(self, touch: MotionEvent) -> None:
        # print("Released", touch)
        with self.canvas:
            d = 30.0
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))


class PaintApp(App):
    """"""

    def build(self) -> Widget:
        # return LoginScreen()
        parent: Widget = Widget()
        self.painter = PaintWidget()
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj: Button) -> None:
        self.painter.canvas.clear()


if __name__ == "__main__":
    PaintApp().run()
