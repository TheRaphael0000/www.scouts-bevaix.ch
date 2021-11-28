import tempfile
import hashlib
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, FileResponse

from PIL import Image, ImageOps, UnidentifiedImageError


IMG = "imgs"
THUMB_SIZE = 175
# best quality for downscale : https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
THUMB_ALGO = Image.LANCZOS
THUMB = tempfile.gettempdir()


def can_view_album(request, name):
    return name[0] != "_" or request.session["auth"]


def albums(request, name=None):
    if name is None:
        return albums_list(request)
    else:
        return album(request, name)


def albums_list(request):
    _albums = os.listdir(IMG)
    covers = [os.listdir(os.path.join(IMG, album))[0] for album in _albums]

    l = []
    for name, cover in zip(_albums, covers):
        if can_view_album(request, name):
            l.append({"name": name, "cover": cover})
    l.sort(key=lambda x: x["name"])
    context = {
        "albums": l,
    }

    return render(request, "albums.html", context=context)


def album(request, name):
    try:
        if not can_view_album(request, name):
            raise FileNotFoundError

        images = os.listdir(os.path.join(IMG, name))
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "404.html"))

    context = {
        "name": name,
        "images": images,
    }

    return render(request, "albums_name.html", context=context)


def image(request, album, name):
    try:
        if not can_view_album(request, album):
            raise FileNotFoundError

        return image_to_response(get_image(album, name))
    except (FileNotFoundError, UnidentifiedImageError) as e:
        return HttpResponseNotFound(render(request, "404.html"))


def thumbnail(request, album, name):
    try:
        if not can_view_album(request, album):
            raise FileNotFoundError

        return image_to_response(get_thumbnail(album, name))
    except (FileNotFoundError, UnidentifiedImageError) as e:
        return HttpResponseNotFound(render(request, "404.html"))


def image_to_response(im):
    format = im.format
    response = HttpResponse(content_type=f"image/{format}")
    response["Cache-Control"] = "public, max-age=3600"
    im.save(response, format)
    return response


def get_image_path(album, name):
    return os.path.join(IMG, album, name)


def get_thumbnail_path(album, name):
    thumbnail_filename = hashlib.md5(
        (album + name).encode("utf-8")).hexdigest()
    return os.path.join(THUMB, thumbnail_filename)


def get_thumbnail(album, name):
    thumbnail_path = get_thumbnail_path(album, name)
    if os.path.exists(thumbnail_path):
        im = Image.open(thumbnail_path)
        return im
    im = get_image(album, name)
    format = im.format
    im = ImageOps.fit(im, (THUMB_SIZE, THUMB_SIZE), THUMB_ALGO)
    try:
        im.save(thumbnail_path, format=format)
        # restore format after image fit
        im.format = format
    except ValueError:
        pass
    return im


def get_image(album, name):
    image_path = get_image_path(album, name)
    return Image.open(image_path)
