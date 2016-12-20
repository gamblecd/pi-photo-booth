import facebook_uploader as fb


class FacebookTest:

    def __init__(self):
        pass

    def testLogin(self):
        fb.FacebookUploader()

    def testEvents(self):
        uploader = fb.FacebookUploader()
        id = uploader.event("Christmas Party")
        print(id)



if __name__ == "__main__":
    testee = FacebookTest()
    testee.testEvents()
    #CameraTest().testOpenViewFinder()
    #CameraTest().testAutoFocusToLivePreviewToCapture()
