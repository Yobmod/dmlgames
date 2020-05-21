from __future__ import annotations
# import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#from kivy.graphics import Line, Color, Ellipse
# from kivy.input import MotionEvent
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import dotenv

env = dotenv.load_dotenv('../.env')


class MyGrid(Widget):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def _submit(self) -> None:
        print(f"{self.username.text}")
        self.username.text = ""  # clear box


class MyApp(App):
    """"""

    def build(self) -> MyGrid:
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
