from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import DiretoriosS3
from pathlib import Path

import os
from django.conf import settings
from django.core.files import File
# Create your views here.


def index(request):
    
    if request.method == "POST":

        arquivo_recebido = request.FILES.get('arquivos')
        nome = str(arquivo_recebido)
        #print(request.FILES)
        if not DiretoriosS3.objects.filter(nome=nome).exists():
            DiretoriosS3.objects.create(nome=nome, arquivo=arquivo_recebido)
        else:
            return render(request, "index.html")
        arquivo = DiretoriosS3.objects.get(nome=nome)
        path = arquivo.arquivo.path
        arquivo.arquivo.name = f'{datetime.now().date()}/{str(arquivo_recebido)}'
        #print(nome)
        print(path)
        path_inicial = path
        #criar diretório
        if not os.path.isdir(f'./media/{datetime.now().date()}/'):
            os.mkdir(f'./media/{datetime.now().date()}/')
        
        #deletar diretorio
        ##os.rmdir(f'./media/{str(arquivo_recebido)}')
        
        #Deltar aeuivos
        os.remove(f'./media/{str(arquivo_recebido)}')
        novo_path = f'./media/{arquivo.arquivo.name}'
        
        # Renomear diretorio do arquivo
        os.rename(path_inicial, novo_path)
        
        #salva novo local no banco
        arquivo.save()
        print(arquivo.arquivo.path)
        
    return render(request, "index.html")
