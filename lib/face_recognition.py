import face_recognition as fr
import cv2
from PIL import Image
import base64
import io
import numpy as np


def image_to_ndarray(image_base64):
    im_bytes = base64.b64decode(image_base64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    known_encoding = fr.face_encodings(img)

    if not known_encoding:
        return None
    return list(known_encoding[0])
