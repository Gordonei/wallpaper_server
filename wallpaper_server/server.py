import os
import json

from flask import Flask, request, jsonify, send_file

from wallpaper_server import DEFAULT_RESOLUTION, DEFAULT_BACKGROUND_DIR
from wallpaper_server.Background import Background

app = Flask(__name__)

@app.route('/')
def serve_root():
    resolution = DEFAULT_RESOLUTION
    if 'resolution' in request.args:
        resolution = request.args.get('resolution')

    list_backgrounds = ["_".join((resolution, background))
                        for background in os.listdir(DEFAULT_BACKGROUND_DIR)]

    backgrounds_dict = {'backgrounds': list_backgrounds}
    backgrounds_json = json.dumps(backgrounds_dict)

    return backgrounds_json


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message

        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response


@app.route('/backgrounds/<background_name>')
def serve_background(background_name):
    split_background_name = background_name.split("_")
    if len(split_background_name) < 2:
        raise InvalidUsage('Whoops - the resolution should prepend the image name, e.g. 800x600_foo.jpg')

    resolution = split_background_name[0]
    image_name = "_".join(split_background_name[1:])

    image_path = os.path.join(DEFAULT_BACKGROUND_DIR, image_name)
    abs_image_path = os.path.abspath(image_path)
    if os.path.commonpath([abs_image_path, DEFAULT_BACKGROUND_DIR]) != DEFAULT_BACKGROUND_DIR:
        raise InvalidUsage('Sorry, not allowed.', status_code=403)

    if not os.path.exists(image_path) or os.path.isdir(image_path):
        raise InvalidUsage('Whoops - the image file "{}" does not exist'.format(image_name))

    # Processing the image into a background
    background = Background(image_path, resolution)
    image_data, image_format = background.get_image()

    return send_file(
        image_data, mimetype=image_format
    )


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

