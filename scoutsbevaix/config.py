import tempfile
from pathlib import Path
from PIL import Image
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

# Django Settings
DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = secrets.token_urlsafe(30)
ALLOWED_HOSTS = ["*"]

# ALBUM
IMG = Path("imgs")
THUMB_SIZE = 175
# best quality for downscale : https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
THUMB_ALGO = Image.LANCZOS
THUMB = Path(tempfile.gettempdir())
MAX_AGE = 86400

CONTACTS = [
    {
        "titre": "Responsable de Groupe et de Troupe",
        "nom": "Colibri, Kim Huguenin",
        "email": "contact@scouts-bevaix.ch",
        "telephone": "079 572 25 60",
    },
    {
        "titre": "Responsable de Meute",
        "nom": "Gerbille, Matteo Matulli",
        "telephone": "079 443 77 60",
    },
    {
        "titre": "Gérance locations",
        "nom": "Catherine Béguin",
        "email": "locations@scouts-bevaix.ch",
    },
    {
        "titre": "Webmaster",
        "nom": "Koala, Raphaël Margueron",
        "telephone": "079 471 28 64",
    },
]

GOOGLE_CREDS = "google_token.json"

TELEGRAM_ALLOWED_USERS = [
    {
        "chatId": "675387676",
        "name": "Raphaël"
    },
    {
        "chatId": "7151448698",
        "name": "Nathalie"
    }
]