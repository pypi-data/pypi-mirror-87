#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - module shared

Constantes e funções privadas usadas por mais de um módulo
"""

import os
from pathlib import Path
from time import time
from subprocess import run
from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED

# não troque as constantes das PNADS...
PNAD = 'pnad'
PNADCA = 'pnadc_anual'
PNADCT = 'pnadc_trimestral'

# microdados no IBGE
URL = 'ftp.ibge.gov.br'
FLDRS = {PNAD: ('Trabalho_e_Rendimento',
                'Pesquisa_Nacional_por_Amostra_de_Domicilios_anual',
                'microdados'),
         PNADCA: ('Trabalho_e_Rendimento',
                  'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                  'Anual', 'Microdados'),
         PNADCT: ('Trabalho_e_Rendimento',
                  'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                  'Trimestral', 'Microdados')}
ALL = (PNAD, PNADCA, PNADCT)

# pastas especificas no IBGE
TRIDOCS = 'Documentacao'
CA_DOCS = 'Documentacao'
CA_DATA = 'Dados'
CA_VIS = 'Visita'
CA_TRI = 'Trimestre'

# nome para pastas das cópias locais e paineis
ORI = 'originais'
META = 'metadados'
MICRO = 'microdados'
REGPES = 'pessoas'
REGIND = 'individuos'
REGPID = 'chaves'

# chaves dos dicionários de variáveis json
_VPART = 'parte'  # parte do registro: identificação e controle etc.
_VDESC = 'desc'  # description
_VPER = 'periodo'  # period
_VPOS = 'colunas'  # position in fixed width microdata file
_VSIZE = 'bytes'  # bytes needed to store the variable
_VCAT = 'valores'  # content - categories
_VQUES = 'quesito'  # question number if from the questionnaire
_MISS = 'vazio'  # key for "não aplicável" in _VCAT


# ------------------------------------
# funções usadas por mais de um módulo
# ------------------------------------


def __time__(start):
    # string com o tempo formatado desde start
    end = time()
    hours = int((end - start) / 3600)
    mins = int(((end - start) - hours * 3600) / 60)
    segs = int((end - start) - hours * 3600 - mins * 60)
    mils = int(((end - start) - int(end - start)) * 1000)
    if hours:
        result = f'{hours:3.0f}h{mins:3.0f}m{segs:3.0f}s'
    elif mins:
        result = f'{mins:3.0f}m{segs:3.0f}s'
    elif segs:
        result = f'{segs:3.0f}s'
    else:
        result = f'{mils:3.0f}ms'
    return result


def __nomecsv__(nome, pnad):
    # nome do arquivo csv a partir do original e tipo de pnad
    if pnad == PNAD:
        pass
    if pnad == PNADCA:
        stub = '.'.join(nome[:-4].split('_')[1:3])
    if pnad == PNADCT:
        stub = nome[:-4].split('_')
        stub = f'{stub[1][2:]}.{stub[1][1]}'
    nome = ".".join(pnad.split('_'))
    nome = f'microdados.{nome}.{stub}.csv'
    return nome


def __is_mirror_file__(mirrorfile):
    # verifica se arquivo zip é um mirror válido
    valid = True
    if not Path(mirrorfile).is_file():
        valid = False
    elif not is_zipfile(mirrorfile):
        valid = False
    if valid:
        with ZipFile(mirrorfile) as src:
            items = src.namelist()
        if not [item for item in items
                if ORI in item and any(pnad in item for pnad in ALL)]:
            valid = False
    if not valid:
        print(f'{mirrorfile} inválido')
    return valid


def __delete__(archive, delete):
    # zipfile é horrível para deletar, usar zip ou 7zip se disponíveis
    def __withzipfile__():
        os.rename(archive, archive + '.old')
        with ZipFile(archive + '.old') as src:
            with ZipFile(archive, 'w', ZIP_DEFLATED) as tgt:
                for file in src.namelist():
                    if file not in delete:
                        tgt.writestr(file, src.read(file))
        os.remove(archive + '.old')
    start = time()
    print(' - Removendo arquivos desatualizados', end='...', flush=True)
    try:
        run(('zip', '-d', archive, *delete),
            capture_output=True, check=True)
    except FileNotFoundError:
        if os.name == 'posix':
            u7z = '7za'
        else:
            u7z = '7z'
        try:
            run((u7z, 'd', archive, *delete),
                capture_output=True, check=True)
        except FileNotFoundError:
            print(' (zipfile) ', end='', flush=True)
            __withzipfile__()
    print(f'OK! {__time__(start)}')
