"""Main Test File for Photo Booth background actions

Usage:
    

"""
from unittest import TestCase
from mock import patch, Mock, MagicMock
import logging
import os

from pi_photobooth.background.image import ImageProcessor, Directions
from pi_photobooth.background.actions import Actions
from pi_photobooth.background.social.facebook_uploader import FacebookUploader

from PIL import Image


@patch("pi_photobooth.background.actions.ImageProcessor")
@patch("pi_photobooth.background.actions.FacebookUploader")
class TestActions(TestCase):

    def setUp(self):
        self.actions = Actions()

    def tearDown(self):
        pass

    def test_define_name_empty_list(self, uploader, processor_fn):
        expected = ""
        self.assertEquals(expected, self.actions.define_name([]))

    def test_define_name_single_list(self, uploader, processor_fn):
        expected = "test_photoBooth.jpg"
        self.assertEquals(expected, self.actions.define_name(["test"]))

    def test_define_name_triple_list(self, uploader, processor_fn):
        expected = "test_photoBooth.jpg"
        self.assertEquals(expected, self.actions.define_name(["test", "test2", "test3"]))

    def test_combine_and_upload_to_event_empty(self, uploader, processor):
        self.assertEquals("", self.actions.combine_and_upload_to_event([],"anything"))

    def test_combine_and_upload_to_event_not_empty(self, uploader, processor):
        event_nm = "Test Event Name"
        new_img_name = "Image Name"
        input_data = ["testName", "test2", "test3"]

        def assert_event(event_name):
            self.assertEquals(event_nm, event_name)
            return "event_id"
        uploader.return_value.event = Mock(side_effect=assert_event)

        def assert_combine(img_arr, name, directions):
            self.assertListEqual(input_data, img_arr)
            self.assertEquals("testName_photoBooth.jpg", name)
            self.assertEquals(Directions.VERTICAL, directions)
            return new_img_name
        processor.return_value.combine = Mock(side_effect=assert_combine)
        def assert_upload(img_name, event_id):
            self.assertEquals(new_img_name, img_name)
            self.assertEquals("event_id", event_id)
            return {"id": "id", "post_id": "post_id_data"}
        uploader.return_value.upload_to_event = Mock(side_effect=assert_upload)
        expected = "post_id_data"
        action = Actions(uploader=uploader(), image_proc=processor())
        self.assertEquals(expected, action.combine_and_upload_to_event(input_data, event_nm))


class TestImageProcessor(TestCase):

    def setUp(self):
        self.processor = ImageProcessor()
        if not os.path.exists("pi_photobooth/tests/imgs/results"):
            os.mkdir("pi_photobooth/tests/imgs/results")

    def tearDown(self):
        if os.path.exists("pi_photobooth/tests/imgs/results"):
            for filename in os.listdir("pi_photobooth/tests/imgs/results"):
               os.remove("pi_photobooth/tests/imgs/results/{}".format(filename))
            os.rmdir("pi_photobooth/tests/imgs/results")

    def test_empty(self):
        with self.assertRaises(IndexError):
            self.processor.combine_with_name([], "")

    def test_filename(self):
        expected_filename = "pi_photobooth/tests/imgs/results/test_filename.jpg"
        filename = self.processor.combine_with_name(
            ["pi_photobooth/tests/imgs/test.jpg"],
            expected_filename)
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

class TestFacebookUploader(TestCase):

    def setUp(self):
        self.uploader = FacebookUploader()
        pass

    def tearDown(self):
        pass

    @patch("facebook.GraphAPI.get_object")
    def test_get_events(self, get_object):
        get_object.return_value = []
        self.assertFalse(self.uploader.get_events())

    @patch("facebook.GraphAPI.get_object")
    def test_get_events_called_twice(self, get_object):
        get_object.return_value = []
        self.assertFalse(self.uploader.get_events())
        self.uploader.get_events()
        self.assertEquals(1, len(get_object.mock_calls))
        
    @patch("facebook.GraphAPI.get_object")
    def test_find_event_missing_event(self, get_object):
        get_object.return_value = {"data":[{"id": "name", "name":"Test"},
            {"id": "name", "name":"Test1"}]}
        self.assertIsNone(self.uploader.event("Test2"))

    @patch("facebook.GraphAPI.get_object")
    def test_find_event(self, get_object):
        get_object.return_value = {"data":[{"id": "name", "name":"Test"},
            {"id": "name", "name":"Test1"}]}
        self.assertEquals("name", self.uploader.event("Test"))

    @patch("facebook.GraphAPI.put_photo")
    def test_upload_to_event(self, put_photo):
        imageName = "pi_photobooth/tests/imgs/test.jpg"
        expected = {"id":"id", "post_id":"data"}
        def return_post_id(image=None, album_path=""):
            self.assertEquals("eventId/photos", album_path)
            f = open(imageName)
            f.seek(0, os.SEEK_END)
            image.seek(0, os.SEEK_END)
            self.assertEquals(f.tell(), image.tell())
            return expected
        put_photo.side_effect = return_post_id
        self.assertEquals(expected, self.uploader.upload_to_event("pi_photobooth/tests/imgs/test.jpg", "eventId"))


if __name__ == '__main__':
    unittest.main()