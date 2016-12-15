"""Main Test File for Photo Booth

Usage:
    

"""
import unittest
import logging
import os
import io

from pi_photobooth.background.image import ImageProcessor, Directions

from PIL import Image

class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = ImageProcessor()
        if not os.path.exists("pi_photobooth/tests/imgs/results"):
            os.mkdir("pi_photobooth/tests/imgs/results")
    
    def tearDown(self):
        if os.path.exists("pi_photobooth/tests/imgs/results"):
            pass
            #for filename in os.listdir("pi_photobooth/tests/imgs/results"):
            #    os.remove("pi_photobooth/tests/imgs/results/{}".format(filename))
            #os.rmdir("pi_photobooth/tests/imgs/results")
        

    def test_empty(self):
        with self.assertRaises(IndexError):
            self.processor.combine_with_name([], "")
            
    def test_filename(self):
        expected_filename = "pi_photobooth/tests/imgs/results/test_filename.jpg"
        filename =  self.processor.combine_with_name(["pi_photobooth/tests/imgs/test.jpg"], expected_filename)
        self.assertEquals(expected_filename, filename)

    def test_one_image(self):
        test_file = "pi_photobooth/tests/imgs/test.jpg"
        test_file_img = Image.open(test_file)
        filename = self.processor.combine_with_name([test_file], "pi_photobooth/tests/imgs/results/test_one_image.jpg")
        result_file = Image.open(filename)
        self.assertEquals(test_file_img.size, result_file.size)
        
    def test_two_images_is_twice_as_tall(self):
        test_file = "pi_photobooth/tests/imgs/test.jpg"
        test_file_img = Image.open(test_file)
        filename = self.processor.combine_with_name([test_file, test_file], "pi_photobooth/tests/imgs/results/result.jpg")
        result_file = Image.open(filename)
        self.assertEquals(test_file_img.size[0], result_file.size[0])
        self.assertEquals(2 * test_file_img.size[1], result_file.size[1], "Expected Height to be twice as tall")

    def test_two_images_horizontal_twice_as_wide(self):
        test_file = "pi_photobooth/tests/imgs/test.jpg"
        test_file_img = Image.open(test_file)
        filename = self.processor.combine_with_name([test_file, test_file], "pi_photobooth/tests/imgs/results/result-wide.jpg", Directions.HORIZONTAL)
        result_file = Image.open(filename)
        self.assertEquals(test_file_img.size[1], result_file.size[1], "Height should be same")
        self.assertEquals(2 * test_file_img.size[0], result_file.size[0], "Expected Width to be twice as tall")

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


if __name__ == '__main__':
    unittest.main()

    #PreviewTest().testPreview()
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
    #boot = booth.PhotoBooth()
    #boot.takePictures(2)