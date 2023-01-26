import json
import logging
import locale
import os

from typing import Union
import gphoto2 as gp
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/camera/capture", responses={200: {"description": "Capture image", "content": {"image/png": ""}}})
def capture_image():
    locale.setlocale(locale.LC_ALL, '')
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)

    camera = gp.Camera()
    camera.init()
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    file_path.rotate(180)

    filename = "temp_image.jpg"
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))

    target = os.path.join('/tmp', filename)

    print('Copying image to', target)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)

    camera.exit()
    return FileResponse(target, media_type="image/png")


@app.get("/camera/summary")
def get_summary():
    camera = gp.Camera()
    camera.init()
    text = camera.get_summary()
    camera.exit()
    # convert text to json
    return {json.dumps(str(text.text))}
