from kivy.config import ConfigParser

class SettingsBase:
    def __init__(self, settings_file=""):
        self.config = ConfigParser.get_configparser("photobooth_settings")
        self.config.read(settings_file)
        self.config.add_callback(self.settings_updated)

    def settings_updated(self, section, key, value):
        pass
