"""Image Processor 

Functionality to perform on a series of images.

combine:
    combines all the images into a single image, in the direction specified
"""
import sys
from enum import Enum
from PIL import Image

class Directions(Enum):
    VERTICAL = 1, lambda x, y: (max(x), sum(y)), lambda x, y, w, h: (x, y + h)
    HORIZONTAL = 2, lambda x, y: (sum(x), max(y)), lambda x, y, w, h: (x + w, y)

    def __new__(cls, val, size_fn, offset_fn):
        obj = object.__new__(cls)
        obj._value_ = val
        obj.size_fn = size_fn
        obj.offset_fn = offset_fn
        return obj

    def total_size(self, widths, heights):
        return self.size_fn(widths, heights)

    def offset(self, x, y):
        while True:
            width, height = yield (x, y)
            x, y = self.offset_fn(x, y, width, height)

class ImageProcessor:
    def __init__(self):
        pass

    def combine_with_name(self, images, filename, direction=Directions.VERTICAL):
        return self.combine(images, filename, direction)

    def combine(self, image_paths, filename, direction):
        """combines all the images into a single image, in the Direction specified.
        """
        if not image_paths:
            raise IndexError("image_paths need to have atleast one value")
        opened_imgs = map(Image.open, image_paths)
        # * unpacks arguments in python so the [(x,y),...] list becomes
        # [x1, x2,...], [y1, y2, ...] here.
        widths, heights = zip(*(img.size for img in opened_imgs))
        total_width, total_height = direction.total_size(widths, heights)

        new_img = Image.new('RGB', (total_width, total_height))

        offsets = direction.offset(0, 0)
        offset = offsets.send(None)
        for img in opened_imgs:
            print(offset)
            new_img.paste(img, offset)
            offset = offsets.send(img.size)

        new_img.save(filename)
        return filename
  
    def combine_v(self, image_arr):
        filename = "{}_photoBooth.jpg".format(image_arr[0].split(".")[0])
        imgs = map(Image.open, image_arr)
        widths, heights = zip(*(i.size for i in imgs))

        total_height = sum(heights)
        total_width = max(widths)

        new_im = Image.new('RGB', (total_width, total_height))

        y_offset = 0
        for img in imgs:
            new_im.paste(img, (0, y_offset))
            y_offset += img.size[1]

        new_im.save(filename)
        return filename



if __name__ == "__main__":
    testee = ImageProcessor()
    testee.combine_v(["test/test1.jpeg", "test/test.jpeg", "test/test.jpeg"])
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
