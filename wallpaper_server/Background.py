import io

from PIL import Image
import numpy

from wallpaper_server import DEFAULT_RESOLUTION

class Background:
    def __init__(self, image_path,
                 resolution=DEFAULT_RESOLUTION):

        self.image_format = image_path.split('.')[-1]

        resolution_split = resolution.split("x")
        self.x_res, self.y_res = map(int, resolution_split)
        self.size = (self.x_res, self.y_res)

        self.img = Image.open(image_path)
        self.image_mime_format = self.img.format

        self._resize_image()
        self._add_border()


    def _resize_image(self):
        # Coping with images of a different size
        if self.img.size[0] != self.x_res or self.img.size[1] != self.y_res:
            # Resizing
            self.img.thumbnail(self.size, Image.ANTIALIAS)

    def _add_border(self):
        # finding the median background colour
        img_data = numpy.asarray(self.img)
        background_colours = tuple(
            numpy.median(img_data, axis=(0, 1))
                 .astype(numpy.uint8)
        )
        # Centering the image, and adding a border
        background = Image.new('RGB', self.size, background_colours, )
        background.paste(self.img,
                         ((self.x_res - self.img.size[0]) // 2, (self.y_res - self.img.size[1]) // 2)
                         )

        self.img = background

    def get_image(self):
        image_format = self.image_format if self.image_format.lower() != 'jpg' else 'jpeg'

        image_data = io.BytesIO()
        self.img.save(image_data, format=image_format)
        image_data.seek(0)

        return image_data, self.image_mime_format
