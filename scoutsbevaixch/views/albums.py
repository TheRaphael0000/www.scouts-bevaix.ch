from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from django.core.paginator import Paginator, EmptyPage
from PIL import Image, ImageOps, UnidentifiedImageError

import os


IMG = "imgs"
THUMB_SIZE = 200


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
        l.append({"name": name, "cover": cover})

    context = {
        "albums": l,
    }

    return render(request, "albums.html", context=context)


def album(request, name):
    images = os.listdir(os.path.join(IMG, name))

    context = {
        "name": name,
        "images": images,
    }

    return render(request, "albums_name.html", context=context)


def image(request, album, name):
    return get_image(request, album, name, False)


def thumbnail(request, album, name):
    return get_image(request, album, name, True)


def get_image(request, album, name, is_thumbail=False):
    path = os.path.join(IMG, album, name)

    try:
        im = Image.open(path)
    except (FileNotFoundError, UnidentifiedImageError) as e:
        return HttpResponseNotFound(render(request, "404.html"))

    format = im.format
    response = HttpResponse(content_type=f"image/{format}")
    if is_thumbail:
        im = ImageOps.fit(im, (THUMB_SIZE, THUMB_SIZE), Image.ANTIALIAS)
    im.save(response, format)

    return response
