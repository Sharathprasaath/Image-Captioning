import cv2
import base64
import numpy as np

import matplotlib.pyplot as plt

class Helper():
    
    @staticmethod
    def bytes_2_img(bytes):
        # Encode -> Base64 -> NpBuffer -> CV2
        img = base64.b64decode(bytes.encode("utf-8"))
        # print(img)
        img = np.frombuffer(img, dtype=np.uint8)
        # print(len(img))
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        # print(img)

        return img
    
    @staticmethod
    def img_2_bytes(img):
        # Img -> CV2 Encode -> Base64 -> Decode
        bytes = cv2.imencode('.png', img)[1].tobytes()
        bytes = base64.b64encode(bytes)
        bytes = bytes.decode('utf-8')

        return bytes