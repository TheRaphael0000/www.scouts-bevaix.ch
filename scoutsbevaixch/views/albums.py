import tempfile
import hashlib
import os

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image, ImageOps, UnidentifiedImageError


def can_view_album(request, name):
    return name[0] != "_" or request.session.get("auth", default=False)


def get_valid_images(album):
    files = os.listdir(os.path.join(settings.IMG, album))
    for f in files:
        path = os.path.join(settings.IMG, album, f)
        try:
            Image.open(path).close()
        except (IsADirectoryError, UnidentifiedImageError, ValueError):
            continue
        yield f


def albums(request, name=None):
    if name is None:
        return albums_list(request)
    else:
        try:
            return album(request, name)
        except FileNotFoundError:
            return HttpResponseNotFound(render(request, "404.html"))


def albums_list(request):
    try:
        _albums = next(os.walk(settings.IMG))[1]
    except StopIteration:
        _albums = []
    _albums_list = []
    for name in _albums:
        cover = next(get_valid_images(name), False)
        if cover and can_view_album(request, name):
            _albums_list.append({"name": name, "cover": cover})
    _albums_list.sort(key=lambda x: x["name"])
    context = {"albums": _albums_list}
    return render(request, "albums.html", context=context)


def album(request, name):
    images = list(get_valid_images(name))
    if not can_view_album(request, name) or len(images) <= 0:
        return HttpResponseNotFound(render(request, "404.html"))
    context = {"name": name, "images": images}
    return render(request, "albums_name.html", context=context)


def image(request, album, name):
    try:
        if not can_view_album(request, album):
            raise FileNotFoundError
        return image_to_response(get_image(album, name))
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "404.html"))


def thumbnail(request, album, name):
    try:
        if not can_view_album(request, album):
            raise FileNotFoundError
        return image_to_response(get_thumbnail(album, name))
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "404.html"))


def image_to_response(im):
    format = im.format
    response = HttpResponse(content_type=f"image/{format}")
    response["Cache-Control"] = f"public, max-age={settings.MAX_AGE}"
    im.save(response, format)
    return response


def get_thumbnail_path(album, name):
    thumbnail_filename = hashlib.md5(
        (album + name).encode("utf-8")).hexdigest()
    return os.path.join(settings.THUMB, thumbnail_filename)


def get_thumbnail(album, name):
    thumbnail_path = get_thumbnail_path(album, name)
    if os.path.exists(thumbnail_path):
        im = Image.open(thumbnail_path)
        return im
    im = get_image(album, name)
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


def get_image(album, name):
    image_path = os.path.join(settings.IMG, album, name)
    return Image.open(image_path)
