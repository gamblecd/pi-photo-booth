import io

from kivy.core.image import Image as CoreImage
from kivy.core.image.img_pil import ImageLoaderPIL
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from PIL import Image as PILImage
from ui.widgets import PhotoboothPreview
from ui.screens import PhotoboothScreen
class MemoryImage(Image):
    memory_data = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(MemoryImage, self,).__init__(**kwargs)
        #img_data = open("tests/imgs/test1_photoBooth.jpg",  "rb").read()

    def on_memory_data(self, *args):
        data = self.memory_data
        if data != '':
            with self.canvas:
                byte_arry = data
                byte_arry.seek(0)
                img2 = CoreImage(byte_arry, ext="jpg")
                byte_arry.flush();
                self.texture = img2.texture

class ImageApp(App):

    def build(self):
        screen = PhotoboothScreen()
        widget = PhotoboothPreview()
        widget.preview(generator=self.cam.generate_preview())
        memImage = MemoryImage()
        widget.bind(image_data=memImage.setter("memory_data"))
        layout= FloatLayout()
        # layout.add_widget(img)
        layout.add_widget(memImage)
        return layout

if __name__ == '__main__':
    ImageApp().run()
