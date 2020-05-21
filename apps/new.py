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
import dotenv

env = dotenv.load_dotenv('../.env')


class MyGrid(GridLayout):

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.cols = 2

        # row1
        self.add_widget(Label(text="Username: "))

        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        # row2
        self.add_widget(Label(text="Password: "))

        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)

        # row3
        self.submitBttn = Button(text='Submit', font_size=30)
        self.submitBttn.bind(on_press=self._submit)
        self.add_widget(self.submitBttn)

    def _submit(self, e: object) -> None:
        print(f"{self.username.text}")
        self.username.text = ""  # clear box


class MyApp(App):
    """"""

    def build(self) -> MyGrid:
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
