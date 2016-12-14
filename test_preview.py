import logging
import io
import booth
import preview as pv
import models
import gphoto2 as gp

from PIL import Image

class PreviewTest:

    def __init__(self):
        logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
        gp.check_result(gp.use_python_logging())
        self.previewer = pv.Previewer(gp.Context())

    def testPreview(self):
        cam = models.PhotoBoothCamera()
        self.previewer.preview(cam, 6)
        cam.mirror_down()


class CameraTest:

    def __init__(self):
        pass

    def testOpenViewFinder(self):
        cam = models.PhotoBoothCamera()
        cam.mirror_up()
        cam.mirror_down()

    def testAutoFocus(self):
        cam = models.PhotoBoothCamera()
        cam.focus()
        file_data = cam.capture()
        img = cam.get_image(file_data)
        image = Image.open(io.BytesIO(img.get_data_and_size()))
        image.show()
        cam.mirror_down()

    def testLivePreview(self):
        gps.startLivePreview()

    def testAutoFocusToLivePreviewToCapture(self):
        cam = models.PhotoBoothCamera()

        #init focus, ignore picture
        cam.focus()
        file_data = cam.capture()

        cam.camera.exit(cam.context)

        #Live Preview
        gps.startLivePreview("./test.mjpg", 7)

        cam = models.PhotoBoothCamera()
        #Capture
        file_data = cam.capture()
        img = cam.get_image(file_data)
        image = Image.open(io.BytesIO(img.get_data_and_size()))
        image.show()
        cam.mirror_down()


if __name__ == "__main__":
    #PreviewTest().testPreview()
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
    boot = booth.PhotoBooth()
    #boot.takePictures(2)