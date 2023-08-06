#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - Class Mirror

Gera um arquivo ZIP para armazenar uma cópia local dos
microdados da PNAD ou da PADC e possibilita a sincronização da cópia

A biblioteca zlib deve estar instalada para compressão
"""


import time
from ftplib import FTP, error_perm
from pathlib import Path, PurePosixPath as PPath
from zipfile import ZipFile, ZIP_DEFLATED
from .shared import ORI, URL, FLDRS, ALL
from .shared import __time__, __is_mirror_file__, __delete__


class Mirror():
    """
    Gera ou sincroniza um arquivo zip com cópias locais da PNAD ou PNADC.

    **mirrorfile** é uma string com o caminho e nome do arquivo
    """

    def __init__(self, mirrorfile):
        # aceitar um Path como argumento
        if isinstance(mirrorfile, Path):
            mirrorfile = str(mirrorfile)

        # tenta criar o arquivo ou abri-lo se existente
        try:
            file = ZipFile(mirrorfile, 'x', ZIP_DEFLATED)
        except FileExistsError:
            if __is_mirror_file__(mirrorfile):
                file = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
            else:
                return

        # se não deu erro de permissão ou outros tipos
        # fecha e guarda o nome
        file.close()
        self.zip = Path(mirrorfile)

        # remotefiles dicionário de listas
        # uma entrada para cada pnad
        # as listas tem o Path relativo ao root
        # atualizado por list_remote_files
        self.remotefiles = {}
        self.distros = {}

        # equivalente com arquivos zip
        self.localfiles = {}
        self.__mapzip__()

        # lista de items para sincronizar
        # atualizado por sync_list
        self.synclst = {'dld': {}, 'rmv': {}}

    @staticmethod
    def __connect__():
        """Conecta ao servidor FTP."""
        server = FTP(URL)
        server.connect()
        server.login()
        return server

    @staticmethod
    def __isfolder__(server, path):
        """Verifica se path é pasta."""
        try:
            server.cwd(path)
            server.cwd('..')
            return True
        except error_perm:
            return False

    def __mapftp__(self, server, pnad, ftproot, ftpcur):
        """Recursiva - lista arquivos in *remotefolder*."""
        server.cwd(str(PPath(ftproot, ftpcur)))
        itens = server.nlst()
        for item in itens:
            sourcename = PPath(ftproot, ftpcur, item)
            if self.__isfolder__(server, str(sourcename)):
                self.__mapftp__(server, pnad, ftproot, PPath(ftpcur, item))
            else:
                self.remotefiles[pnad].append(
                    [ftpcur, item, server.size(str(sourcename))])

    def __mapzip__(self):
        """Lista os arquivos originais no mirrorfile."""
        self.localfiles = {}
        archive = ZipFile(self.zip)
        # aqui é preciso infolist para obter nome e tamanho do arquivo
        files = archive.infolist()
        for file in files:
            path = PPath(file.filename)
            pnad = path.parts[1]
            if pnad not in self.localfiles:
                self.localfiles[pnad] = []
            self.localfiles[pnad].append([PPath(*path.parts[2:-1]),
                                          path.name,
                                          file.file_size])
        archive.close()
        return files

    def list_remote_files(self, pnads=ALL):
        """
        Lista os arquivos de microdados no servidor FTP do IBGE.

        **pnads** é uma string, tuple ou lista com tipos
        definidos pelas constantes:

            - *PNAD*, *PNADCA*, *PNADCT*

        **pnads** determina o tipo de cópia e pode ser qualquer combinação:

            - list_remote_files(*PNAD*) - copia da PNAD
            - list_remote_files((*PNADCA*, *PNADCT*)) - copia
              da PNADC trimestral e anual
            - list_remote_files(ALL) - copia da PNAD e da PNADC
        """
        if not isinstance(pnads, (tuple, list)) and pnads in ALL:
            pnads = (pnads, )
        self.distros = {}
        server = self.__connect__()
        for pnad in pnads:
            print(f' - Verificando arquivos da {pnad} - aguarde',
                  end='... ', flush=True)
            self.remotefiles[pnad] = []
            self.distros[pnad] = {}
            start = time.time()
            self.__mapftp__(server, pnad,
                            PPath('/', *FLDRS[pnad]), PPath(''))
            print(f'OK! {__time__(start)}')
            self.distros[pnad]['files'] = len(self.remotefiles[pnad])
            self.distros[pnad]['size'] = sum([item[2] for item in
                                              self.remotefiles[pnad]])
        server.close()

    def sync_list(self):
        """
        Atualiza *synclst* de acordo com *remote_files*.

        *synclst* contém as listas de arquivos a serem baixados e removidos
        """
        self.__mapzip__()
        for pnad in self.remotefiles:

            # download: arquivos remotos que não existem localmente
            self.synclst['dld'][pnad] = []
            for file in self.remotefiles[pnad]:
                if not self.localfiles:
                    self.synclst['dld'][pnad].append(file)
                elif file not in self.localfiles[pnad]:
                    self.synclst['dld'][pnad].append(file)

            # remove: arquivos locais que não existem remotamente
            self.synclst['rmv'][pnad] = []
            if self.localfiles:
                for file in self.localfiles[pnad]:
                    if file not in self.remotefiles[pnad]:
                        self.synclst['rmv'][pnad].append(file)

    def sync_now(self):
        """Sincroniza de acordo com *synclst*."""

        def __download__(remotefile, localfile):
            with archive.open(localfile, 'w') as handle:
                server.retrbinary(f'RETR {remotefile}', handle.write)

        def __synced__():
            for pnad in self.remotefiles:
                if self.synclst['rmv'][pnad] or self.synclst['dld'][pnad]:
                    return False
            return True

        def __remove__():
            del_lst = []
            for pnad in self.synclst['dld']:
                if self.synclst['dld'][pnad]:
                    dlds = [(file[0], file[1]) for file
                            in self.synclst['dld'][pnad]]
                    for file in self.localfiles[pnad]:
                        if (file[0], file[1]) in dlds:
                            del_lst.append(str(PPath(ORI, pnad,
                                                     file[0], file[1])))
            for pnad in self.synclst['rmv']:
                for file in self.synclst['rmv'][pnad]:
                    del_lst.append(str(PPath(ORI, pnad,
                                             file[0], file[1])))
            return del_lst

        if __synced__():
            print('Cópia local sincronizada')
            return

        start0 = time.time()
        server = self.__connect__()

        # remover arquivos desatualizados
        if self.localfiles:
            remove = __remove__()
            if remove:
                __delete__(self.zip, remove)

        # abre o novo zip - sem os arquivos desatualizados
        archive = ZipFile(self.zip, 'a', ZIP_DEFLATED)

        # baixar
        for pnad in ALL:
            if pnad in self.synclst['dld'] and self.synclst['dld'][pnad]:
                print(f'Arquivos da {pnad}')
                for file in self.synclst['dld'][pnad]:
                    start = time.time()
                    print(f' - Baixando {file[1]}', end='... ', flush=True)
                    source = PPath('/', *FLDRS[pnad], file[0], file[1])
                    target = PPath(ORI, pnad, file[0], file[1])
                    __download__(str(source), str(target))
                    print(f'OK! {__time__(start)}')
        archive.close()
        server.close()
        self.__mapzip__()
        self.sync_list()
        print(f'Arquivos baixados em {__time__(start0)}')
        print('Cópia local sincronizada')
