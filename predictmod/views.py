from django.shortcuts import render, HttpResponse, redirect
import os
import matlab.engine 
import matlab


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        files = request.FILES.get("files", None)
        if not files:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join("predictmod/upload/", files.name), 'wb+')
        for chunk in files.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse("Done!")

