import tempfile
import hashlib
import os
from pathlib import Path
from dataclasses import dataclass

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image, ImageOps, UnidentifiedImageError


@dataclass
class ImageFile():
    album: str
    privacy: str
    name: str

    def check_rights(self, request):
        if self.privacy != "public" and not can_view_private(request):
            raise FileNotFoundError

    def path(self):
        return str(settings.IMG / Path(self.album) / Path(self.privacy) / Path(self.name))



def can_view_private(request):
    return request.session.get("auth", default=False)


def get_valid_images(request, album):
    files = []

    def add_images(privacy):
        path = settings.IMG / Path(album) / Path(privacy)
        try:
            for name in os.listdir(path):
                image_file = ImageFile(album, privacy, name)
                files.append(image_file)
        except FileNotFoundError:
            pass

    add_images("public")
    if can_view_private(request):
        add_images("private")

    files.sort(key=lambda x: x.name)

    if not files:
        raise FileNotFoundError

    for file in files:
        try:
            file.check_rights(request)
            Image.open(file.path()).close()
        except (FileNotFoundError, IsADirectoryError, UnidentifiedImageError, ValueError):
            continue
        yield file


def albums(request):
    try:
        _albums = next(os.walk(settings.IMG))[1]
    except StopIteration:
        _albums = []
    cards = []
    for name in _albums:
        try:
            card = next(get_valid_images(request, name), False)
        except FileNotFoundError:
            continue
        cards.append(card)
    cards.sort(key=lambda x: x.album)
    context = {"cards": cards}
    return render(request, "albums.html", context=context)


def albums_name(request, name):
    try:
        cards = list(get_valid_images(request, name))
        context = {"cards": cards, "name": name }
        return render(request, "albums_name.html", context=context)
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "404.html"))


def image(request, album, privacy, name):
    try:
        image_file = ImageFile(album, privacy, name)
        image_file.check_rights(request)
        image = get_image(image_file)
        return image_to_response(image)
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "404.html"))


def thumbnail(request, album, privacy, name):
    try:
        image_file = ImageFile(album, privacy, name)
        image_file.check_rights(request)
        thumbnail = get_thumbnail(image_file)
        return image_to_response(thumbnail)
    except FileNotFoundError as e:
        return HttpResponseNotFound(render(request, "404.html"))


def image_to_response(im):
    format = im.format
    response = HttpResponse(content_type=f"image/{format}")
    response["Cache-Control"] = f"public, max-age={settings.MAX_AGE}"
    im.save(response, format)
    return response


def get_thumbnail_path(image_file):
    path = (image_file.album + image_file.privacy +
            image_file.name).encode("utf-8")
    thumbnail_filename = hashlib.md5(path).hexdigest()
    return settings.THUMB / Path(thumbnail_filename)


def get_thumbnail(image_file):
    thumbnail_path = get_thumbnail_path(image_file)
    if os.path.exists(thumbnail_path):
        im = Image.open(thumbnail_path)
        return im
    im = get_image(image_file)
    format = im.format
    size = (settings.THUMB_SIZE, settings.THUMB_SIZE)
    im = ImageOps.fit(im, size, settings.THUMB_ALGO)
    try:
        im.save(thumbnail_path, format=format)
        # restore format after image fit
        im.format = format
    except ValueError:
        pass
    return im


def get_image(image_file):
    return Image.open(image_file.path())
