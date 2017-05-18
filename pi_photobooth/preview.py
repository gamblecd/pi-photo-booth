import io

from PIL import Image

import time

'''
Creates a image generator and converts the PIL images to ByteIO.
'''
class Previewer:

    def producer(self, frame_generator):
        # Grab Preview
        camera_file = next(frame_generator)
        while True:
            file_data = camera_file.get_data_and_size()
            # display image
            yield self.produce_frame(file_data)
            camera_file = next(frame_generator)

    def produce_frame(self, file_data):
        return io.BytesIO(file_data)
