from datetime import datetime
from django.forms import SlugField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import DiretoriosS3
from pathlib import Path
from django.views.generic import View
import os
from django.conf import settings
from django.core.files import File
import json
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

def pega_pasta(diretorio):
    pasta = ''
    if diretorio:
        if '/' in diretorio:
            pasta = diretorio.split('/')[len(diretorio.split('/'))-1]
        else:
            pasta = diretorio

    return pasta

def arquivos_subpastas(pasta):
    lista_desenho_diretorio = []
    for diretorio, subpastas, arquivos in os.walk('media'):

        nome_pasta = pega_pasta(str(diretorio))
        print(nome_pasta)
        if str(nome_pasta) == str(pasta):
            diretorio_pasta = {}
            arquivo_pasta = {}

            arquivo_pasta['subpastas'] = subpastas
            arquivo_pasta['nome_pasta'] = nome_pasta
            arquivo_pasta['arquivos'] = arquivos
            diretorio_pasta['diretorio'] = diretorio
            diretorio_pasta['pasta'] = arquivo_pasta
            
            lista_desenho_diretorio.append(diretorio_pasta)
            break
    return lista_desenho_diretorio

class ASGIGerenciadorArquivos(APIView):
    def post(self, request, format=None):
        diretorio = f"media/{request.POST.get('diretorio')}"
        #criar nova pasta
        if not os.path.isdir(diretorio):
            os.makedirs(diretorio)
        return Response(None)

    def patch(self, request, format=None):
        
        pasta = request.POST.get('data')
        lista_desenho_diretorio = arquivos_subpastas(pasta)
        
        return Response(lista_desenho_diretorio)

    def delete(self, request, format=None):
        
        dados = json.loads(request.POST.get('data'))
        pasta = dados.get('pasta')
        arquivo = dados.get('arquivo')
        flag = dados.get('flag')

        if flag == 1:
            arquivo_encontrado = DiretoriosS3.objects.get(nome=arquivo, pasta=pasta)

            #deletar diretorio
            arquivo_excluido = os.path.join(f"{arquivo_encontrado.arquivo.name}")
            os.remove(arquivo_excluido) 
            arquivo_encontrado.delete()
        else:
            #Deltar arquivos
            diretorio_excluir = os.path.join(f"{pasta}/{arquivo}")
            os.rmdir(diretorio_excluir)
            
        return Response(None)

class GerenciarArquivos(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, *args, **kwargs):
        pasta = "media"

        lista_desenho_diretorio = arquivos_subpastas(pasta)
        
        df = {
            "pasta": 'media',
            "arquivos": lista_desenho_diretorio
        }

        return render(self.request, "index.html", df)

    def post(self, *args, **kwargs):
        #root_dir = 'media/'
        diretorio = self.request.POST.get('diretorio')
        print(f"seu diretorio é: {diretorio}")
        pasta = diretorio.split('/')[len(diretorio.split('/'))-2]
        print(f"sua pasta é: {pasta}")
        arquivo_recebido = self.request.FILES.get('arquivos')
        nome = str(arquivo_recebido)


        if not DiretoriosS3.objects.filter(nome=nome, pasta=pasta).exists():
            DiretoriosS3.objects.create(nome=nome, arquivo=arquivo_recebido, pasta=pasta)
        else:
            pass

        #criar diretório
        if not os.path.isdir(diretorio):
            os.makedirs(diretorio)
        arquivo = DiretoriosS3.objects.get(nome=nome, pasta=pasta)

        path = arquivo.arquivo.path
        path_inicial = path
        arquivo.arquivo.name = f'{diretorio}{nome}'
        novo_path = arquivo.arquivo.name
        
        # Renomear diretorio do arquivo
        os.rename(path_inicial, novo_path)
        
        #excluir diretorios temporarios
        diretorio_excluir = os.path.join(f"media/temp")
        os.rmdir(diretorio_excluir)

        #salva novo local no banco
        arquivo.save()
        print(arquivo.arquivo.path)

        return redirect('/')
