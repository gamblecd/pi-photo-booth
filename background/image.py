import sys
from PIL import Image


class ImageProcessor:
    def __init__(self):
        pass
    
    def combine(self, image_arr):
        filename = "{}_photoBooth.jpg".format(image_arr[0].split(".")[0])
        imgs = map(Image.open, image_arr)
        widths, heights = zip(*(i.size for i in imgs))

        total_height = sum(heights)
        total_width = max(widths)

        new_im = Image.new('RGB', (total_width, total_height))

        y_offset = 0
        for im in imgs:
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]
        
        new_im.save(filename)
        return filename;



if __name__ == "__main__":
    testee = ImageProcessor()
    testee.combine(["test/test1.jpeg", "test/test.jpeg", "test/test.jpeg"])
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
