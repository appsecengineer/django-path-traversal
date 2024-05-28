# image_app/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import mimetypes
import os


def home(request):
    return render(request, 'home.html')

def fetch_image(request):
    param = request.GET.get('filename')
    file_path = os.path.join(settings.BASE_DIR, "image_app", "static", "images", param)

    f = open(file_path, 'rb')
    return HttpResponse(content=f, content_type=get_content_type(file_path))

def get_content_type(file_path):
    # Use mimetypes module to determine the MIME type based on file extension
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'text/plain'
