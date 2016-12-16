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


