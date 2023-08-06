#####
pynad
#####
A command line application and package to download, sync, organize and prepare the microdata and metadata of the Brazilian National Household Survey, **Pesquisa Nacional por Amostra de Domicílios Contínua** - **PNADC** - fielded by the Instituto Brasileiro de Geografia e Estatística, `IBGE <http://www.ibge.gov.br>`_.

The **PNADC** is a rotating panel survey. The residential dwellings sampled for a panel are visited five times, quarterly. Every quarter a new panel starts, thus there are five active panels in visits 1 to 5. However, IBGE only disseminates PNADC microdata as cross-section datasets, aggregating records from distinct panels. The *trimestral* and the *anual-trimestre* datasets are aggregates of the distinct visits of the five panels surveyed in a quarter; the *anual-visita* datasets are annual aggregates of first or fifth visit interviews, comprised by four panels visited for the first or fifth time in a year.

----------------
What pynad does?
----------------
**IBGE periodically releases new PNADC datasets and documents. Eventually, previously released datasets and documents are patched. Currently, there are more than a hundred files to download and monitor for updates.**

Pynad ascertains one always have the latest versions of data and documents, and helps to keep track of the versions used in an application. It clones the *Microdados* folder of the PNADC distributions at IBGE's `FTP server <ftp://ftp.ibge.gov.br/>`_ as a local archive, a compressed **zip** file, syncing it at user demand.

**PNADC datasets are disseminated as text files with fixed width records. The position of each variable in the record must be declared to load them. The full metadata (names and columns of variables, categories etc.) are in binary xls Excel files.**

Pynad converts the original microdata to standard **csv** text files, conveniently organizes copies of the original *dicionários de variáveis*, and generates machine and human readable **json** text files containing all metadata. The new files are stored in the archive containing the local copy of the PNADC, in distinct folders.

When the local copy is synced, pynad updates the metadata and **csv** files on a need basis.

**PNADC datasets are organized for use as a quarterly or annual cross-section survey, mixing records from 4 or 5 distinct panels. One panel has variables scattered in different datasets. Though dwellings are identified, households and individuals are not. Population weights are not available for the panels**

Pynad creates another archive for panel files. It separates the panels retrieving their records from the cross-sectional datasets and generates a **csv** microdata file for each panel. Then pynad identifies the households and individuals in each dwelling and generates a **csv** microdata file with the keys for each panel.

Finally, pynad joins the panels and identifiers, and reshapes the joined datasets as identified individual records. Original variables have up to five instances in the identified individual records. E.g. for literacy, v3001, the identified individual record has v3001_1, v3001_2 v3001_3, v3001_4, v3001_5.

After reshaping, it calculates and adds panel population weights to the records. Then the records are split in variable blocks: basic, education, labour, income etc. A **csv** microdata file of identified individual records is created for each block of every panel.

When the local copy is synced, and the metadata and **csv** files updated, pynad updates the panel files on a need basis.

-------
Install
-------
`Windows <https://docs.python.org/3/using/windows.html#install-layout-option>`_ users should add Python to the PATH environment variable.

Use `pip <https://docs.python.org/3/installing/index.html#installing-index>`_ to install pynad.

************
Requirements
************
Three additional packages will be installed: `Tablib <https://pypi.org/project/tablib/>`_, `xlrd <https://pypi.org/project/xlrd/>`_, `xlwt <https://pypi.org/project/xlwt/>`_. They are required to extract the metadata from the *dicionários de variáveis*, disseminated as Excel binary files (**xls**).

Pynad requires a computer with **16GB RAM**, as it can use up to 10GB when processing large panels.

Optionally, pynad's performance will improve if a command line compression utility is available.

************************
Using pynad as a package
************************
Pynad can be imported as a Python package. All public classes, functions and methods have descriptive docstrings (in Portuguese). See the file **pynad.py** for examples.

***********
Performance
***********
IBGE disseminates microdata in text files with fixed width field records. Pynad does not load the content of the original microdata files as numeric data types. It operates with text records converted to comma separated values. Handling, writing and compressing text files, particularly those with lenghty records, takes time. The command **painel-mnt** might take 10-15 minutes to process a panel. In the first use, some hours will be required to process the more than 30 panels available. *Cythonizing* some modules can speed up the process, though not much.

Archives with compressed files have one major drawback: there is no fast and safe way to delete a compressed file. Compression utilities that offer a delete option actually replace the archive by a new one excluding the "deleted" files. Therefore, it takes more time to delete a small file from a large archive than to delete a large file.

