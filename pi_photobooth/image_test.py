from kivy.lang import Builder
Builder.load_string('''

<PhotoboothScreen>
    RelativeLayout:
        PhotoboothPreview:
            pos_hint: {'center_x': .5, 'center_y': .5}
            size_hint: (1,1)
            id: preview
        Countdown:
            pos_hint: {'x': .0, 'y': .8}
            size_hint: (.1, .3)
            id: countdown
            starting_number: 5
        Button:
            size_hint:(.3, .1)
            pos_hint: {'center_x': .5, 'y': .05}
            id: shoot_button
            text: "Take My Picture"
            on_press:
                root.run_booth()
        Button:
            size_hint: (.1, .1)
            pos_hint: {'x': .9, 'y': .9}
            id: close_button
            text: "Cancel"
            on_press:
                # Update the nav_drawer back to welcome
                app.root.ids.nav_drawer.active_item._active = False
                app.root.ids.nav_drawer.active_item = app.root.ids.welcome
                app.root.ids.nav_drawer.active_item._active = True

                root.manager.transition.direction = 'down'
                root.manager.current = 'welcome'
                app.root.ids.toolbar.size_hint_y = None
<Countdown>:
    Label:
        id: label
        text: str(root.current) if root.current >= 0 else ''
        font_size:50
        outline_width:2

''')


import io

from kivy.core.image import Image as CoreImage
from kivy.core.image.img_pil import ImageLoaderPIL
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from PIL import Image as PILImage
from ui.widgets import *
from ui.screens import *

from kivymd.theming import ThemeManager

SettingsScreen()

class ImageApp(App):
    theme_cls = ThemeManager()
    def __init__(self, **kwargs):
        super(ImageApp, self).__init__(**kwargs)

    def build(self):
        return PhotoboothScreen()

if __name__ == '__main__':
    ImageApp().run()
