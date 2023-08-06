#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - module panels

gera no arquivo ZIP de painéis
arquivos de identificação dos grupos domésticos e indivíduos
nos painéis de domicílios

Methods
-------
    ident(args)  para identificar todos os painéis
    load_panel(args)  para carregar um painel
    ident_panel(args)  para identificar o painel carregado
    view(args)  para visualizar um domicílio do painel
    (específico ou aleatório)
"""


import json
from io import BytesIO, StringIO, TextIOWrapper
from random import choice
from time import time
from pathlib import Path, PurePosixPath as PPath
from zipfile import ZipFile, ZIP_DEFLATED
from .shared import REGPES, REGPID, META
from .shared import __time__, __is_mirror_file__, __delete__


class Person():
    """
    representa um registro de pessoa.

    As instâncias desta classe representam registros de pessoas e
    seus atributos correspondem às variáveis empregadas na identificação,
    especificadas em __load_panel_metadata__(), função que retorna
    **attribs** e **categs** usados para criar uma instância;
    **values** é o registro como lista de valores e os
    códigos dos atributos da pessoa
    """

    def __init__(self, attribs, categs, values):
        for idx, attrib in enumerate(attribs):
            self.__dict__[attrib] = values[idx]
        self.sexcat = categs['sexcat'][str(self.sex)]
        self.stdcat = categs['stdcat'][str(self.std)] + 18 * ' '
        self.pid = 0
        self.cla = 0
        self.grp = 0
        self.ind = 0
        self.igi = 0
        self.igd = ''
        self.igm = ''
        self.iga = ''
        self.grpent = 0
        self.indent = 0

    def __repr__(self):
        """
        Retorna uma string que representa a pessoa.

        Contém os atributos usados na identificação,
        bem como os resultantes
        """
        repres = (f'e{self.ent} {self.sexcat[:3]} '
                  + f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f} '
                  + f'{self.ord:02.0f} {self.stdcat[:18]} '
                  + f'cla {self.cla} grpd {self.grp} ind {self.ind:02.0f}')
        if self.igd:
            repres += f' ({self.age} anos - {self.ano - self.age}-99-99)'
        return repres

    def classificada(self, csvdel=','):
        """
        Retorna o registro csv correspondente a pessoa.

        Para escrita no no arquivo de identificação de um painel
        """
        return csvdel.join([str(atrib) for atrib in (self.ano, self.tri,
                                                     self.upa, self.dom,
                                                     self.paibge, self.ent,
                                                     self.ord, self.pid,
                                                     self.cla, self.grp,
                                                     self.grpent,
                                                     self.ind, self.indent,
                                                     self.igd, self.igm,
                                                     self.iga)])

    def ident(self, estrita):
        """Retorna os atributos para a agregação em indivíduos."""
        idnt = f'{self.sexcat[:3]} '
        idnt += f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f}'
        if estrita:
            idnt += f' {self.ord:02.0f} {self.stdcat[:18]}'
        return idnt


def ident(panelfile, pnadc, delimiter=','):
    """
    Identifica os painéis.

    **panelfile** é uma string com o caminho e nome do arquivo de painel
    gerado por **setup()**

    **pnadc** é uma string com o caminho e nome do arquivo com a cópia
    da PNAD Contínua trimestral

    **delimiter** é opcional, *default* é vírgula
    """
    # aceitar Paths como argumentos e verificar
    if isinstance(panelfile, Path):
        panelfile = str(panelfile)
    if isinstance(pnadc, Path):
        pnadc = str(pnadc)
    with ZipFile(panelfile) as archive:
        files = archive.namelist()
        if not any(REGPES in file for file in files):
            print(f'{Path(panelfile).name} não é válido')
            return False
    if not __is_mirror_file__(pnadc):
        return False

    if any(REGPID in file for file in files):
        panelfiles = __id_select__(panelfile)
    else:
        panelfiles = [file for file in files if all(tag in file
                                                    for tag in (REGPES,
                                                                'csv'))]
    if panelfiles:
        with ZipFile(pnadc) as src:
            metadata = json.loads(src.read(str(PPath(META,
                                                     'variaveis.pnadc.'
                                                     + 'trimestral.json'))))
        archive = ZipFile(panelfile, 'a', ZIP_DEFLATED)
        start = time()
        print('\nIdentificando painéis:')
        panelfiles.sort()
        for pfile in panelfiles:
            pid, panel = load_panel(archive, pfile, metadata, delimiter)
            ident_panel(pid, panel, archive)
        archive.writestr(f'{REGPID}/microdados.pnadc.paineis.json',
                         archive.read(f'{REGPES}/'
                                      + 'microdados.pnadc.paineis.json'))
        archive.close()
        print(f'{len(panelfiles)} painéis identificados',
              f'em{__time__(start)}')
    print('Identificação dos painéis atualizada')
    return True


def ident_panel(pid, panel, archive=None, delimiter=','):
    """
    Identifica um painel na memória.

    **pid** e **panel** são retornados por **load_panel()**

    Se especificado o parâmetro **archive**, escreve um
    arquivo csv com a identificação do painel no arquivo
    """
    # prolegômenos
    start = time()
    print(f' - Identificando painel {pid}',
          end='... ', flush=True)

    # passa a lista de pessoas de cada domicílio do painel
    # para o método de identificação __identify__()
    for upa in tuple(panel.keys()):
        for dom in tuple(panel[upa].keys()):
            __identify__(panel[upa][dom])
    print('OK!', __time__(start))

    # escreve o arquivo csv de identificação
    if archive:
        start = time()
        print(f' - Escrevendo arquivo de identificação {pid}',
              end='... ', flush=True)
        target = StringIO()
        target.write(delimiter.join(('ano', 'trimestre', 'upa',
                                     'v1008', 'v1014', 'v1016', 'v2003',
                                     'pid', 'pidcla', 'pidgrp', 'pidgrpent',
                                     'pidind', 'pidindent', 'piddnd',
                                     'piddnm', 'piddna')) + '\n')
        for upa in tuple(panel.keys()):
            for dom in tuple(panel[upa].keys()):
                for pessoa in panel[upa][dom]:
                    target.write(pessoa.classificada() + '\n')
        target.seek(0)
        archive.writestr(f'{REGPID}/pid{pid}.csv', target.read())
        print('OK!', __time__(start))


def load_panel(archive, panelfile, metadata, delimiter=','):
    """
    Carrega um arquivo de microdados de painel.

    **archive** é o arquivo zip com os painéis (gerados por **setup()**)

    **panelfile** é um arquivo de microdados de painel em CSV

    **metadata** é o dicionário de variáveis trimestrasi da PNADC

    **delimiter** é opcional, *default* é vírgula

    Retorna:

    - **pid** código de identificação do painel no formato AAAAT

    - **painel** dicionário python contendo as pessoas dos
      domicílios do painel como instâncias da classe Person, organizados
      pelo número da UPA (chave primária) e pelo número do
      domicílio (v1008, chave secundária)
    """
    def __csv2person__(record):
        pessoa = []
        for attrib in attribs.values():
            pessoa.append(int(record[attrib[1]]))
        return tuple(pessoa)

    # prolegômenos
    start = time()
    print(f' - Carregando {Path(panelfile).name}',
          end='... ', flush=True)

    # carrega o painel
    painel = {}
    pdef = True

    file = TextIOWrapper(BytesIO(archive.read(panelfile)), encoding='utf-8')
    file.seek(0)
    header = file.readline()
    header = header.replace('\n', '').split(delimiter)
    # variáveis usadas na identificação e categorias de sexo e sitdom
    attribs, categs = __load_panel_metadata__(metadata, header)
    for line in file:

        # cada registro de pessoa em texto csv é pŕocessado
        # para gerar uma instância da classe Person, cujos atributos
        # são as variáveis empregadas na identificação
        person = Person(attribs, categs, __csv2person__(line.split(',')))

        # a identificação do painel é feita a partir do
        # primeiro registro de pessoa
        if pdef:
            pid = person.ano * 10 + person.tri
            pdef = False

        # todas as pessoas recebem o código de identificação do painel
        person.pid = pid

        # se for data ignorada, imputa ano de nascimento
        # igual ao ano de inicio do painel
        if person.dtd == 99:
            person.dta = int(person.pid / 10) - person.age

        # a pessoa do registro é inserida na lista de seu domicílio
        # criando as entradas da upa e do domicílio se necessário
        if person.upa not in painel:
            painel[person.upa] = {}
        if person.dom not in painel[person.upa]:
            painel[person.upa][person.dom] = []
        painel[person.upa][person.dom].append(person)
    print('OK!', __time__(start))
    return pid, painel


def view(pid, panel, upa=None, dom=None):
    """
    Retorna uma representação das pessoas de um domicílio.

    **pid** e **panel** são retornados por **load_panel()**

    Se a **upa** e o **dom** não são especificados, escolhe um domicilio
    aleatório do painel
    """
    if not upa:
        upa = choice(tuple(panel.keys()))
    if not dom:
        dom = choice(tuple(panel[upa].keys()))
    print(f'\nPainel {pid}, upa {upa}, domicílio {dom}')
    for pessoa in panel[upa][dom]:
        print(pessoa)


def __load_panel_metadata__(meta, header):
    """Seleciona e identifica os campos do registro csv."""
    # atributos e variáveis correspondentes
    attribs = {'ano': ['ano'],
               'tri': ['trimestre'],
               'upa': ['upa'],
               'dom': ['v1008'],
               'paibge': ['v1014'],
               'ent': ['v1016'],
               'tam': ['v2001'],
               'ord': ['v2003'],
               'std': ['v2005'],
               'sex': ['v2007'],
               'dtd': ['v2008'],
               'dtm': ['v20081'],
               'dta': ['v20082'],
               'age': ['v2009']}

    # acha a posição de cada atributo e obtém as descrições
    # dos códigos de sexo e situação no domicílio
    # tem que ler o header, a ordem das variáveis
    # é diferente
    for attrib in attribs.values():
        attrib.append(header.index(attrib[0]))
    categs = {'stdcat': meta['v2005']['valores'],
              'sexcat': meta['v2007']['valores']}
    return attribs, categs


def __id_select__(panelfile):
    selection = []
    metadata = 'microdados.pnadc.paineis.json'
    with ZipFile(panelfile) as archive:
        items = archive.namelist()
        curpanels = json.loads(archive.read(f'{REGPES}/{metadata}'))
        curpids = json.loads(archive.read(f'{REGPID}/{metadata}'))
    update = [pankey for pankey in curpanels
              if pankey not in curpids
              or curpids[pankey] != curpanels[pankey]]
    if update:
        print('Atualizando a identificação dos painéis')
        selection = [file for file in items for panel in update
                     if panel in file and REGPID in file]
        selection.append(f'{REGPID}/{metadata}')
        __delete__(panelfile, selection)
        selection = [file for file in items
                     for panel in update if panel in file
                     and REGPES in file]
    return selection


def __identify__(pessoas):
    # define a sequencia dos classificadores
    classificadores = (__id_cls1__,
                       __id_cls2__,
                       __id_cls3__)

    # se alguma pessoa tem data de nascimento ignorada, tratamento
    if any(pessoa.dtd == 99 for pessoa in pessoas):
        __id_birthdate_unknown__(pessoas)

    # identificar e separar os grupos domésticos do domicílio
    grpsdom = __id_split_grpds__(pessoas)

    # identificar os indivíduos de cada grupo doméstico
    for grpdom in grpsdom:
        for classificador in classificadores:
            classificadas = classificador(grpsdom[grpdom], grpdom)
            if classificadas:
                break


def __id_aggr_persons__(pessoas, estrita):
    """
    Agrega pessoas em indivíduos.

    **pessoas** são os registros das diferentes pessoas de todas
    as entrevistas realizadas em um domicílio

    **estrita** = True considera sexo, data de nascimento
    número de ordem e situação no domicílio

    **estrita** = False considera sexo e data de nascimento

    Retorna um dicionário de indivíduos com duas listas, a das entrevistas
    do indivíduo, e a das pessoas que lhe correspondem em cada entrevista
    """
    individuos = {}
    for pessoa in pessoas:
        identidade = pessoa.ident(estrita)
        if identidade not in individuos:
            individuos[identidade] = [[], []]
        individuos[identidade][0].append(pessoa.ent)
        individuos[identidade][1].append(pessoa)

    # se apenas sexo e data de nascimento, precisa controlar gemeos,
    # que aparecem como um indivíduo com entrevistas duplicadas
    # é preciso separá-los
    if not estrita:
        for individuo in list(individuos.keys()):
            reflist = list(set(individuos[individuo][0]))
            reflist.sort()
            if individuos[individuo][0] != reflist:
                for entrevista in reflist:
                    gemeos = [idx for idx, item in
                              enumerate(individuos[individuo][0])
                              if item == entrevista]
                    for gemeo, ordem in enumerate(gemeos):
                        identidade = individuo + 'gemeo' + str(gemeo + 1)
                        if identidade not in individuos:
                            individuos[identidade] = [[], []]
                        individuos[identidade][0].append(
                            individuos[individuo][1][ordem].ent)
                        individuos[identidade][1].append(
                            individuos[individuo][1][ordem])
                del individuos[individuo]

    # lista para conjunto de entrevistas do indivíduo
    for individuo in individuos:
        individuos[individuo][0] = list(set(individuos[individuo][0]))
    return individuos


def __id_birthdate_unknown__(pessoas):
    """
    Trata datas de nascimento ignoradas.

    Verifica se uma pessoa com data de nascimento ignorada em uma
    entrevista teve data declarada em outra, imputando a data em caso
    afirmativo
    """
    # separa as pessoas segundo a situação da data de nascimento
    dataign = [pessoa for pessoa in pessoas if pessoa.dtd == 99]
    datacon = [pessoa for pessoa in pessoas if pessoa.dtd != 99]
    for ign in dataign:

        # para cada pessoa com data ignorada, a lista de doadores
        # inicial considera todas as com data conhecida em outras
        # entrevistas, do mesmo sexo e, e com diferença de até
        # 3 anos do ano de nascimento estimado para a data ignorada
        doadores = [pessoa for pessoa in datacon
                    if pessoa.ent != ign.ent
                    and pessoa.sex == ign.sex
                    and abs(pessoa.dta - ign.dta) <= 3]

        # preferência para doadores com a mesma situação no domicílio
        # se existirem, desprezar os demais
        if [pessoa for pessoa in doadores if pessoa.std == ign.std]:
            doadores = [pessoa for pessoa in doadores
                        if pessoa.std == ign.std]

        # se não há doadores com a mesma situação no domicílio,
        # verificar se há doadores do conjunto permitido de troca
        # de código de situação, eliminando os que não estejam
        elif doadores:
            filtro = []
            if ign.std in (1, 2, 3):
                filtro = (1, 2, 3)
            elif ign.std in (4, 5, 6):
                filtro = (4, 5, 6)
            elif ign.std in (8, 9):
                filtro = (8, 9)
            else:
                filtro = (ign.std, )
            doadores = [doador for doador in doadores
                        if doador.std in filtro]

        # havendo doadores, a lista é ordenada pela proximidade
        # do ano de nascimento, sendo escolhido o mais próximo
        # o primeiro da lista
        if doadores:
            difs = [abs(doador.dta - ign.dta) for doador in doadores]
            mindif = [idx for idx, dif in enumerate(difs)
                      if dif == min(difs)][0]
            doador = doadores[mindif]
            ign.igd = doador.dtd
            ign.igm = doador.dtm
            ign.iga = doador.dta

    # imputa as datas de nascimento para as pessoas com data ignorada que
    # encontraram doadoras
    for pessoa in pessoas:
        if pessoa.igd:
            pessoa.dtd = pessoa.igd
            pessoa.dtm = pessoa.igm
            pessoa.dta = pessoa.iga
    return pessoas


def __id_cls1__(pessoas, grpdom):
    """Classificador 1, grupo doméstico sem mudanças."""
    # verifica se o tamanho do grupo doméstico é o mesmo
    # em todas as entrevistas e gera sua lista de entrevistas
    tamanho = pessoas[0].tam
    entdom = []
    for pessoa in pessoas:
        if pessoa.tam != tamanho:
            return []
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=True: sexo, data, ordem e sitdom
    individuos = __id_aggr_persons__(pessoas, True)

    # verifica se indivíduos aparecem em todas as entrevistas do grupo
    for individuo in individuos:
        if individuos[individuo][0] != entdom:
            return []

    # identifica as pessoas
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            identidade = pessoa.ident(True)
            if identidade == individuo:
                pessoa.cla = 1
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
    return pessoas


def __id_cls2__(pessoas, grpdom):
    """Classificador 2 grupos domésticos com tamanho constante e mudanças."""
    # verifica se o tamanho do grupo doméstico é o mesmo
    # em todas as entrevistas e gera sua lista de entrevistas
    tamanho = pessoas[0].tam
    entdom = []
    for pessoa in pessoas:
        if pessoa.tam != tamanho:
            return []
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=False: sexo e data
    individuos = __id_aggr_persons__(pessoas, False)

    # verifica se indivíduos aparecem em todas as entrevistas do grupo
    for individuo in individuos:
        if individuos[individuo][0] != entdom:
            return []

    # identifica as pessoas controlando gemeos do mesmo sexo
    indents = {}
    for individuo in individuos:
        indents[individuo] = []
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            if (pessoa in individuos[individuo][1]
                    and pessoa.ent not in indents[individuo]):
                pessoa.cla = 2
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
                indents[individuo].append(pessoa.ent)
    return pessoas


def __id_cls3__(pessoas, grpdom):
    """Classificador 3 grupos domésticos com mudanças variadas."""
    # recursiva para gerar todas as permutações de individuos
    # que não aparecem na mesma entrevista
    def __permuta__(indids, entrevistas, outras, possiveis):
        for outra in outras:
            entconjunta = entrevistas + individuos[outra][0]
            entconjunta.sort()

            possiveis.append([entconjunta, indids[:] + [outra]])
            if entconjunta != entdom:
                mais = [out for out in outras
                        if not any(ent in entconjunta
                                   for ent in individuos[out][0])]
                if mais:
                    possiveis = __permuta__(indids[:] + [outra],
                                            entconjunta[:], mais,
                                            possiveis)
        return possiveis

    # agrega indívíduos
    def __aggr_ind__(juntar, cla):
        individuos[juntar[1][0]][0] = juntar[0][:]
        for outra in juntar[1][1:]:
            individuos[juntar[1][0]][1].extend(
                individuos[outra][1])
            del individuos[outra]
        for pessoa in individuos[juntar[1][0]][1]:
            pessoa.cla = cla
        return juntar[1]

    # entrevistas do grupo doméstico
    entdom = []
    for pessoa in pessoas:
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=False: sexo e data
    individuos = __id_aggr_persons__(pessoas, False)

    # separa e classifica os indivíduos que aparecem em todas as entrevistas
    todas = [individuo for individuo in individuos
             if individuos[individuo][0] == entdom]
    for individuo in todas:
        for pessoa in individuos[individuo][1]:
            pessoa.cla = 3

    # separa e classifica provisoriamente os que aparecem em algumas
    algumas = [individuo for individuo in individuos
               if individuo not in todas]
    for individuo in algumas:
        for pessoa in individuos[individuo][1]:
            pessoa.cla = 4

    # permutações de indivíduos sem aparições conjuntas
    possibilidades = []
    for individuo in algumas:
        entrevistas = list(individuos[individuo][0])
        outras = [outra for outra in list(algumas)
                  if outra != individuo
                  and not any(entrevista in entrevistas
                              for entrevista in individuos[outra][0])]
        if outras:
            possibilidades.extend(__permuta__([individuo],
                                              entrevistas,
                                              outras, []))

    # reduzir permutações a combinações
    organizadas = []
    for possibilidade in possibilidades:
        if not organizadas:
            organizadas.append(possibilidade)
        elif possibilidade not in organizadas:
            adicionar = True
            for organizada in organizadas:
                if (organizada[0] == possibilidade[0]
                        and len(organizada[1]) == len(possibilidade[1])
                        and all(individuo in organizada[1]
                                for individuo in possibilidade[1])):
                    adicionar = False
                    break
            if adicionar:
                organizadas.append(possibilidade)

    # comparar todos os pares de atributos e registrar diferenças
    # a ordem de atribs é relevante
    atribs = ('sex', 'dtd', 'dtm', 'dta', 'std')
    for idx, organizada in enumerate(organizadas):
        organizadas[idx].append([])
        organizadas[idx].append([])
        organizadas[idx].append([])
        possiveis = organizada[1][:]
        while possiveis:
            possivel = possiveis.pop(0)
            pessoa1 = individuos[possivel][1][0]
            outras = [outra for outra in possiveis
                      if outra != possivel]
            for outra in outras:
                pessoa2 = individuos[outra][1][0]
                difs = [atrib for atrib in atribs
                        if pessoa1.__dict__[atrib] !=
                        pessoa2.__dict__[atrib]]
                organizadas[idx][2].append(difs)
                organizadas[idx][3].append([pessoa1.std, pessoa2.std])
                organizadas[idx][4].append([pessoa1.dta, pessoa2.dta])

    # ordenar as combinações para processar primeiro as
    # que resultariam em fusão de mais fragmentos e maior número
    # de entrevistas
    organizadas.sort(key=lambda item: len(item[0]) * 100 + len(item[1]) * 10
                     + 5 - max([len(difs) for difs in item[2]]),
                     reverse=True)

    # conjunto de erros permitidos
    erros = [['sex'],
             ['dtd'],
             ['dtm'],
             ['dta'],
             ['sex', 'dtd'],
             ['sex', 'dtm'],
             ['sex', 'dta'],
             ['dtd', 'dtm'],
             ['dtm', 'dta'],
             ['dtd', 'dta']]

    # com mudança de condição no domicílio
    erstd = [erro[:] + ['std'] for erro in erros]

    # agregar fragmentos de indivíduos
    juntados = []
    residuos = []
    for organizada in organizadas:
        if not any(individuo in organizada[1] for individuo in juntados):

            # fragmentos com mesma condição no domicílio
            # diferença de até 3 anos entre anos de nascimento
            if (all(erro in erros for erro in organizada[2])
                    and all(abs(dta[0] - dta[1]) <= 3
                            for dta in organizada[4])):
                juntados.extend(__aggr_ind__(organizada, 6))

            # fragmentos com diferente condição no domicílio
            # diferença de até 3 anos entre anos de nascimento
            elif (all(erro in erstd for erro in organizada[2])
                  and all(abs(dta[0] - dta[1]) <= 3
                          for dta in organizada[4])):
                juntados.extend(__aggr_ind__(organizada, 7))
            else:
                residuos.append(organizada)
                for individuo in organizada[1]:
                    for pessoa in individuos[individuo][1]:
                        pessoa.cla = 5

    # identifica as pessoas controlando gemeos do mesmo sexo
    indents = {}
    for individuo in individuos:
        indents[individuo] = []
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            if (pessoa in individuos[individuo][1]
                    and pessoa.ent not in indents[individuo]):
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
                indents[individuo].append(pessoa.ent)
    return pessoas


def __id_split_grpds__(pessoas):
    """Identifica e separa os grupos domésticos de um domicílio."""
    # dicionário de grupos domésticos
    grpsdom = {}

    # separa as pessoas por entrevista
    ents = {}
    for pessoa in pessoas:
        if pessoa.ent not in ents:
            ents[pessoa.ent] = []
        ents[pessoa.ent].append(pessoa)

    # uma entrevista, um grupo; nada a separar...
    if len(ents) == 1:
        grpsdom[1] = pessoas
        for pessoa in grpsdom[1]:
            pessoa.grp = 1
        return grpsdom

    # se mais de uma entrevista
    # agrega as pessoas em indivíduos
    # estrita=False: sexo e, data
    individuos = __id_aggr_persons__(pessoas, False)

    # procurar a entrevista com mais pessoas com data de nascimento conhecida
    inicio = [(ent, len([pessoa for pessoa in ents[ent]
                         if pessoa.dtd < 99]))
              for ent in ents]
    inicio.sort(key=lambda e: e[1], reverse=True)
    ent = inicio[0][0]
    curdom = 0

    # processar entrevistas e ir retirando as atribuídas a um grupo
    # doméstico da lista de entrevistas
    while ents:

        # atribui ao primeiro grupo as pessoas da entrevista inicial
        # e a retira da lista
        curdom += 1
        grpsdom[curdom] = ents[ent]
        del ents[ent]

        # achar outras entrevistas com pessoas de indivíduos que estavam
        # na entrevista inicial e removê-las
        for individuo in individuos.values():
            if any(pessoa in grpsdom[curdom] for pessoa in individuo[1]):
                for ent in individuo[0]:
                    if ent in ents:
                        grpsdom[curdom].extend(ents[ent])
                        del ents[ent]
                    for ini in inicio:
                        if ini[0] == ent:
                            inicio.remove(ini)
                    if not ents:
                        break
            if not ents:
                break

        # verifica se há entrevistas não atribuídas, havendo
        # seleciona a com maior número de pessoas e reinicia o loop
        # criando outro grupo doméstico
        if inicio:
            ent = inicio[0][0]

    # reordenar pessoas
    reord = []
    for grpdom in grpsdom:
        grpsdom[grpdom].sort(key=lambda pessoa: pessoa.ent * 100 + pessoa.ord)
        reord.append([min([pessoa.ent for pessoa in grpsdom[grpdom]]), grpdom])
    reord.sort(key=lambda e: e[0])

    # ordenar grupos domésticos segundo a visita
    # o grupo 1 é o da primeira entrevista
    grpsdomord = {}
    for idx, val in enumerate(reord):
        grpsdomord[idx + 1] = grpsdom[val[1]]
    return grpsdomord