The standard Python package `zipfile <https://docs.python.org/3/library/zipfile.html?highlight=zipfile#module-zipfile>`_ does not have a method to delete files. Although it can be easily implemented - write a temporary archive excluding the undesirable files, exclude the old archive, and rename the temporary archive to replace it - its performance is very bad when compared to that of compression utilities such as `zip <http://infozip.sourceforge.net/Zip.html>`_ or `7zip <https://www.7-zip.org/>`_. In Linux, usually **zip** is already installed or is available in the software repositories, and **7zip** can be installed using the **p7zip-full** package. Windows users must make sure the utilitiy is on the system PATH.

Pynad will try to subprocess **zip** or **7zip** to delete files from the archives. If none is found, pynad will resort to the standard library to remove outdated files from the archives.

------------
Instructions
------------
Pynad is a command line application. It will create and update archives in the **current working directory**. After opening a terminal, or command prompt, the user should ascertain the current working directory is the desired one; if not, use **cd** to change it.

Pynad takes keywords as options. In a terminal, type **pynad** and press enter to show the keywords and what they command (in Portuguese)::

    Uso:  pynad COMANDO

      COMANDO pode ser:

        pnad        criar/sincronizar uma cópia da PNAD Anual
        pnadc       criar/sincronizar uma cópia da PNAD Contínua
        metadados   gerar metadados
        microdados  gerar microdados em formato csv
        painel-sep  separar painéis
        painel-id   identificar painéis
        painel-mnt  montar painéis identificados
        pnadc-tudo  pnadc metadata microdata painel-sep|id|mnt

When used for the first time, commands **pnad**, **pnadc**, **painel-sep** and **pnadc-tudo** will create compressed **zip** archive files in the current working directory:

   * pnad creates *copia.ibge.pnad.zip*
   * pnadc creates *copia.ibge.pnadc.zip*
   * painel-sep creates *paineis.ibge.pnadc.zip*
   * pnadc-tudo creates *copia.ibge.pnadc.zip* and *paineis.ibge.pnadc.zip*

The other commands will seek these archive files.

After the first use, pynad will only update the archives when IBGE releases new microdata and metadata, or patches previously released files.

****
pnad
****
Most of pynad's functionalities are for the ongoing **PNADC**. However, pynad can create and sync a local copy of the *Microdados* folder of the discontinued **PNAD**, fielded from 1976 to 2015::

    pynad pnad

This command will create or update *copia.ibge.pnad.zip* in the current working directory.

The number of files and download size will be shown, and pynad will ask before downloading from IBGE's `FTP server <ftp://ftp.ibge.gov.br/>`_.

Original files will be in the *original/pnad* folder in *copia.ibge.pnad.zip*.

**********
pnadc-tudo
**********
Pynad was devised to be as simple as possible. The full suite of options for the **PNADC** can be evoked with a single command. Open a terminal, make sure the current working directory is the desired one and type::

    pynad pnadc-tudo

In the first use, pynad will take about 8-10 hours to download all files, prepare them, and process the more than 30 panels available. After that, updates will be quick, if done frequently.

No questions will be asked: as long as the computer does not shutdown or sleep, no user interaction is needed.

This command is equivalent to::

    pynad pnadc
    pynad metadados
    pynad microdados
    pynad painel-sep
    pynad painel-id
    pynad painel-mnt

*****
pnadc
*****
Create and/or sync a local copy of the **PNADC**::

    pynad pnadc

This command will create or update *copia.ibge.pnadc.zip* in the current working directory. 

The number of files and download size will be shown, and pynad will ask before downloading from IBGE's `FTP server <ftp://ftp.ibge.gov.br/>`_.

Original files will be in the *original/pnadc_anual* and *original/pnadc_trimestral* folders in *copia.ibge.pnadc.zip*.

*********
metadados
*********
**Use after** pynad pnadc

Organize and extract **PNADC** metadata::

    pynad metadados

