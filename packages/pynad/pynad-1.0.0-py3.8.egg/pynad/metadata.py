#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - method metadata

Organiza os metadados originais em uma só pasta
e cria versões dos dicionários de variáveis em json
"""


import json
import re
from io import BytesIO
from pathlib import Path, PurePosixPath as PPath
from zipfile import ZipFile, ZIP_DEFLATED
from tablib import Dataset
from .shared import PNAD, PNADCA, PNADCT, ORI, META, TRIDOCS
from .shared import CA_VIS, CA_TRI, CA_DOCS, CA_DATA
from .shared import __is_mirror_file__, __delete__
from .shared import _VPART, _VDESC, _VPER, _VPOS
from .shared import _VSIZE, _VCAT, _VQUES, _MISS


def metadata(mirrorfile):
    """
    Extrai e organiza os metadados.

    Restrito ao necessário para ler e rotular as variáveis e categorias dos
    arquivos de microdados - não inclui
    deflatores, códigos de ocupação, documentos de metodologia etc.
    """
    # aceitar um Path como argumento e verificar
    if isinstance(mirrorfile, Path):
        mirrorfile = str(mirrorfile)
    if not __is_mirror_file__(mirrorfile):
        return
    with ZipFile(mirrorfile, 'a', ZIP_DEFLATED) as archive:
        files = archive.namelist()

    # verificar os dados originais no mirrorfile
    # pode ter qualquer combo de PNAD PNADCT e PNADCA
    metadados = {}
    if any(PNAD == Path(file).parts[1] for file in files):
        metadados[PNAD] = []
    if any(PNADCA == Path(file).parts[1] for file in files):
        metadados[PNADCA] = __metadata_pnadc_anual__(mirrorfile)
    if any(PNADCT == Path(file).parts[1] for file in files):
        metadados[PNADCT] = __metadata_pnadc_trimestral__(mirrorfile)

    if not __atualizados__(mirrorfile, files, metadados):
        __write_metadata__(mirrorfile, metadados)
        archive.close()
    print('Metadados atualizados')


def __atualizados__(mirrorfile, files, metadados):
    # carregar microdados json e verificar mudanças em item[0] e [1]
    metanew = {}
    curmetafiles = [Path(item).name for item in files
                    if Path(item).parts[0] == META
                    and 'json' not in item]
    for pnad in metadados:
        metanew[pnad] = [item for item in metadados[pnad]
                         if Path(item[1]).name not in curmetafiles]
    if all(metanew[pnad] == [] for pnad in metadados):
        return True

    # se houver qualquer atualização, os arquivos
    # microdados*.json terão que ser removidos do mirrorfile
    # isto demora, e aqui, como os metadados atualizados estão
    # todos carregados, apagar todos os arquivos de metadados
    # existentes é mais rápido do que apagar poucos
    curmetafiles = [file for file in files if Path(file).parts[0] == META]
    if curmetafiles:
        print('Atualizando metadados')
        __delete__(mirrorfile, curmetafiles)
    return False


def __write_metadata__(mirrorfile, metadados):
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
    for pnad in metadados:
        if pnad == PNAD:
            pass
        if pnad == PNADCA:
            processados = []
            for item in metadados[pnad]:
                target = str(PPath(META, Path(item[1]).name))
                if item[1] not in processados:
                    processados.append(item[1])
                    archive.writestr(target, archive.read(item[1]))
                item[1] = target
                if item[2][0] not in processados:
                    processados.append(item[2][0])
                    archive.writestr(item[2][0], json.dumps(item[2][1]))
                item[2] = item[2][0]
            target = str(PPath(META, 'microdados.pnadc.anual.json'))
            archive.writestr(target, json.dumps(metadados[pnad]))
        if pnad == PNADCT:
            item = metadados[pnad][0]
            item[1] = str(PPath(META, item[1]))
            archive.writestr(item[1], item[2][2].read())
            archive.writestr(item[2][0], json.dumps(item[2][1]))
            for item in metadados[pnad]:
                item[2] = item[2][0]
            target = str(PPath(META, 'microdados.pnadc.trimestral.json'))
            archive.writestr(target, json.dumps(metadados[pnad]))
    archive.close()


def __metadata_pnadc_anual__(mirrorfile):
    """
    Extrai e organiza metadados da pnadc anual.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação

    Em dezembro de 2019 a estrutura de disseminação da pnadc
    anual mudou radicalmente

    Há pastas para:
     - 5 visitas (dicionario por visita e por ano)
     - 4 trimestres (dicionário por trimestre vale para todos os anos)
    """
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
    microdados = __metadata_pnadc_anual_arquivos__(archive.namelist())
    for microdado in microdados:
        # lê o dicionário correspondente
        temp = BytesIO(archive.read(microdado[1]))
        doc = Dataset()
        doc.load(temp.getvalue(), format='xls')
        dicionario = __metadata_pnadc_vars__(doc.export('tsv'))

        # acrescenta à lista
        nome = Path(microdado[0]).name
        if 'trimestre' in nome:
            dicid = nome[:-4].split('_')[2]
        else:
            dicid = '.'.join(nome[:-4].split('_')[1:3])
        target = f'variaveis.pnadc.anual.{dicid}.json'
        microdado[2] = [str(PPath(META, target)), dicionario]
    archive.close()
    return microdados


def __metadata_pnadc_anual_arquivos__(zipitems):
    microdados = []
    for vis in range(1, 6):
        datafolder = PPath(ORI, PNADCA, CA_VIS, f'{CA_VIS}_{vis}', CA_DATA)
        docsfolder = PPath(ORI, PNADCA, CA_VIS, f'{CA_VIS}_{vis}', CA_DOCS)
        docfiles = [item for item in zipitems
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in zipitems
                     if str(datafolder) in item
                     and item.endswith('zip')]
        for doc in docfiles:
            anodoc = Path(doc).name.split('_')[3]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles
                               if (Path(item).name.split('_')[1]
                                   == anodoc and f'{CA_VIS.lower()}{vis}'
                                   in item) or
                               (Path(item).name.split('_')[1]
                                in ('2013', '2014') and
                                f'{CA_VIS.lower()}{vis}'
                                in item and anodoc == '2012')])
    for tri in range(1, 5):
        datafolder = PPath(ORI, PNADCA, CA_TRI, f'{CA_TRI}_{tri}', CA_DATA)
        docsfolder = PPath(ORI, PNADCA, CA_TRI, f'{CA_TRI}_{tri}', CA_DOCS)
        docfiles = [item for item in zipitems
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in zipitems
                     if str(datafolder) in item
                     and item.endswith('zip')]
        if docfiles:
            doc = docfiles[0]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles])
    return microdados


def __metadata_pnadc_trimestral__(mirrorfile):
    """
    Extrai e organiza metadados da pnadc trimestral.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação
    """
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)

    # apenas um dicionário para a pnadc trimestral
    file = [file for file in archive.namelist() if
            all(stub in file for stub
                in (ORI, PNADCT, TRIDOCS, 'Dicionario_e_input'))][0]

    # ler o arquivo zip do dicionário e obter metadados
    buffer = BytesIO(archive.read(file))
    file = ZipFile(buffer)
    diciori = [item for item in file.namelist()
               if 'dicionario' in item][0]
    original = BytesIO(file.read(diciori))

    # le o dicionario com tablib e converte para tsv
    doc = Dataset()
    doc.load(original.getvalue(), format='xls')
    dicionario = __metadata_pnadc_vars__(doc.export('tsv'))
    target = str(PPath(META, 'variaveis.pnadc.trimestral.json'))

    # lista com os arquivos de microdados trimestrais
    microdados = [[item, diciori, [target, dicionario, original], PNADCT]
                  for item in archive.namelist()
                  if PNADCT in item and
                  item.split('/')[2].isnumeric()]
    archive.close()
    return microdados


def __metadata_pnadc_vars__(contents):
    """Depende da estrutura dos dicionários de variáveis."""
    def __clean_label(label):
        label = label.replace('"', '').strip()
        label = label.replace('\n', ' ')
        label = re.sub(' +', ' ', label)
        try:
            label = int(float(label))
        except ValueError:
            pass
        return label

    def __set_bytes(size):
        # dtype bytes para armazenar 9 * colunas da var
        # C signed numeric types
        # 99 - 1 byte
        # 9999 - 2 bytes
        # 999999999 - 4 bytes - float ou int
        # >999999999 - 8 bytes - double ou long
        # pnadc pesos são floats - code 15
        bts = 'ERROR'
        if size <= 2:
            bts = 1
        elif size <= 4:
            bts = 2
        elif size <= 9:
            bts = 4
        elif size <= 14:
            bts = 8
        elif size == 15:
            bts = 15
        return bts

    # meta é o dicionário de variáveis
    meta = {}
    curvar = None

    # seção do questionário
    parte = ''

    # pula linhas de cabeçalho e processa
    rows = contents.split('\r\n')[3:-1]
    for row in rows:

        # line breaks, double spaces e outras coisas
        # limpar campos para processar linhas
        fields = [__clean_label(field) for field in row.split('\t')]

        # linha com informação de "parte" do questionário
        if fields[0] and not fields[1]:
            parte = fields[0].lower()

        # linha principal de variável
        elif all(isinstance(field, int)
                 for field in (fields[0], fields[1])):

            # código (uf, v1008 etc) é a chave em meta
            curvar = fields[2].lower()
            meta[curvar] = {}

            # parte atual
            meta[curvar][_VPART] = parte

            # tuple com:
            # coluna inicial - index em 1
            # coluna final
            # número de colunas
            meta[curvar][_VPOS] = (fields[0],
                                   fields[0] + fields[1] - 1,
                                   fields[1])

            meta[curvar][_VSIZE] = __set_bytes(meta[curvar][_VPOS][2])

            # número do quesito (se tiver)
            meta[curvar][_VQUES] = fields[3]

            # descrição da variável
            meta[curvar][_VDESC] = fields[4].lower()
            if not meta[curvar][_VDESC]:
                meta[curvar][_VDESC] = curvar

            # período
            meta[curvar][_VPER] = fields[7].lower()

            # tem campo 5 - categórica ou info adicional
            meta[curvar][_VCAT] = {}
            especial = (' a ', 'código', 'valor', '130', '01-')
            if (isinstance(fields[5], int)
                    or any(item in fields[5].lower() for item in especial)):
                meta[curvar][_VCAT][fields[5]] = str(fields[6]).lower()
            elif fields[5] or fields[6]:
                meta[curvar][_VCAT] = ', '.join([item.lower()
                                                 for item in fields[5:7]
                                                 if item])

        # linha de categoria
        elif not fields[0] and not fields[1]:
            if not fields[5]:
                fields[5] = _MISS
            try:
                meta[curvar][_VCAT][fields[5]] = fields[6].strip().lower()
            except TypeError:
                print(curvar, fields)
    return meta
