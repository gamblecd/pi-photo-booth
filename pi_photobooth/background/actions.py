from .social.facebook_uploader import FacebookUploader
from .image import ImageProcessor, Directions
class Actions:

    def __init__(self, uploader=FacebookUploader(), image_proc=ImageProcessor()):
        self.fb = uploader
        self.image_processor = image_proc
        print("Actions Loaded")

    def define_name(self, img_arr):
        if not img_arr:
            return ""
        return "{}_photoBooth.jpg".format(img_arr[0].split(".")[0])

    def combine_and_upload_to_event(self, img_arr, event_name):
        if not img_arr:
            return ""
        print("Grabbing Event Id")
        event_id = self.fb.event(event_name);

        print("Processing Image")
        image_name = self.define_name(img_arr)
        new_img_name = self.image_processor.combine(img_arr, image_name, Directions.VERTICAL)

        print("Uploading new Image to Event")
        post_id = self.fb.upload_to_event(new_img_name, event_id).get("post_id")
        print("Uploaded...")
        return post_id