This command will create or update the folder *metadata* in *copia.ibge.pnadc.zip*. The metadata folder contains:

   * copies of all original *dicionários de variáveis* (**xls** format)
   * **json** text files containing the list of original microdata and metadata files and pynad-generated files:

       * *microdados.pnadc.anual.json*
       * *microdados.pnadc.trimestral.json*

   * **json** text files with the metadata extracted from the *dicionários de variáveis*:

       * *variaveis.pnadc.trimestral.json*
       * *variaveis.pnadc.anual.trimestre{#}.json*
       * *variaveis.pnadc.anual.{ano}.visita{#}.json*

Each `variaveis.pnadc.*.json` metadata file contains a dictionary. The main key is IBGE's variable code, e.g. uf, v1008, v2005, v3001.

Each variable contains a dictionary describing it, which keys and values are:

   * **parte**: variable group, e.g. "parte 1 - identificação e controle"
   * **quesito**: for variables storing answers to questions, the sequential number of the question in the questionnaire; missing for questionnaire identification and control or calculated variables
   * **desc**: name or description  e.g. "unidade da federação" for uf
   * **periodo**: the availability period – e.g. "1o tri/2012 - atual"
   * **colunas**: position (columns) in the original fixed width record [first; last; lenght] e.g., for ano (year), first variable of the record, spanning 4 columns: [1, 4, 4]
   * **bytes**: bytes – 1, 2, 4 ou 8 – needed to store the variable as C signed integers, considering all its columns filled with 9s (9, 99, 999 etc.),  non-integer fields (weights only) are represented by 15 and require an 8 bytes float.
   * **valores**: for categorical values, a dictionary with the codes and short descriptions of the categories, e.g. for v2007 (gender) **valores** stores the dictionary {'1': 'homem', '2': 'mulher'}.

Using Python, a dictionary can be loaded directly from the archive::

    from json import loads
    from zipfile import ZipFile

    with ZipFile('copia.ibge.pnadc.zip') as src:
        dicvars = loads(src.read('metadados/variaveis.pnadc.trimestral.json'))

    # list all vars, code and name
    for var in dicvars:
        print(f"{var} - {dicvars[var]['desc']}")

    # list v2005 category codes and names
    for cat in dicvars['v2005']['valores']:
        print(f"{cat} - {dicvars['v2005']['valores'][cat]}")


**********
microdados
**********
**Use after** pynad pnadc and metadados

Convert **PNADC** microdata to csv::

    pynad microdados

This command will create or update the folder *microdata* in *copia.ibge.pnadc.zip*. The microdata folder contains:

   * **csv** microdata files named as:

     *microdados.pnadc.{trimestral | anual}.{ano}.{# | (visita# | trimestre#)}.csv*

     The header line has the variable codes and commas are used as delimiters. Change of delimiter is only possible using pynad as a Python package.

   * **json** text files containing the list of original microdata and metadata files, and pynad-generated files used to create the **csv** files:

       * *microdados.pnadc.anual.json*
       * *microdados.pnadc.trimestral.json*

**********
painel-sep
**********
**Use after** pynad pnadc, metadados and microdados

Separate **PNADC** panels::

    pynad painel-sep

This command will create or update *paineis.ibge.pnadc.zip* in the current working directory; and its *pessoas* folder. 

Pynad separates the finished panels available, retrieving their records from the cross-sectional datasets, generating a **csv** microdata file for each panel. These files have a long record, with all variables already released, and pynad will update them when new variables are released.

The *pessoas* folder contains:

   * unidentified panel **csv** microdata files named as:

     *microdados.pnadc.paineis.{ano#}.csv*

   * **json** text file containing the list of original microdata files used to create the panel **csv** files:

     *microdados.pnadc.paineis.json*

*********
painel-id
*********
**Use after** pynad pnadc, metadados, microdados and painel-sep

Identify **PNADC** panels::

    pynad painel-id

This command will create or update the *chaves* folder in *paineis.ibge.pnadc.zip*.

Pynad identifies households and individuals in each dwelling using gender, birthdate or estimated age, relation to household head and position in the household roster, generating one **csv** microdata file with the identification keys by panel. Those files have only keys, as they are meant to be joined one-to-one with their source panel files in the *pessoas* folders.

The *chaves* folder contains:

   * panel identification keys **csv** microdata files named as:

     *pid{ano#}.csv*

   * **json** text file containing the list of original microdata files used to create the source panels in the *pessoas* folder:

     *microdados.pnadc.paineis.json*

**********
painel-mnt
**********
**Use after** pynad pnadc, metadados, microdados, painel-sep and painel-id

Assemble **PNADC** identified panels and add panel weights::

    pynad painel-mnt

This command will create or update the *individuos* folder in *paineis.ibge.pnadc.zip*.

Pynad joins the panels in the *pessoas* folders with their identification in the *chaves* folder.

Then it reshapes the resulting dataset, moving the interviews from rows to columns, generating individual records. Original variables from the basic questionnaire (applied in all visits) have five instances in the individual records, e.g. for literacy, v3001, the individual record has v3001_1, v3001_2, v3001_3, v3001_4, v3001_5.

After reshaping, it calculates and adds panel population weights to the records.

The records are split in variable blocks: basic, education, labour, income etc. A **csv** microdata file of individual records is created for each block of every panel.

The *individuos* folder contains:

   * identified panel thematic **csv** microdata files named as:

     *microdados.pnadc.paineis.{ano#}.{theme}.csv*

     where *theme* can be *basico*, *educa*, *trabalho*, *rendas*, *moradia*, *tics*, *turismo*, *derivadas* or *trabinfa* 

   * **json** text file containing the list of original microdata files used to create the source panels in the *pessoas* folder:

     *microdados.pnadc.paineis.json*


