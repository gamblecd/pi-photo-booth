import io

from kivy.core.image import Image as CoreImage
from kivy.core.image.img_pil import ImageLoaderPIL
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from PIL import Image as PILImage

class MemoryImage(Image):
    memory_data = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(MemoryImage, self,).__init__(**kwargs)
        img_data = open("tests/imgs/test1_photoBooth.jpg",  "rb").read()
        self.memory_data = img_data
    
    def on_memory_data(self, *args):
        data = self.memory_data
        
        img = PILImage.open("tests/imgs/test1_photoBooth.jpg")
        img = img.resize((800,480))
        with self.canvas:
            print(img.height)
            print(img.width)
            byte_arry = io.BytesIO()
            img.save(byte_arry, format="jpeg")
            byte_arry.seek(0)
            img2 = CoreImage(byte_arry, ext="jpg")
            print(img.height)
            print(img.width)
            img = None
            byte_arry.flush();
            self.texture = img2.texture

class ImageApp(App):

    def build(self):
        img = Image(source="tests/imgs/test1_photoBooth.jpg", mipmap=True,size=(600,400), allow_stretch=True)
        layout= FloatLayout()
        # layout.add_widget(img)
        layout.add_widget(MemoryImage(size=(800,600)))
        return layout

if __name__ == '__main__':
    ImageApp().run()
