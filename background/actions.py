import social
from social import facebook_uploader as fu
import image as img_proc
class Actions:
    def __init__(self):
        self.fb = fu.FacebookUploader()
        self.image_processor = img_proc.ImageProcessor();
        print("Actions Loaded")
    
    def combineAndUploadToEvent(self, img_arr, eventName):
        print("Grabbing Event Id")
        eventId = self.fb.findEvent(eventName);

        print("Processing Image")
        newImgName = self.image_processor.combine(img_arr);

        print("Uploading new Image to Event")
        return self.fb.uploadToEvent(newImgName, eventId).get("post_id")


if __name__ == "__main__":
    testee = Actions()
    testee.combineAndUploadToEvent(["test/test1.jpeg", "test/test.jpeg", "test/test.jpeg"], "TestEventForUpload")
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
