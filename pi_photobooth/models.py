import gphoto2 as gp


class PhotoBoothCamera:

    def __init__(self, context=gp.Context()):
        self.context = context
        self.set_camera(gp.Camera())

    def set_camera(self, camera):
        self.camera = camera
        self.initial_config = camera.get_config(self.context)

    def set_context(self, context):
        self.context = context

    def get_config(self):
        return CameraConfig(self.camera.get_config(self.context))

    def _set_config_value(self, name, value):
        config = self.get_config()
        config.set(name, value)
        self.camera.set_config(config.get_root(), self.context)

    def _set_viewfinder(self, value):
        self._set_config_value("viewfinder", value)

    def image_format(self):
        return self.get_config().get("imageformat").value()

    def capture(self):
        return self.camera.capture(gp.GP_CAPTURE_IMAGE, self.context)

    def get_image(self, file):
        return self.camera.file_get(file.folder, file.name, gp.GP_FILE_TYPE_NORMAL, self.context)

    def generate_preview(self):
        while True:
            yield self.camera.capture_preview(self.context)

    def capture_preview(self):
        return self.camera.capture_preview(self.context)

    def capture_movie(self):
        return self.camera.capture(gp.GP_CAPTURE_MOVIE, self.context)

    def focus(self, distance=None):
        if distance is None:
            #Turn mirror down, set autofocus
            self.mirror_down()
            self._set_config_value("autofocusdrive", 1)
            # Focus will happen before shoot
        else:
            #Need to set preview mode of not available
            config = self.get_config()
            config.set("manualfocusdrive", distance)

    def mirror_up(self):
        self._set_viewfinder(1)

    def mirror_down(self):
        self._set_viewfinder(0)

    def destroy(self):
        self.camera.exit(self.context)


class CameraConfig:

    def __init__(self, config):
        self.config = config

    def get_root(self):
        return self.config

    def get(self, name):
        return CameraConfig(self.config.get_child_by_name(name))

    def set(self, name, value):
        self.config.get_child_by_name(name).set_value(value)

    def value(self):
        return self.config.get_value()