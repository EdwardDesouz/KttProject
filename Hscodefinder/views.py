from typing import Any
from django.shortcuts import render,redirect
from KttApp.views import SqlDb
from django.views import View
from datetime import *
import pandas as pd
from KttApp.models import *
from django.http import JsonResponse 
from django.http import HttpResponse
import json
import re
from PyPDF2 import PdfReader
from django.urls import reverse


def hscodelist(request):

    return render (request,'hscode/hscodefinder.html')

