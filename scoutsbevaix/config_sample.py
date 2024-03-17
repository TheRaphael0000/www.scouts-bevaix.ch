import tempfile
from pathlib import Path
from PIL import Image

# Django Settings
DEBUG = True
SECRET_KEY = ""
ALLOWED_HOSTS = []

# ALBUM
IMG = Path("imgs")
THUMB_SIZE = 175
# best quality for downscale : https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
THUMB_ALGO = Image.LANCZOS
THUMB = Path(tempfile.gettempdir())
MAX_AGE = 86400

CONTACTS = [
    {
        "titre": "",
        "nom": "",
        "email": "",
        "telephone": "",
    }
]

CALENDAR_LOCATIONS = ""
CALENDAR_SEANCES = ""
CALENDAR_DEMANDE = ""
GOOGLE_CREDS = ""

TELEGRAM_API_KEY = ""
TELEGRAM_ALLOWED_USERS = [
    {
        "chatId": "",
        "name": ""
    }
]

PASSWORD = ""
