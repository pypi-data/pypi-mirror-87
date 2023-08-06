#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - www.ipea.gov.br.

pynad - command line app

script para facilitar o uso da biblioteca pynad
"""

import os
import sys
from pathlib import Path
from time import time
from .shared import PNAD, PNADCA, PNADCT, __time__
from .mirror import Mirror
from .metadata import metadata
from .to_csv import to_csv
from .panels_setup import setup
from .panels_ident import ident
from .panels_reshape import reshape


def main():
    """App linha de comando."""
    if len(sys.argv) == 1 or sys.argv[1].lower() not in COMANDOS:
        print(SYNTAX)
    else:
        if sys.argv[1].lower() == 'pnad':
            COMANDOS[sys.argv[1].lower()](ARQ_PNAD)
        elif sys.argv[1].lower() == 'pnadc':
            COMANDOS[sys.argv[1].lower()](ARQ_PNADC)
        else:
            COMANDOS[sys.argv[1].lower()]()
    print('\n' * 2)


def __identificar__():
    print('\nIdentificar os grupos domésticos e indivíduos dos painéis\n'
          + '---------------------------------------------------------')
    if all(ARQ_PNADC != file.name for file in CURDIR.iterdir()):
        print('Não há cópia da PNAD Contínua no diretório atual:')
        print(f'  {CURDIR}')
        print(SYNTAX)
        return
    ident(Path(CURDIR, ARQ_PAINEIS), Path(CURDIR, ARQ_PNADC))


def __metadados__():
    print('\nOrganizar e extrair metadados\n'
          + '-----------------------------')
    pnads = [file.name for file in CURDIR.iterdir()
             if file.name in (ARQ_PNAD, ARQ_PNADC)]
    if not pnads:
        print('Não há cópias da PNAD ou PNADC no diretório atual:')
        print(f'  {CURDIR}')
        print(SYNTAX)
        return
    if ARQ_PNAD in pnads:
        print('Ainda não implantado para cópias da PNAD')
    if ARQ_PNADC in pnads:
        metadata(Path(CURDIR, ARQ_PNADC))


def __microdados__():
    print('\nGerar microdados em csv\n'
          + '-----------------------')
    pnads = [file.name for file in CURDIR.iterdir()
             if file.name in (ARQ_PNAD, ARQ_PNADC)]
    if not pnads:
        print('Não há cópias da PNAD ou PNADC no diretório atual:')
        print(f'  {CURDIR}')
        print(SYNTAX)
        return
    if ARQ_PNAD in pnads:
        print('Não implantado para cópias da PNAD')
    if ARQ_PNADC in pnads:
        to_csv(Path(CURDIR, ARQ_PNADC))


def __montar__():
    print('\nMontar painéis identificados\n'
          + '----------------------------')
    if all(ARQ_PNADC != file.name for file in CURDIR.iterdir()):
        print('Não há cópia da PNAD Contínua no diretório atual:')
        print(f'  {CURDIR}')
        print(SYNTAX)
        return
    reshape(Path(CURDIR, ARQ_PAINEIS))


def __separar__():
    print('\nSeparar os painéis de domicílios\n'
          + '--------------------------------')
    if all(ARQ_PNADC != file.name for file in CURDIR.iterdir()):
        print('Não há cópia da PNAD Contínua no diretório atual:')
        print(f'  {CURDIR}')
        print(SYNTAX)
        return
    setup(Path(CURDIR, ARQ_PAINEIS), Path(CURDIR, ARQ_PNADC))


def __sincronizar__(arquivo):
    modo = f'Criar {arquivo}'
    if Path(arquivo).is_file():
        modo = f'Sincronizar  {arquivo}'
    print(f'\n{modo}\n{"-" * len(modo)}')
    copia = Mirror(arquivo)
    print('Conectando ao servidor de arquivos do IBGE')

    # ARQ_PNADC deve conter pnadc no nome
    if 'pnadc' in arquivo:
        copia.list_remote_files((PNADCT, PNADCA))
    else:
        copia.list_remote_files(PNAD)
    copia.sync_list()
    dld = [0, 0]
    for pnad in copia.synclst['dld']:
        dld[0] += (len(copia.synclst['dld'][pnad])
                   + len(copia.synclst['rmv'][pnad]))
        dld[1] += sum([file[2] for file in copia.synclst['dld'][pnad]])
    if dld[0]:
        print(f'O arquivo {arquivo} não está sincronizado')
        print(f' - {dld[0]} arquivos estão faltando ou desatualizados')
        print(f' - Tamanho do download: {dld[1] / 1000000:,.1f} MBytes')
        resp = input('Digite sim para baixar os arquivos'
                     + ' (ou Enter para sair): ')
        if resp.lower().strip() not in ('s', 'si', 'sim', 'y', 'yes'):
            if modo == 'criar':
                os.remove(arquivo)
                return
        else:
            copia.sync_now()
    else:
        print(f'O arquivo {arquivo} está sincronizado')


def __tudo__():
    print('\nProcessamento completo da pnadc\n'
          + '-------------------------------')
    print('Conectando ao servidor de arquivos do IBGE')
    start = time()
    copia = Mirror(Path(CURDIR, ARQ_PNADC))
    copia.list_remote_files((PNADCT, PNADCA))
    copia.sync_list()
    copia.sync_now()
    metadata(Path(CURDIR, ARQ_PNADC))
    to_csv(Path(CURDIR, ARQ_PNADC))
    setup(Path(CURDIR, ARQ_PAINEIS), Path(CURDIR, ARQ_PNADC))
    ident(Path(CURDIR, ARQ_PAINEIS), Path(CURDIR, ARQ_PNADC))
    reshape(Path(CURDIR, ARQ_PAINEIS))
    print(f'\nTudo feito em{__time__(start)}')


# -----------------------------------------------
# COMMAND LINE APP USA NOMES PADRÃO PARA ARQUIVOS
# -----------------------------------------------
ARQ_PNAD = 'copia.ibge.pnad.zip'
# deve ter pnadc no nome para __sincronizar__
ARQ_PNADC = 'copia.ibge.pnadc.zip'
ARQ_PAINEIS = 'paineis.ibge.pnadc.zip'
SYNTAX = ('\nUso:  pynad COMANDO'
          + '\n\n  COMANDO pode ser:\n'
          + '\n    pnad        criar/sincronizar uma cópia da PNAD Anual'
          + '\n    pnadc       criar/sincronizar uma cópia da PNAD Contínua'
          + '\n    metadados   gerar metadados'
          + '\n    microdados  gerar microdados em formato csv'
          + '\n    painel-sep  separar painéis'
          + '\n    painel-id   identificar painéis'
          + '\n    painel-mnt  montar painéis identificados'
          + '\n    pnadc-tudo  pnadc metadata microdata painel-sep|id|mnt'
          + '\n')
COMANDOS = {'pnadc': __sincronizar__,
            'pnad': __sincronizar__,
            'metadados': __metadados__,
            'microdados': __microdados__,
            'painel-sep': __separar__,
            'painel-id': __identificar__,
            'painel-mnt': __montar__,
            'pnadc-tudo': __tudo__}
CURDIR = Path(os.getcwd())
