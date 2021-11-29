import tempfile
from PIL import Image

SECRET_KEY = ""
# ALBUM
IMG = "imgs"
THUMB_SIZE = 175
# best quality for downscale : https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
THUMB_ALGO = Image.LANCZOS
THUMB = tempfile.gettempdir()
MAX_AGE = 86400

CONTACTS = [
    {
        "titre": "",
        "nom": "",
        "email": "",
        "telephone": "",
    }
]

PASSWORD = ""
