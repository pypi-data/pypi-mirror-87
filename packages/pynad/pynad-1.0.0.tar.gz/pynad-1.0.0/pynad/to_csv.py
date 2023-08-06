#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - method to_csv

Converte os microdados originais para CSV
os arquivos microdados.pnadc.{anual|trimestral}.json
contêm a lista de arquivos originais convertidos
e são usados como base para definir as atualizações
"""


import json
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path, PurePosixPath as PPath
from time import time
from zipfile import ZipFile, ZIP_DEFLATED
from .shared import META, MICRO, _VPOS
from .shared import __nomecsv__, __time__, __is_mirror_file__
from .shared import __delete__


def to_csv(mirrorfile, delimiter=','):
    """
    Gera os arquivos de microdados em formato CSV.

    **mirrofile** é o arquivo com a cópia da PNAD

    **delimiter** é opcional, *default* é vírgula
    """
    # aceitar um Path como argumento e verificar requisitos
    if isinstance(mirrorfile, Path):
        mirrorfile = str(mirrorfile)
    if not __is_mirror_file__(mirrorfile):
        return
    if not __check_metadata__(mirrorfile):
        return

    with ZipFile(mirrorfile, 'r', ZIP_DEFLATED) as archive:
        files = archive.namelist()

    if any(MICRO in Path(file).parts[0] for file in files):
        pnads = __select__(mirrorfile)
    else:
        with ZipFile(mirrorfile, 'r', ZIP_DEFLATED) as archive:
            pnads = [[file, json.loads(archive.read(file))] for file in files
                     if all(tag in file for tag in (META,
                                                    'microdados', 'json'))]

    if pnads:
        start0 = time()
        print('Convertendo microdados originais para CSV:')
        archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
        for pnad in pnads:
            for microdado in pnad[1]:
                __convert__(microdado, archive, delimiter)
            metafile = Path(pnad[0]).name
            nome = str(PPath(MICRO, metafile))
            metafile = str(PPath(META, metafile))
            archive.writestr(nome, archive.read(metafile))
        archive.close()
        print(f'Conversão de arquivos em {__time__(start0)}')

    print('Microdados em csv atualizados')


def __convert__(microdado, archive, delimiter=','):
    """
    Faz a conversão do arquivo.

    dicvars = ((*var*, *start*, *stop*), ...), onde:
     - **var** variable code - usado par nomear as variáveis na primeira linha
     - **start** coluna inicial - começando em 0
     - **stop** coluna depois da final

    O conteúdo dos campos é integralmente preservado,
    exceto os campos em branco ou com . que são transformados
    em strings vazias ''
    """
    nome = __nomecsv__(Path(microdado[0]).name, microdado[3])
    if not nome:
        return
    start = time()
    print(f' - Gerando {nome}', end='... ', flush=True)
    original = BytesIO()
    original.write(archive.read(microdado[2]))
    metadata = TextIOWrapper(original, encoding='utf-8')
    metadata.seek(0)
    meta = json.loads(metadata.read())
    dicvars = [(var,
                meta[var][_VPOS][0] - 1,
                meta[var][_VPOS][1]) for var in meta]

    # ler o arquivo zip com os dados e extrair
    with ZipFile(BytesIO(archive.read(microdado[0]))) as src:
        original = BytesIO()
        original.write(src.read(src.namelist()[0]))

    tgt = StringIO()
    tgt.write(delimiter.join([var[0] for var in dicvars]) + '\n')
    fixwidth = TextIOWrapper(original, encoding='utf-8')
    fixwidth.seek(0)
    for reg in fixwidth:
        csvreg = delimiter.join([reg[var[1]:var[2]].strip(' .')
                                 for var in dicvars])
        tgt.write(csvreg + '\n')

    # acrescentar ao arquivo e remover
    tgt.seek(0)
    archive.writestr(str(PPath(MICRO, nome)), tgt.read())
    print(f'OK! {__time__(start)}')


def __select__(mirrorfile):
    """
    Seleciona arquivos para atualização.

    NOTA:-em dezembro de 2020 os dicionários de variáveis
    foram corrigidos para atualizar a descrição de uma categoria
    de uma variável, sem atualizar as bases de microdados

    Atualizações no dicionário fazem gerar novamente os arquivos csv
    das bases que compartilham o dicionário, pois pode ser mudança em
    posição de leitura por conta de erro nas posições, não nos microdados
    """
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
    metas = {Path(item).name: json.loads(archive.read(item))
             for item in archive.namelist()
             if all(tag in item for tag in (META, 'microdados', 'json'))}
    dados = {Path(item).name: json.loads(archive.read(item))
             for item in archive.namelist()
             if all(tag in item for tag in (MICRO, 'microdados', 'json'))
             and META not in item}
    update = []
    # arquivos de registro são sempre atualizados
    drop = [str(PPath(MICRO, dado)) for dado in dados]
    for meta in metas:
        new = [item for item in metas[meta]
               if item not in dados[meta]]
        update.append([meta, new])
        drop.extend([str(PPath(MICRO, __nomecsv__(Path(item[0]).name,
                                                  item[3])))
                     for item in dados[meta]
                     if item not in metas[meta]])
    archive.close()
    if all(pnad[1] == [] for pnad in update):
        update = []
    if update:
        print('Atualizando microdados')
        __delete__(mirrorfile, drop)
    return update


def __check_metadata__(mirrorfile):
    # verifica se metadados já foram criados
    with ZipFile(mirrorfile, 'r') as archive:
        items = archive.namelist()
    if not any(META in Path(item).parts[0] for item in items):
        print('Metadados não encontrados')
        return False
    return True
