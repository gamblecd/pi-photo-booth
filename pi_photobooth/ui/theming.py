from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import OptionProperty, AliasProperty, ObjectProperty, \
    StringProperty, ListProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.atlas import Atlas
from kivymd.color_definitions import colors
from kivymd.material_resources import FONTS, DEVICE_TYPE
from kivymd import images_path

for font in FONTS:
    LabelBase.register(**font)


class ThemeManager(Widget):
    bg_light = ObjectProperty(get_color_from_hex(colors['Light']['CardsDialogs']))
    primary_palette = OptionProperty(
            'Blue',
            options=['Pink', 'Blue', 'Indigo', 'BlueGrey', 'Brown',
                     'LightBlue',
                     'Purple', 'Grey', 'Yellow', 'LightGreen', 'DeepOrange',
                     'Green', 'Red', 'Teal', 'Orange', 'Cyan', 'Amber',
                     'DeepPurple', 'Lime'])

    primary_hue = OptionProperty(
            '500',
            options=['50', '100', '200', '300', '400', '500', '600', '700',
                     '800',
                     '900', 'A100', 'A200', 'A400', 'A700'])

    primary_light_hue = OptionProperty(
            '200',
            options=['50', '100', '200', '300', '400', '500', '600', '700',
                     '800',
                     '900', 'A100', 'A200', 'A400', 'A700'])

    primary_dark_hue = OptionProperty(
            '700',
            options=['50', '100', '200', '300', '400', '500', '600', '700',
                     '800',
                     '900', 'A100', 'A200', 'A400', 'A700'])

    accent_palette = StringProperty("Amber")
    theme_style = StringProperty("Light")
    disabled_hint_text_color = ObjectProperty((0,0,0, .26))
    standard_increment = ObjectProperty(dp(64))
    horizontal_margins =  ObjectProperty(dp(24))
    divider_color = ObjectProperty((0,0,0, .12))
    secondary_text_color = ObjectProperty((0,0, 0, .54))
    primary_text_color = ObjectProperty((0,0,0, .12))
    primary_color = ObjectProperty((.26,.65,.96, 1))
    accent_color = ObjectProperty((1,.76,.03))
    theme_text_color = ObjectProperty((0,0,0, .12))
    text_color = ObjectProperty((0,0,0, .12))
    ripple_color = ListProperty((.74,.74,.74, 1))
    
    def __init__(self, **kwargs):
        super(ThemeManager, self).__init__(**kwargs)
        self.rec_shadow = Atlas('{}rec_shadow.atlas'.format(images_path))
        self.rec_st_shadow = Atlas('{}rec_st_shadow.atlas'.format(images_path))
        self.quad_shadow = Atlas('{}quad_shadow.atlas'.format(images_path))
        self.round_shadow = Atlas('{}round_shadow.atlas'.format(images_path))
