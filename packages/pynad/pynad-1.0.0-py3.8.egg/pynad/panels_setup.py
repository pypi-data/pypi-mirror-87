#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - method setup

gera um arquivo ZIP com os microdados das pnads
organizados em painéis a partir de cópias locais
da PNAD Contínua Trimestral e Anual
"""


import json
from io import BytesIO, StringIO, TextIOWrapper
from time import time
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from .shared import REGPES, PNADCA, PNADCT, MICRO
from .shared import __time__, __is_mirror_file__
from .shared import __delete__, __nomecsv__


def setup(panelfile, pnadc, pnadca='', delimiter=','):
    """
    Separa os microdados por painel.

    **panelfile** é uma string com o caminho e nome do arquivo dos painéis;
    se não existir será criado

    **pnadc** é uma string com o caminho e nome da cópia da PNADC;
    se a pnadc trimestral e a anual estiverem em arquivos separados
    deve ser o da PNADC trimestral

    **pnadca** se a pnadc trimestral e a anual estiverem em arquivos separados
    especifica o caminho e nome do arquivo da PNADC anual

    **delimiter** é opcional, *default* é vírgula
    """
    # aceitar Paths como argumentos e verificar
    if isinstance(panelfile, Path):
        panelfile = str(panelfile)
    if isinstance(pnadc, Path):
        pnadc = str(pnadc)
    if isinstance(pnadca, Path):
        pnadca = str(pnadca)
    if not __is_mirror_file__(pnadc):
        return
    if pnadca and not __is_mirror_file__(pnadca):
        return

    microdados = __set_validate_mirror__(pnadc, pnadca)
    if len(microdados) < 2:
        print('Não foram encontrados os microdados da PNAD Contínua',
              'anual e trimestral com metadados e microdados em formato CSV')
        return False
    if pnadca == '':
        pnadca = pnadc

    start = time()

    # paineis completos disponíveis em mirror - básico e suplementos
    curpanels = __set_panels_mirror__(microdados)
    update = curpanels
    try:
        archive = ZipFile(panelfile, 'x', ZIP_DEFLATED)
        archive.close()
    except FileExistsError:
        with ZipFile(panelfile) as archive:
            files = archive.namelist()
        if not any(REGPES in file for file in files):
            print(f'{Path(panelfile).name} não é válido')
            return False
        update = __set_panels_archive__(panelfile, curpanels)
    if update == 'abort':
        return
    if update:
        __set_join__(update, panelfile, pnadc, pnadca, delimiter)
        with ZipFile(panelfile, 'a', ZIP_DEFLATED) as archive:
            archive.writestr(f'{REGPES}/microdados.pnadc.paineis.json',
                             json.dumps(curpanels))
        print(f'{len(update)} painéis separados',
              f'em{__time__(start)}')
    print('Painéis de domicílios atualizados')


def __set_append__(joinfiles, newheader, delimiter):
    data = {}
    keys = ['upa', 'v1008', 'v2003']
    for visita, bases in enumerate(joinfiles):
        bases[0][1].seek(0)
        header = bases[0][1].readline()
        header = header.replace('\n', '').split(delimiter)
        poskeys = [header.index(var) for var in keys]
        posvars = [header.index(var) if var in header else -1
                   for var in newheader]
        for reg in bases[0][1]:
            reg = reg.replace('\n', '').split(delimiter)
            key = tuple([int(reg[pos]) for pos in poskeys] + [visita])
            if reg[header.index('v1016')] == str(visita + 1):
                data[key] = [reg[pos] if pos > -1 else ''
                             for pos in posvars]
        if len(bases) == 2:
            bases[1][1].seek(0)
            header = bases[1][1].readline()
            header = header.replace('\n', '').split(delimiter)
            poskeys = [header.index(var) for var in keys]
            posvars = [header.index(var) if var in header else -1
                       for var in newheader]
            for reg in bases[1][1]:
                reg = reg.replace('\n', '').split(delimiter)
                key = tuple([int(reg[pos]) for pos in poskeys] + [visita])
                xtr = [reg[pos] if pos > -1 else '' for pos in posvars]
                if key in data:
                    fin = []
                    for idx, _unu in enumerate(xtr):
                        if data[key][idx] == '' and xtr[idx] == '':
                            fin.append('')
                        elif data[key][idx] != '':
                            fin.append(data[key][idx])
                        elif xtr[idx] != '':
                            fin.append(xtr[idx])
                    data[key] = fin
    return data


def __set_join__(panels, panelfile, pnadc, pnadca, delimiter):
    print('Separando painéis:')
    for panel in panels:
        start = time()
        print(f' - Painel {panel}, aguarde', end='... ', flush=True)
        tri = int(str(panel)[-1]) - 1
        ano = panel // 10
        joinfiles = []
        for vis in range(0, 5):
            tri += 1
            if tri > 4:
                tri = 1
                ano = ano + 1
            trimestre = [file for file in panels[panel][1]
                         if f'trimestre{tri}' in file and str(ano) in file]
            if trimestre:
                joinfiles.append([[__nomecsv__(Path(trimestre[0]).name,
                                               PNADCA), BytesIO()]])
            else:
                joinfiles.append([[__nomecsv__(
                    Path(panels[panel][0][vis]).name,
                    PNADCT), BytesIO()]])
            visita = [file for file in panels[panel][1]
                      if f'visita{vis + 1}' in file]
            if visita:
                joinfiles[-1].append([__nomecsv__(Path(visita[0]).name,
                                                  PNADCA), BytesIO()])
        newheader = __set_join_vars__(joinfiles, pnadc, pnadca, delimiter)
        joined = __set_append__(joinfiles, newheader, delimiter)
        tgt = StringIO()
        tgt.write(delimiter.join(newheader) + '\n')
        for reg in joined.values():
            tgt.write(delimiter.join(reg) + '\n')
        tgt.seek(0)
        with ZipFile(panelfile, 'a', ZIP_DEFLATED) as arc:
            arc.writestr(f'{REGPES}/microdados.pnadc.paineis.{panel}.csv',
                         tgt.read())
        print(f'OK! {__time__(start)}')
        del joinfiles


def __set_join_vars__(joinfiles, pnadc, pnadca, delimiter):
    alphaheader = ['ano', 'trimestre', 'uf', 'capital', 'rm_ride',
                   'estrato', 'posest', 'upa']
    headers = {}
    for visita in joinfiles:
        for file in visita:
            archive = pnadc
            if any(tag in file[0] for tag in ('trimestre', 'visita')):
                archive = pnadca
            with ZipFile(archive) as src:
                file[1].write(src.read(f'{MICRO}/{file[0]}'))
            file[1] = TextIOWrapper(file[1], encoding='utf-8')
            file[1].seek(0)
            headers[file[0]] = file[1].readline().strip('\n').split(delimiter)

    # variáveis começadas por v antes das começadas por s
    ordenar = [[], []]
    for header in headers:
        for var in headers[header]:
            if (var not in alphaheader
                and var not in ordenar[0]
                    and var[0] == 'v'):
                ordenar[0].append(var)
            if (var not in alphaheader
                and var not in ordenar[1]
                    and var[0] == 's'):
                ordenar[1].append(var)
    ordenar[0].sort()
    ordenar[1].sort()
    newheader = alphaheader + ordenar[0] + ordenar[1]
    return newheader


def __set_panels_archive__(panelfile, curpanels):
    with ZipFile(panelfile, 'a', ZIP_DEFLATED) as archive:
        try:
            panels = json.loads(archive.read(
                f'{REGPES}/microdados.pnadc.paineis.json'))
        except KeyError:
            print('Arquivo de painéis inválido - delete e tente de novo')
            return 'abort'
    update = {pankey: panval for pankey, panval in curpanels.items()
              if str(pankey) not in panels
              or panels[str(pankey)] != curpanels[pankey]}
    if update:
        print('Atualização de painéis de domicílios')
        drop = [f'{REGPES}/microdados.pnadc.paineis.{pid}.csv'
                for pid in update if str(pid) in panels]
        drop.append(f'{REGPES}/microdados.pnadc.paineis.json')
        __delete__(panelfile, drop)
    return update


def __set_panels_mirror__(microdados):
    panels = {}
    # para os últimos 4 trimestres não há paineis completos
    # microdados estão ordenados
    for idx, microdado in enumerate(microdados[PNADCT][:-4]):
        ano = int(Path(microdado[0]).name.split('_')[1][2:6])
        tri = int(Path(microdado[0]).name.split('_')[1][:2])
        pid = ano * 10 + tri
        panels[pid] = [[mcdt[0] for mcdt in microdados[PNADCT][idx:idx + 5]]]
        anuais = []
        for seq in range(5):
            if tri > 4:
                tri = 1
                ano += 1
            anuais.append((str(ano), f'trimestre{tri}'))
            anuais.append((str(ano), f'visita{seq + 1}'))
            tri += 1
        panels[pid].append([microdado[0] for microdado in microdados[PNADCA]
                            if any(f'_{anual[0]}_' in microdado[0] and
                                   anual[1] in microdado[0]
                                   for anual in anuais)])
    return panels


def __set_validate_mirror__(pnadc, pnadca):
    micro = {}
    with ZipFile(pnadc) as archive:
        try:
            micro[PNADCT] = json.loads(archive.read(
                f'{MICRO}/microdados.pnadc.trimestral.json'))
        except KeyError:
            pass
    if pnadca:
        with ZipFile(pnadca) as archive:
            try:
                micro[PNADCA] = json.loads(archive.read(
                    f'{MICRO}/microdados.pnadc.anual.json'))
            except KeyError:
                pass
    else:
        with ZipFile(pnadc) as archive:
            try:
                micro[PNADCA] = json.loads(archive.read(
                    f'{MICRO}/microdados.pnadc.anual.json'))
            except KeyError:
                pass
    return micro
