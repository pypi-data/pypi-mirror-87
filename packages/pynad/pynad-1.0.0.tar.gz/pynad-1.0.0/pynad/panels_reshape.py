#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - method reshape

gera um um conjunto de microdados de painéis com os registros
de indivíduos

nesta base, as variáveis dos indivíduos são replicadas por visita
e sufixadas com o número da visita eg. v2005_1, v2005_2 ... v2005_5
"""


import json
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path
from time import time
from zipfile import ZipFile, ZIP_DEFLATED
from tablib import Dataset
from .shared import REGIND, REGPID, REGPES
from .shared import __time__, __delete__


def reshape(panelfile, delimiter=','):
    """
    Monta ou atualiza os painéis de individuos identificados.

    **panelfile** arquivo dos painéis

    **delimiter** é opcional, *default* é vírgula
    """
    # aceitar Paths como argumentos e verificar
    if isinstance(panelfile, Path):
        panelfile = str(panelfile)
    with ZipFile(panelfile) as src:
        files = src.namelist()
    if not any(file for file in files if REGPES in file or REGPID in file):
        print(f'{panelfile} inválido')
        return
    panels = __select__(panelfile)
    if panels == 'abort':
        return
    start = time()
    if panels:
        print('Montando painéis identificados')
        for panel in panels:
            print(f'Painel {panel}')
            __reshape_panel__(panel, panelfile, delimiter)
        with ZipFile(panelfile, 'a', ZIP_DEFLATED) as tgt:
            tgt.writestr(f'{REGIND}/microdados.pnadc.paineis.json',
                         tgt.read(f'{REGPID}/microdados.pnadc.paineis.json'))
        print(f'{len(panels)} painéis identificados montados',
              f'em{__time__(start)}')
    print('Painéis de indivíduos atualizados')


def __drop_columns__(datafile):
    data = Dataset()
    datafile.seek(0)
    data.load(datafile, format='csv')
    for var in data.headers[:]:
        if not any(obs != '' for obs in data[var]):
            del data[var]
    return StringIO(data.export('csv'))


def __reshape_panel__(panel, panelfile, delimiter):
    with ZipFile(panelfile) as src:
        stacked = BytesIO(src.read(
                          f'{REGPES}/microdados.pnadc.paineis.{panel}.csv'))
        pidfile = BytesIO(src.read(f'{REGPID}/pid{panel}.csv'))

    header, individuos = __unstack__(stacked, pidfile, delimiter)
    __write_base__(panel, panelfile, header, individuos, delimiter)
    __write_sections__(panel, panelfile, header, individuos, delimiter)


def __select__(panelfile):
    selection = []
    metadata = 'microdados.pnadc.paineis.json'
    with ZipFile(panelfile) as archive:
        files = archive.namelist()
        curpanels = json.loads(archive.read(f'{REGPES}/{metadata}'))
        curpids = json.loads(archive.read(f'{REGPID}/{metadata}'))
        if any(REGIND in file for file in files):
            unstacked = json.loads(archive.read(f'{REGIND}/{metadata}'))
        else:
            unstacked = []
    update = [pankey for pankey in curpanels
              if pankey not in curpids
              or curpids[pankey] != curpanels[pankey]]
    if update:
        print('Há painéis não identificados')
        return 'abort'

    update = [pankey for pankey in curpids
              if pankey not in unstacked
              or curpids[pankey] != unstacked[pankey]]
    if update and unstacked:
        print('Atualização de painéis de indivíduos')
        selection = [file for file in files for panel in update
                     if panel in file and REGIND in file]
        selection.append(f'{REGIND}/{metadata}')
        __delete__(panelfile, selection)
    return update


def __unstack__(stacked, pidfile, delimiter):
    start = time()
    print(' - Carregando pessoas por indivíduo (reshape wide, unstack)',
          end='... ', flush=True)
    individuos = {}
    src = TextIOWrapper(pidfile, encoding='utf-8')
    pidheader = src.readline()
    pidheader = pidheader.replace('\n', '').split(delimiter)
    indpos = tuple(pidheader.index(var) for var in
                   ('upa', 'v1008', 'pidgrp', 'pidind'))
    pespos = tuple(pidheader.index(var) for var in
                   ('upa', 'v1008', 'v1016', 'v2003'))
    pidpos = tuple(pidheader.index(var) for var in pidheader
                   if var[:3] == 'pid')
    for reg in src:
        reg = reg.replace('\n', '').split(delimiter)
        indkey = tuple(int(reg[pos]) for pos in indpos)
        try:
            peskey = tuple(int(reg[pos]) for pos in pespos)
        except IndexError:
            print(pespos, reg)
            raise
        pid_dt = tuple(reg[pos] for pos in pidpos)
        if indkey not in individuos:
            individuos[indkey] = [pid_dt, [peskey]]
        else:
            individuos[indkey][1].append(peskey)

    pidheader = [var for var in pidheader if var[:3] == 'pid']
    pessoas = {}
    src = TextIOWrapper(stacked, encoding='utf-8')
    panheader = src.readline()
    panheader = panheader.replace('\n', '').split(delimiter)
    pespos = tuple(panheader.index(var) for var in
                   ('upa', 'v1008', 'v1016', 'v2003'))
    for reg in src:
        reg = reg.replace('\n', '').split(delimiter)
        peskey = tuple(int(reg[pos]) for pos in pespos)
        pessoas[peskey] = tuple(reg)

    for ind in individuos:
        pesind = []
        for peskey in individuos[ind][1][:]:
            pesind.append(individuos[ind][0] + pessoas[peskey])
        individuos[ind] = pesind
    print('OK!', __time__(start))
    pesheader = __weights__((pidheader + panheader), individuos)
    return pesheader, individuos


def __weights__(header, individuos):
    posv1016 = header.index('v1016')
    posv1027 = header.index('v1027')
    posv1029 = header.index('v1029')
    posposest = header.index('posest')
    popposest = {}
    for vis in range(1, 6):
        popposest[str(vis)] = {}
    for individuo in individuos:
        for pessoa in individuos[individuo]:
            visita = pessoa[posv1016]
            posest = pessoa[posposest]
            if posest not in popposest[visita]:
                popposest[visita][posest] = [int(pessoa[posv1029]),
                                             float(pessoa[posv1027])]
            else:
                popposest[visita][posest][1] += float(pessoa[posv1027])
    for individuo in individuos:
        for idx, pessoa in enumerate(individuos[individuo]):
            visita = pessoa[posv1016]
            posest = pessoa[posposest]
            peso = (popposest[visita][posest][0] /
                    popposest[visita][posest][1] *
                    float(pessoa[posv1027]))
            individuos[individuo][idx] += (str(peso), )
    header.append('pidpeso')
    return header


# constantes para os nomes de blocos - sections
BASE = 'basico'
EDUC = 'educa'
TRAB = 'trabalho'
OREN = 'rendas'
MORA = 'moradia'
TICS = 'tics'
TURI = 'turismo'
DERI = 'derivadas'
TRIN = 'trabinfa'


def __write_base__(panel, panelfile, pesheader, individuos, delimiter):
    # BASE - caso especial
    # inclui todas as variáveis constantes nas visitas
    start = time()
    print(f' - Escrevendo e compactando arquivo {BASE}',
          end='... ', flush=True)

    constantes = ('uf', 'capital', 'rm_ride', 'v1022', 'v1023',
                  'estrato', 'posest', 'v1014', 'pid', 'upa', 'v1008',
                  'pidgrp', 'pidgrpent', 'pidind', 'pidcla', 'pidindent',
                  'piddnd', 'piddnm', 'piddna')
    variaveis = [var for var in pesheader
                 if var[:2] in ('v1', 'v2') or var[:3] == 'vd2'
                 and var not in constantes]
    variaveis.sort()
    variaveis = ['ano', 'trimestre', 'pidpeso'] + variaveis
    header = constantes + tuple(f'{var}_{vis}' for vis in range(1, 6)
                                for var in variaveis)
    tgt = StringIO()
    tgt.write(delimiter.join(header) + '\n')
    for indkey in individuos:
        reg = [individuos[indkey][0][pesheader.index(var)]
               for var in constantes]
        track = 1
        for pessoa in individuos[indkey]:
            visita = int(pessoa[pesheader.index('v1016')])
            while visita > track:
                reg.extend([''] * len(variaveis))
                track += 1
            reg.extend([pessoa[pesheader.index(var)]
                        for var in variaveis])
            track += 1
        while track < 6:
            reg.extend([''] * len(variaveis))
            track += 1
        tgt.write(delimiter.join(reg) + '\n')
    print('OK!', __time__(start))
    tgt.seek(0)
    tgtname = f'{REGIND}/microdados.pnadc.paineis.{panel}.{BASE}.csv'
    with ZipFile(panelfile, 'a', ZIP_DEFLATED) as archive:
        archive.writestr(tgtname, tgt.read())
    del tgt


def __write_sections__(panel, panelfile, pesheader, individuos, delimiter):
    constantes = ('pid', 'upa', 'v1008', 'pidgrp', 'pidind')
    sections = ((EDUC, ('v3',)),
                (TRAB, ('v4',)),
                (OREN, ('v5', 'vi5')),
                (DERI, ('vd', 'vdi')),
                (MORA, ('s01',)),
                (TICS, ('s07',)),
                (TURI, ('s08',)),
                (TRIN, ('s06', 'sd')))
    for section in sections:
        variaveis = [var for var in pesheader
                     if any(prefix in var[:len(prefix)]
                            for prefix in section[1])]
        if not variaveis:
            continue
        variaveis.sort()
        start = time()
        print(f' - Escrevendo e compactando arquivo da seção {section[0]}',
              end='... ', flush=True)
        header = constantes + tuple(f'{var}_{vis}' for vis in range(1, 6)
                                    for var in variaveis)
        datafile = StringIO()
        datafile.write(delimiter.join(header) + '\n')
        for indkey in individuos:
            reg = [individuos[indkey][0][pesheader.index(var)]
                   for var in constantes]
            track = 1
            for pessoa in individuos[indkey]:
                visita = int(pessoa[pesheader.index('v1016')])
                while visita > track:
                    reg.extend([''] * len(variaveis))
                    track += 1
                reg.extend([pessoa[pesheader.index(var)]
                            for var in variaveis])
                track += 1
            while track < 6:
                reg.extend([''] * len(variaveis))
                track += 1
            datafile.write(delimiter.join(reg) + '\n')
        datafile = __drop_columns__(datafile)
        datafile.seek(0)
        tgtname = f'{REGIND}/microdados.pnadc.paineis.{panel}.{section[0]}.csv'
        with ZipFile(panelfile, 'a', ZIP_DEFLATED) as archive:
            archive.writestr(tgtname, datafile.read())
        del datafile
        print('OK!', __time__(start))
