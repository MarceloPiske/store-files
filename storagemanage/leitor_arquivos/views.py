from django.shortcuts import render
from django.http import HttpResponse
from .models import DiretoriosS3
from pathlib import Path
from django.core.files import File
# Create your views here.

def index(request):
    arquivo = DiretoriosS3.objects.get(pk=2).arquivo.path
    
    print(arquivo)
    DiretoriosS3.objects.get(pk=2).arquivo.path
    #sarquivo.save()
    return HttpResponse("tamo indo ai")
