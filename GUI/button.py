from GUI.text_box import TextBox
class Button(TextBox):
    def __init__(self, text, font_size, text_color, background_color):
        # Only difference is that a Button's text can't be edited
        super().__init__(text, font_size, False, text_color, background_color)