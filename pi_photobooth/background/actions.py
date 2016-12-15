import social
from social import facebook_uploader as fu
from image import ImageProcessor, Directions
class Actions:
    def __init__(self):
        self.fb = fu.FacebookUploader()
        self.image_processor = ImageProcessor();
        print("Actions Loaded")
    
    def combine_and_upload_to_event(self, img_arr, eventName):
        print("Grabbing Event Id")
        eventId = self.fb.findEvent(eventName);

        print("Processing Image")
        imageName = "{}_photoBooth.jpg".format(img_arr[0].split(".")[0])
        newImgName = self.image_processor.combine(img_arr, imageName, Directions.VERTICAL)

        print("Uploading new Image to Event")
        return self.fb.uploadToEvent(newImgName, eventId).get("post_id")


if __name__ == "__main__":
    testee = Actions()
    testee.combine_and_upload_to_event(["test/test1.jpeg", "test/test.jpeg", "test/test.jpeg"], "TestEventForUpload")
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
