from django.shortcuts import render, HttpResponse, redirect
from django.template.response import TemplateResponse
from django.conf import settings

import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

import os
import getpass
import requests

# import matlab.engine
# import matlab

logger = logging.getLogger()


# Create your views here.
def index(request):
    if request.method == "GET":
        ### TODO: BUG HERE ###
        args = {"PREDICTMOD_INSTANCE": "predictmod/upload/"}
        return TemplateResponse(request, "index.html", args)
    if request.method == "POST":
        try:
            # files = request.FILES.get("files", None)
            # if not files:
            #     return HttpResponse("no files for upload!")
            # try:
            #     with open(os.path.join("/hostfs", files.name), 'wb+') as fp:
            #         [fp.write(c) for c in files.chunks()]
            #     fp.close()
            # except Exception as e:
            #     logger.error(f"Caught exception {e}!")
            #     return HttpResponse(f"User: {getpass.getuser()}")
            # eng = matlab.engine.start_matlab()
            # MATLAB_FILE = f'{settings.BASE_DIR}/predictmod/{files.name}'
            # eng.cd(f'{settings.BASE_DIR}/predictmod/', nargout=0)
            # eng.editted_single_predict(MATLAB_FILE, nargout=0)
            # result = eng.editted_single_predict()
            logger.debug("+" * 80)
            logger.debug(f"Request files: {request.FILES}")
            logger.debug("+" * 80)
            result = requests.post(
                f"http://host.docker.internal:4243/", files=request.FILES
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
