=======
Colbert
=======

.. image:: https://coveralls.io/repos/Starou/Colbert/badge.png
  :target: https://coveralls.io/r/Starou/Colbert

.. image:: https://img.shields.io/pypi/v/colbert.svg
  :target: https://pypi.python.org/pypi/Colbert

.. image:: https://img.shields.io/pypi/pyversions/colbert.svg
    :target: https://pypi.python.org/pypi/Colbert/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/colbert.svg
    :target: https://pypi.python.org/pypi/Colbert/
    :alt: License

.. image:: https://api.travis-ci.org/Starou/Colbert.svg
    :target: https://travis-ci.org/Starou/Colbert
    :alt: Travis C.I.

*Colbert* is not about this douche `Stephen Colbert <https://www.rt.com/usa/507821-barack-obama-stephen-colbert-interview/>`_.
It is serious matter.

The name is a tribute to `Jean-Baptiste Colbert <http://en.wikipedia.org/wiki/Jean-Baptiste_Colbert>`_,
the Minister of Finances of France in the 17th century also known for being the
father of the modern accountancy.

Installation
============

.. code-block:: bash

    pip install Colbert

Functionalities
===============

Colbert helps you to manage your accountancy with a unique constraint: get your
*Livre Journal* (the book where you are supposed to daily register the financial
operations) up-to-date. That's it.

From that file it produce the annual reports (*Bilan*, *Compte de résultat* etc).
There are also some utilities to check your Livre-journal against the bank
reports, to generate invoices, activity report from *iCalendar* etc.

Disclaimer(s)
=============

This software has **not** been written by and /or with the help of an accountant
(and no accountant has been hurt during the process).

The concepts
============

Background
----------

I am running a small business since 2011 and from the start I decided to not
outsource the accountancy nor to use a commercial software.

Maybe I should have given `Gnucash <http://www.gnucash.org/>`_ but I decided to
be cheap on the technology side and to build a collection of utilities on the
fly as I was facing formalities.

*Colbert* is that very collection of tools working over organized and formated
text files (*reStructuredText* and *JSON*).
These tools produce other text files. Combined with LaTex (inside Makefile for
automation) you can produce beautiful documents.

::


                   colbert-scripts
    file-A.txt, ----------------->  file-C.txt
    file-B.json                        -
         -                             |
         |                             |
         | LaTex, etc.                 | LaTeX, etc.
         |                             |
         v                             v
    file-A.tex                       file-C.tex
    file-A.pdf
    file-A.ps


The core of accountancy is *le livre-journal*. This is our database where every
single operation occuring in your business is recorded. Each operation must be
balanced: the sum of the entries must be balanced by one or more output of the
same amount.

In large compagnies, this book is usualy splitted in several ones to regroup
operations by type.

The scaffold I use is the following::


    + MyBusiness/   +-- accountancy/    +-- livre-journal/  +-- livre-journal.txt
                                        |                   |
                                        |                   +-- Makefile
                                        |
                                        +-- 2011/   +-- grand-livre/
                                        |           |
                                        |           +-- releves-bancaires/
                                        |           |
                                        |           +-- factures/
                                        |           |
                                        |           +-- balance-des-comptes/
                                        |           |
                                        |           +-- bilan/
                                        |           |
                                        |           +-- compte-de-resultat/
                                        |           |
                                        |           +-- TVA/
                                        |           |
                                        |           +-- ecritures-de-cloture/
                                        |
                                        +-- 2012/   +-- grand-livre/
                                        |           |
                                        |           +-- releves-bancaires/
                                                    ...


*Le livre-journal* is a never-ending story, this is the reason for keeping it
at the root level. In accountancy, a main concept is *l'indépendance des
exercices comptables* which is why I have broken down my organization by year
(I am opening my accounts on Junary the 1st and closing them on December, 31th,
every year).

In each year directory reside sub-directories named with the tasks, books or
documents you have to deal with and produce all along the financial/fiscal year.

Almost every sub-directory should contain a Makefile to automatically call some
Colbert or LaTeX routines to update your files from the source (which may be
the *livre-journal*, the *Grand-livre* or the *Balance des comptes*).


In a nutshell, a typical usage at the end of a fiscal year is:

1. having a *Livre-journal* up-to-date and accurate ;
2. check your *relevés bancaires* (bank statement) against the Livre-journal.
   Go back to (1) if it is not the case ;
3. generate the *Grand-livre* as JSON from the Livre-journal ;
4. generate the *Balance des comptes* from the *grand_livre.json* file ;
5. compute the *Bilan* from  the *balance_des_comptes.json* file ;
6. compute the *Compte de résultat* from  the *balance_des_comptes.json* file ;
7. compute the *écritures de clôture* from  the *balance_des_comptes.json* file
   and write them back to the Livre-journal.

**Note** : each *JSON* file can be converted in a *reStructuredText* format
with a *colbert_\*_to_rst* script.

Le Livre-journal
----------------

The Livre-journal is a diary or a book where every flow of money is logged.
There is a tight legislation concerning those books in general and you must
refer yourself to the legislation of your country or juridiction.

In Colbert, this is a reStructuredText file meeting the french administration
requirements (the columns' width had been reduced to fit properly in this
document):

.. code-block:: rst

    ==================
    MyBusiness S.A.R.L
    ==================

    -------------
    Livre-Journal
    -------------

    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    | Date        |  N°compte débit | N°compte crédit |   Intitulé / nom du compte                      | Débit en €| Crédit en |
    +=============+=================+=================+=================================================+===========+===========+
    | *Mars 2011*                                                                                                               |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    || 18/03/2011 ||                ||                || Frais de constitution de la société CFE Paris. ||          ||          |
    ||            ||    6227        ||                || Achats - Frais d'actes et de contentieux       ||  80.00   ||          |
    ||            ||    44566       ||                || T.V.A. déductible sur autres biens et services ||  10.45   ||          |
    ||            ||                ||     455        ||     Associés - Comptes courants                ||          ||    90.45 |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    || 18/03/2011 ||                ||                || Frais de constitution de la société - Annonce  ||          ||          |
    ||            ||    6227        ||                || Achats - Frais d'actes et de contentieux       ||  80.00   ||          |
    ||            ||    44566       ||                || T.V.A. déductible sur autres biens et services ||  19.00   ||          |
    ||            ||                ||     455        ||     Associés - Comptes courants                ||          ||    99.00 |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    || 31/03/2011 ||                ||                || Facture 2011-01 MyClient1                      ||          ||          |
    ||            ||                ||                ||       Prestation MyClient1 mars 2011           ||          ||          |
    ||            ||    4111-CL1    ||                ||     Clients - ventes de biens ou prestations   ||  980.00  ||          |
    ||            ||                ||    706         ||      Produits - prestations de services        ||          ||  5 000.00|
    ||            ||                ||    44587       ||      Taxes sur le CA sur factures à établir    ||          ||  980.00  |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    | *Avril 2011*                                                                                                              |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+
    || 01/04/2011 ||                ||                || Résultat arrêté compte                         ||          ||          |
    ||            ||    6278-LCL    ||                || Autres frais de commission sur prestations     ||  48.00   ||          |
    ||            ||                ||     512        ||     Banques                                    ||          ||   48.00  |
    +-------------+-----------------+-----------------+-------------------------------------------------+-----------+-----------+



Each entry is a multiline row in the table.

I use *Line Blocks* to get a descent formatting in the multiline cells. Trying
to right-align the content of the two last columns was a failure.
In fact for a reason I don't get, if those values are not left-aligned,
the LaTeX conversion sucks.

The optional *thousand separator* cannot be anything else than a space
character at the moment. This is on the TODO list.

Adding entries
''''''''''''''

Editing the file can became cumbersome. To speed up this task you can use the
``colbert_livre_journal.py`` script to duplicate an entry:

.. code-block:: bash

    $ python colbert_livre_journal.py search cojean -l path/to/livre-journal.txt
    $ python colbert_livre_journal.py add -l path/to/livre-journal.txt -f cojean -d 14/09/2014 -a 13.50

Checking the Livre-journal
''''''''''''''''''''''''''

A first script allows you to check the entries balance of the book:

.. code-block:: bash

    $ colbert_check_livre_journal.py my_livre_journal.txt

My Makefile in the Livre-journal directory being:

.. code-block:: make

    FILENAME="livre-journal"

    all:	pdf

    pdf:	tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex
        @colbert_check_livre_journal.py $(FILENAME).txt

    tex:
        @rst2latex.py $(FILENAME).txt > $(FILENAME).tex

    purge:	clean
        @for ext in ".pdf" ".tex" ".txt"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tex.tmp"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

Computing VAT
'''''''''''''

The *colbert_solder_tva.py* script compute the flow of money on the VAT-related
accounts for a period of time and produce an JSON-entry to counter-balance
these entries. Then you (manually) copy/paste this entry in the Livre-journal.
Obviously, the JSON-entry need to be converted first in the reStructuredText
format of the Livre-journal with the *colbert_ecritures_to_livre_journal.py*
utility.

This is something you have to do every month or every quarter in France.

In the *TVA* directory:

.. code-block:: bash

    $ colbert_solder_tva ../../livre-journal/livre-journal.txt -d 01/03/2011 -f 30/9/2011 > solde-tva-sept-2011.json
    $ colbert_ecritures_to_livre_journal solde-tva-sept-2011.json > solde-tva-sept-2011.txt

Le Grand-livre
--------------

In that book are gathered the entries of the Livre-journal by account number
for a period of time (a fiscal year). One table for every single account.

Every account should start with the *report à nouveau* (the balance) of the
previous fiscal year.

To generate the Grand-livre, run the following:

.. code-block:: bash

    $ @colbert_grand_livre.py ../../livre-journal/livre-journal.txt --label="MyBusiness - Grand-Livre 2011" -d 1/1/2011 -f 31/12/2011 > grand-livre_2011.json

And then in reStructuredText:

.. code-block:: bash

    $ colbert_grand_livre_to_rst.py grand-livre_2011.json > grand-livre_2011.txt


Or in a Makefile:

.. code-block:: make

    FILENAME="grand_livre-2011"
    DATE_DEBUT="18/03/2011"
    DATE_FIN="31/12/2011"

    all:	pdf

    pdf:	tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex

    tex:	rst
        @rst2latex.py --table-style=booktabs $(FILENAME).txt >  $(FILENAME).tex.tmp
        @sed -E -f fix_table.sed < $(FILENAME).tex.tmp > $(FILENAME).tex

    rst:	json
        @echo "Conversion du grand livre au format reStructuredText..."
        @colbert_grand_livre_to_rst.py $(FILENAME).json > $(FILENAME).txt

    json:
        @echo "calcul du Grand-Livre..."
        @colbert_grand_livre.py ../../livre-journal/livre-journal.txt --label="MyBusiness - Grand-Livre 2011" -d $(DATE_DEBUT) -f $(DATE_FIN) > $(FILENAME).json

    purge:	clean
        @for ext in ".pdf" ".tex" ".txt"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tex.tmp"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

The *fix_table.sed* in the TeX conversion rule is a Sed script managing the
right-alignment of the money columns::

    s/\\begin{longtable\*}.*/\\newcolumntype{x}[1]{% \
    >{\\raggedleft\\hspace{0pt}}p{#1}}% \
    \\newcolumntype{y}[1]{% \
    >{\\raggedright\\hspace{0pt}}p{#1}}% \
    \\begin{longtable*}[c]{y{2cm}y{7.5cm}x{2cm}|y{2cm}y{7.5cm}x{2cm}}/
    s/&[[:space:]]+\\\\/\& \\tabularnewline/
    s/[[:space:]]+\\\\$/\\tabularnewline/

Here an example of the reStructuredText output:

.. code-block:: rst

    ================
    Grand-Livre 2011
    ================


    -----------------------------------
    Période du 01/03/2011 au 31/12/2011
    -----------------------------------



    100 - *Capital et compte de l'exploitant*
    '''''''''''''''''''''''''''''''''''''''''


    +------------+---------------------------------+-------------+------------+---------------------------------------+---------+
    | Date       | Libellé                         | Débit       | Date       | Libellé                               | Crédit  |
    +============+=================================+=============+============+=======================================+=========+
    |            |                                 |             | 02/04/2011 | Capital initial Dépôt de 1500 € par...| 1500.00 |
    +------------+---------------------------------+-------------+------------+---------------------------------------+---------+
    |            | *Solde créditeur au 31/12/2011* | **1500.00** |            |                                       |         |
    +------------+---------------------------------+-------------+------------+---------------------------------------+---------+

    .. raw:: latex

        \newpage


    4111-CL1 - *Clients - ventes de biens ou prestations de services*
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


    +------------+---------------------------------+----------+------------+-----------------------------------------+----------+
    | Date       | Libellé                         | Débit    | Date       | Libellé                                 | Crédit   |
    +============+=================================+==========+============+=========================================+==========+
    | 31/03/2011 | Facture 2011-01 MyClient1 ...   | 5980.00  | 02/09/2011 | Virement MyClient1 ZZZZZZZZZZZ Facture..| 5980.00  |
    +------------+---------------------------------+----------+------------+-----------------------------------------+----------+
    | 28/09/2011 | Facture 2011-04 MyClient1 ...   | 13156.00 | 01/12/2011 | Virement MyClient1 WWWWWWWWWW Facture...| 18538.00 |
    +------------+---------------------------------+----------+------------+-----------------------------------------+----------+
    | 01/11/2011 | Facture 2011-05 MyClient1 ...   | 5382.00  |            |                                         |          |
    +------------+---------------------------------+----------+------------+-----------------------------------------+----------+
    |            | *Compte soldé au 31/12/2011.*   |          |            | *Compte soldé au 31/12/2011.*           |          |
    +------------+---------------------------------+----------+------------+-----------------------------------------+----------+

    .. raw:: latex

N+1 years
'''''''''

When you start a new year there are two things to keep in mind for the
Grand-Livre:

- to start with the *Report à nouveau* of the account of the previous year ;
- to include the entries of the previous year that have not been included in
  the Grand-Livre.


*Colbert* does it for you. All you have to do is to provide the path of the
previous one (as JSON):

.. code-block:: bash

    $ @colbert_grand_livre.py ../../livre-journal/livre-journal.txt --label="MyBusiness - Grand-Livre 2012" \
        -d 1/1/2012 -f 31/12/2012 -p ../../2011/grand-livre/grand-livre_2011.json > grand-livre_2012.json

La balance des comptes
----------------------

The next financial piece is a single table regrouping the balance of the
accounts. It is computed from the Grand-livre for the sake of simplicity.

Again, you first generate a JSON file and then a reStructuredText file:

.. code-block:: bash

    $ colbert_balance_des_comptes.py ../grand-livre/grand_livre-2011.json \
        --label="MyBusiness - Balance des comptes 2011 en €"  > $balance-des-comptes.json
    $ colbert_balance_des_comptes_to_rst.py balance-des-comptes.json > balance-des-comptes.txt

And again, you should use this Makefile:

.. code-block:: make

    FILENAME="balance_des_comptes-2011"

    all:	pdf

    pdf:	tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex

    tex:	rst
        @rst2latex.py --table-style=booktabs $(FILENAME).txt >  $(FILENAME).tex.tmp
        @sed -E -f fix_table.sed < $(FILENAME).tex.tmp > $(FILENAME).tex

    rst:	json
        @echo "Conversion de la balance des comptes au format reStructuredText..."
        @colbert_balance_des_comptes_to_rst.py $(FILENAME).json > $(FILENAME).txt

    json:
        @echo "calcul de la balance des comptes..."
        @colbert_balance_des_comptes.py ../grand-livre/grand_livre-2011.json --label="MyBusiness - Balance des comptes 2011 en €"  > $(FILENAME).json

    purge:	clean
        @for ext in ".pdf" ".tex" ".txt"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tex.tmp"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

With the Sed fix::

    s/\\begin{longtable\*}.*/\\newcolumntype{x}[1]{% \
    >{\\raggedleft\\hspace{0pt}}p{#1}}% \
    \\newcolumntype{y}[1]{% \
    >{\\raggedright\\hspace{0pt}}p{#1}}% \
    \\begin{longtable*}[c]{y{2cm}y{8.5cm}x{2.2cm}x{2.2cm}x{2.2cm}x{2.2cm}}/
    s/} \\\\/} \\tabularnewline/
    s/&[[:space:]]+\\\\/\& \\tabularnewline/
    s/[[:space:]]+\\\\$/\\tabularnewline/

And here a example of the reStructuredText output (again, the table width had
been reduced here to fit well):

.. code-block:: rst

    =====================================
    Balance des comptes 2011 - MyBusiness
    =====================================


    -----------------------------------
    Période du 01/03/2011 au 31/12/2011
    -----------------------------------


    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | N°           | Libellé                                           | Total débit | Total crédit | Solde débit | Solde crédit|
    +==============+===================================================+=============+==============+=============+=============+
    | 100          | Capital et compte de l'exploitant                 |             | 1500.00      |             | 1500.00     |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 4111-CL1     | Clients - ventes de biens ou prestations de ser...| 24518.00    | 24518.00     |             |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 4111-CL2     | Clients - ventes de biens ou prestations de ser...| 1794.00     | 1794.00      |             |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 4111-CL3     | Clients - ventes de biens ou prestations de ser...| 8372.00     |              | 8372.00     |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 4181         | Clients - Factures à établir                      | 13156.00    |              | 13156.00    |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 44551        | TVA à décaisser                                   | 1240.00     | 4278.00      |             | 3038.00     |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 44566        | T.V.A. déductible sur autres biens et services    | 33.66       | 33.66        |             |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 44571        | T.V.A. Collectée                                  | 4312.00     | 4312.00      |             |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 44587        | Taxes sur le CA sur factures à établir            | 4312.00     | 7840.00      |             | 3528.00     |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 455          | Associés - Comptes courants                       |             | 189.45       |             | 189.45      |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 512          | Banques                                           | 27812.00    | 5132.65      | 22679.35    |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 60225        | Achats - Fournitures de bureau                    | 21.44       |              | 21.44       |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6227         | Achats - Frais d'actes et de contentieux          | 160.00      |              | 160.00      |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6278-LCL     | Autres frais de commission sur prestations de s...| 72.00       |              | 72.00       |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6411         | Charges - Salaires et appointements               | 3000.00     |              | 3000.00     |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6411-RSI     | Charges - cotisations RSI                         | 393.00      |              | 393.00      |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6411-URSF1   | Charges - cotisations URSSAF - Allocations famil..| 161.80      |              | 161.80      |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6411-URSF2   | Charges - cotisations URSSAF - CSG/RDS déducti... | 153.31      |              | 153.31      |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 6411-URSF3   | Charges - cotisations URSSAF - CSG/RDS non-dédu...| 86.89       |              | 86.89       |             |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 706          | Produits - prestations de services                |             | 40000.00     |             | 40000.00    |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    | 758          | Produits divers de gestion courante               |             | 0.34         |             | 0.34        |
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+
    |              | **Totaux**                                        | **89598.10**| **89598.10** | **48255.79**| **48255.79**|
    +--------------+---------------------------------------------------+-------------+--------------+-------------+-------------+

Le Bilan
--------

This document is a *résumé* or a «picture» of your business. It is generated
from the *Balance des comptes*:

.. code-block:: bash

    $ colbert_bilan.py ../balance-des-comptes/balance_des_comptes-2011.json \
        --label="MyBusiness - Bilan 2011 en €" > bilan.json
    $ colbert_bilan_to_rst.py bilan.json > bilan.txt

A Makefile to automatically do all the work:

.. code-block:: make

    FILENAME="bilan-2011"

    all:	pdf

    pdf:	tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex

    tex:	rst
        @rst2latex.py --table-style=booktabs --output-encoding=utf-8 $(FILENAME).txt >  $(FILENAME).tex.tmp
        @sed -E -f fix_table.sed < $(FILENAME).tex.tmp > $(FILENAME).tex

    rst:	json
        @echo "Conversion du bilan au format reStructuredText..."
        @colbert_bilan_to_rst.py $(FILENAME).json > $(FILENAME).txt

    json:
        @echo "calcul de la bilan..."
        @colbert_bilan.py ../balance-des-comptes/balance_des_comptes-2011.json \
            --label="MyBusiness - Bilan 2011 en €"  > $(FILENAME).json

    purge:	clean
        @for ext in ".pdf" ".tex" ".txt"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tex.tmp"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

And the Sed script::

    s/\\setlength{\\DUtablewidth}{\\linewidth}/\\setlength{\\tabcolsep}{25pt} \\setlength{\\extrarowheight}{4.5pt}/
    s/\\begin{longtable\*}.*/\\begin{longtable*}[c]{lrrr|lr}/


The reStructuredText output:

.. code-block:: rst

    =======================
    Bilan 2011 - MyBusiness
    =======================


    -----------------------------------
    Période du 01/04/2011 au 31/12/2011
    -----------------------------------


    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+
    | Actif                        | Brut             | Amortissement  | Net           | Passif                | Montant       |
    +==============================+==================+================+===============+=======================+===============+
    | **Actif_circulant**          |                  |                |               | **Capitaux_propres**  |               |
    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+
    | Client_et_comptes_rattaches  | 11960.00         |                | 11960.00      | Resultat              | 9922.65       |
    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+
    | Autres_creances              | 4.21             |                | 4.21          | **Dettes**            |               |
    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+
    |                              |                  |                |               | Autres_dettes         | 2041.56       |
    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+
    | *Total*                      | *11964.21*       | *0.00*         | **11964.21**  | *Total*               | **11964.21**  |
    +------------------------------+------------------+----------------+---------------+-----------------------+---------------+

Le compte de résultat
---------------------

The purpose of this last document is to give an idea of your activity during
the fiscal year:

.. code-block:: bash

    $ colbert_compte_de_resultat.py ../balance-des-comptes/balance_des_comptes-2011.json \
        --label="MyBusiness - Compte de résultat 2011 en €"  > compte-de-resultat.json
    $ colbert_compte_de_resultat_to_rst.py compte-de-resultat.json > compte-de-resultat.txt

In a Makefile:

.. code-block:: make

    FILENAME="compte_de_resultat-2011"

    all:	pdf

    pdf:	tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex
        @pdflatex $(FILENAME).tex

    tex:	rst
        @rst2latex.py --table-style=booktabs --output-encoding=utf-8 $(FILENAME).txt > $(FILENAME).tex.tmp
        @sed -E -f fix_table.sed < $(FILENAME).tex.tmp > $(FILENAME).tex

    rst:	json
        @echo "Conversion du compte de résultat au format reStructuredText..."
        @colbert_compte_de_resultat_to_rst.py $(FILENAME).json > $(FILENAME).txt

    json:
        @echo "calcul du compte de résultat..."
        @colbert_compte_de_resultat.py ../balance-des-comptes/balance_des_comptes-2011.json \
            --label="MyBusiness - Compte de résultat 2011 en €"  > $(FILENAME).json

    purge:	clean
        @for ext in ".pdf" ".tex" ".txt"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tex.tmp"; do\
            [ -e $(FILENAME)$${ext} ] && rm $(FILENAME)$${ext} || [ 1 ] ;\
        done

The Sed script::

    s/\\begin{longtable\*}.*/\\newcolumntype{x}[1]{% \
    >{\\raggedleft\\hspace{0pt}}p{#1}}% \
    \\newcolumntype{y}[1]{% \
    >{\\raggedright\\hspace{0pt}}p{#1}}% \
    \\begin{longtable*}[c]{y{8.5cm}x{2.2cm}|y{8.5cm}x{2.2cm}}/
    s/} \\\\/} \\tabularnewline/
    s/&[[:space:]]+\\\\/\& \\tabularnewline/
    s/[[:space:]]+\\\\$/\\tabularnewline/

The reStructuredText output:

.. code-block:: rst

    ====================================
    Compte de résultat 2011 - MyBusiness
    ====================================


    -----------------------------------
    Période du 01/03/2011 au 31/12/2011
    -----------------------------------


    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | Charges                         | Montant   | Produits                                         | Montant          |
    +=================================+===========+==================================================+==================+
    | *Charges d'exploitation*        |           | *Produits d'exploitation*                        |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | Rémunérations du personnel      | 3795.00   | Prestations de services                          | 40000.00         |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | Fournitures non stockables      | 21.44     | Autres produits de gestion courante              | 0.34             |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | Autres services extérieurs      | 232.00    |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | *Charges financières*           |           | *Produits financiers*                            |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | *Charges exceptionnelles*       |           | *Produits exceptionnels*                         |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    |                                 |           |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | **Sous-total charges**          | 4048.44   | **Sous-total produits**                          | 40000.34         |
    +---------------------------------+-----------+--------------------------------------------------+------------------+
    | **Résultat (bénéfice)**         | 35951.90  |                                                  |                  |
    +---------------------------------+-----------+--------------------------------------------------+------------------+

Managing the transition between 2 fiscal years
==============================================

When you have closed your fiscal year (say 2011) you have to create a new one
(2012). In Colbert, you create a new directory, *2012*, aside *2011*. You can
simply make a *cp 2011 2012*, then run the *make purge* rules in each
subdirectories and replace the dates and the filenames at the top of each
Makefile.

This may looks a bit awkward but this occurs only once a year!

Les écritures de clôture
------------------------

When a fiscal year is closed and when your documents and books are up-to-date
(*Grand-livre*, *Balance des comptes*, *Bilan* and *Compte de résultat*) you
have to insert in the Livre-journal the *écritures de clôture* (accounts
closing entries).  The purpose of these entries is:

1. to reset the *comptes de résultat* (in France, it is those having a number
   in *6xx* and *7xx*) ;
2. transfert the gain or the lost registred at the end of the fiscal year on
   the *comptes de bilan*.

Colbert comes with a script to compute such entries:

.. code-block:: bash

    $ colbert_ecritures_de_cloture.py ../balance-des-comptes/balance_des_comptes-2011.json > ecritures-de-cloture.json
    $ colbert_ecritures_to_livre_journal.py --label="Ecriture de cloture a reporter au Livre-journal" \
        ecritures-de-cloture.json > ecritures-de-cloture.txt


And copy/paste the body of *ecritures-de-cloture.txt* into the Livre-journal at
the right place.

Checking your account statements against the Livre-journal
==========================================================

There must be reciprocity between your account statements from your bank and
the entries in your Livre-journal.

Colbert is able to generate account statements for a bank account (say *512*)
and to check the balance against a JSON file representing the balances of each
account statement received from the bank establishment. Write such a file with
your text editor:

.. code-block:: json

    [
        {
            'numero_compte': "512",
            'journaux': [
                {
                    'label': "Avril 2011",
                    'date_debut': "01/04/2011",
                    'date_fin': "02/05/2011",
                    'debit_initial': "0.00",
                    'credit_initial': "0.00",
                    'debit_final': "1485.93",
                    'credit_final': "0.00",
                },
                {
                    'label': "Mai 2011",
                    'date_debut': "03/05/2011",
                    'date_fin': "01/06/2011",
                    'debit_initial': "1485.93",
                    'credit_initial': "0.00",
                    'debit_final': "1461.94",
                    'credit_final': "0.00",
                },
            ]
        }
    ]

And run *colbert_solde_de_compte.py ../../../livre-journal/livre-journal.txt solde.json*
which outputs:

.. code-block:: rst

    =====================
    Compte n°512 en Euros
    =====================


    Avril 2011
    ''''''''''
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    | Date       | Libellé                                               | Débit  | Crédit     | Solde débiteur| Solde créditeur|
    +============+=======================================================+========+============+===============+================+
    | 01/04/2011 | Report à nouveau                                      |        |            |               |                |
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    | 01/04/2011 | Résultat arrêté compte                                |        | 48.00      |               | 48.00          |
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    | 02/04/2011 | Capital initial Dépôt de 1500 € par Stanislas Guerra a| 1500.00|            | 1452.00       |                |
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    | 28/04/2011 | Cotisation Option PRO  LCL                            |        | 15.00      | 1437.00       |                |
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    | 02/05/2011 | Abonnement LCL Access                                 |        | 3.00       | 1434.00       |                |
    +------------+-------------------------------------------------------+--------+------------+---------------+----------------+
    +---------------------------------------------------------------------------------------------------------------------------+
    | Solde final calculé (*1434.00*, débiteur) *différent* du solde final attendu (*1485.93*, débiteur)                        |
    +---------------------------------------------------------------------------------------------------------------------------+

    .. raw:: latex

        \newpage

    Mai 2011
    ''''''''
    +------------+-------------------------------------------------------+------+------------+----------------+-----------------+
    | Date       | Libellé                                               | Débit| Crédit     | Solde débiteur | Solde créditeur |
    +============+=======================================================+======+============+================+=================+
    | 03/05/2011 | Report à nouveau                                      |      |            | 1485.93        |                 |
    +============+=======================================================+======+============+================+=================+
    +---------------------------------------------------------------------------------------------------------------------------+
    | Solde final calculé (*1485.93*, débiteur) *différent* du solde final attendu (*1461.94*, débiteur)                        |
    +---------------------------------------------------------------------------------------------------------------------------+

    .. raw:: latex

        \newpage

Making invoices
===============

Colbert can assist you to compute invoices, generate TeX/PDF outputs and the
Livre-journal entries from them.  You start with a JSON file like the one below
and use the script *colbert_calculer_facture.py* to fill it out:

.. code-block:: json

    {
        "client": {
            "nom": "MyClient#1",
                "adresse": "1, Infinite Loop",
                "code_postal": "11222",
                "ville": "Cupertino",
                "numero_compte": "4111-CL1",
                "nom_compte": "Clients - ventes de biens ou prestations de services",
                "reference_commande": "XXXXX"
        },
        "numero_facture": "YYYYYYY",
        "date_facture": "10/05/2011",
        "nb_jours_payable_fin_de_mois": "60",
        "taux_penalites": "11",
        "date_debut_execution": "10/04/2011",
        "date_fin_execution": "30/04/2011",
        "devise": "Euro",
        "symbole_devise": "€",
        "nom_compte": "Produits - prestations de services",
        "numero_compte": "706",
        "detail": [
            {
                "reference": "ref-A",
                "description": "Prestation A.",
                "prix_unitaire_ht": "100.00",
                "unite": "jours",
                "taux_tva": "19.6",
                "quantite": "4"
            },
            {
                "reference": "ref-B",
                "description": "Prestation B.",
                "prix_unitaire_ht": "450.99",
                "unite": "jours",
                "taux_tva": "19.6",
                "quantite": "11"
            }
        ],
        "deja_paye": "0.00"
    }

.. code-block:: bash

    $ colbert_calculer_facture.py my_invoice.json

Produce the following:

.. code-block:: json

    {
        "date_facture": "10/05/2011",
        "symbole_devise": "\u20ac",
        "deja_paye": "0.00",
        "taux_penalites": "11",
        "montant_ht": "5360.89",
        "date_fin_execution": "30/04/2011",
        "detail": [
            {
                "quantite": "4",
                "description": "Prestation A.",
                "reference": "ref-A",
                "montant_ht": "400.00",
                "prix_unitaire_ht": "100.00",
                "unite": "jours",
                "taux_tva": "19.6"
            },
            {
                "quantite": "11",
                "description": "Prestation B.",
                "reference": "ref-B",
                "montant_ht": "4960.89",
                "prix_unitaire_ht": "450.99",
                "unite": "jours",
                "taux_tva": "19.6"
            }
        ],
        "numero_facture": "YYYYYYY",
        "devise": "Euro",
        "nom_compte": "Produits - prestations de services",
        "numero_compte": "706",
        "client": {
            "ville": "Cupertino",
            "code_postal": "11222",
            "nom": "MyClient#1",
            "adresse": "1, Infinite Loop",
            "reference_commande": "XXXXX",
            "nom_compte": "Clients - ventes de biens ou prestations de services",
            "numero_compte": "4111-CL1"
        },
        "montant_ttc": "6411.62",
        "date_debut_execution": "10/04/2011",
        "reste_a_payer": "6411.62",
        "nb_jours_payable_fin_de_mois": "60",
        "date_debut_penalites": "01/08/2011",
        "tva": {
            "19.6": "1050.73"
        },
        "date_reglement": "31/07/2011"
    }


You should redirect the output to a new file, say *my_invoice_ok.json* and use
it to generate a LaTeX output:

.. code-block:: bash

    $ colbert_facture_to_tex.py my_invoice_ok.json my_invoice_template.tex > my_invoice.tex
    $ xelatex my_invoice.tex

The parameter *my_invoice_template.tex* is a TeX file having placeholder for
Python string formatting with keyword arguments.
There is an example of such template in the *tests/regressiontests/* folder.

Livre-journal entry
-------------------

Having an invoice filled-in you can now generate the entry for the
Livre-journal:

.. code-block:: bash

    $ colbert_ecriture_facture.py my_invoice_ok.json > my_invoice_entry.json
    $ colbert_ecritures_to_livre_journal.py --label="Entry to report" my_invoice_entry.json > my_invoice_entry.txt

Workflow
--------

My method is to use a directory for each invoice with the following Makefile in
it:

.. code-block:: make

    filename = facture-2012-003
    filename_calcule = $(filename)_calculee
    filename_ecriture = $(filename)_ecriture

    pdf:	tex
        @xelatex --papersize=a4 $(filename).tex
        @xelatex --papersize=a4 $(filename).tex
        @xelatex --papersize=a4 $(filename).tex

    tex:	json
        @export LC_ALL="fr_FR.UTF-8" ; export LC_LANG="fr_FR.UTF-8" ; \
        colbert_facture_to_tex.py $(filename_calcule).json ../../modele_facture.tex > $(filename).tex

    json:
        @colbert_calculer_facture.py $(filename).json > $(filename_calcule).json
        @colbert_ecriture_facture.py $(filename_calcule).json > $(filename_ecriture).json
        @colbert_ecritures_to_livre_journal.py --label="Ecriture a reporter au Livre-journal" \
            $(filename_ecriture).json > $(filename_ecriture).txt

    clean:
        @for ext in ".out" ".aux" ".log" ".tns"; do\
            [ -e $(filename)$${ext} ] && rm $(filename)$${ext} || [ 1 ] ;\
        done

Activity report from iCal
-------------------------

There is a template of LaTeX class in the *tex* directory. Again, I use a
Makefile (the same to generate the invoice associated with):

.. code-block:: make

    month = Juin
    month_index = 007
    year = 2012
    date_debut = 01/06/2012
    date_fin = 30/06/2012

    ref_facture = $(year)-$(month_index)

    filename = facture-$(ref_facture)
    filename_calcule = $(filename)_calculee
    filename_ecriture = $(filename)_ecriture

    rac_template = "rapport_activite-template.tex"
    rac_filename = rac-$(ref_facture)
    rac_label = "Rapport d'activité - $(month) $(year)"
    calendar = MyCalendar.ics

    all:	rac_pdf	facture_pdf

    facture_pdf:	facture_tex
        @xelatex --papersize=a4 $(filename).tex
        @xelatex --papersize=a4 $(filename).tex
        @xelatex --papersize=a4 $(filename).tex

    facture_tex:	facture_json
        @export LC_ALL="fr_FR.UTF-8" ; export LC_LANG="fr_FR.UTF-8" ; \
            colbert_facture_to_tex.py $(filename_calcule).json ../../modele_facture.tex > $(filename).tex

    facture_json:
        @colbert_calculer_facture.py $(filename).json > $(filename_calcule).json
        @colbert_ecriture_facture.py $(filename_calcule).json > $(filename_ecriture).json
        @colbert_ecritures_to_livre_journal.py --label="Ecriture a reporter au Livre-journal" \
            $(filename_ecriture).json > $(filename_ecriture).txt

    rac_pdf:	rac_tex
        @xelatex --papersize=a4 $(rac_filename).tex
        @xelatex --papersize=a4 $(rac_filename).tex
        @xelatex --papersize=a4 $(rac_filename).tex

    rac_tex:	rac_json
        @colbert_rapport_activite_to_tex.py $(rac_filename).json $(rac_template) > $(rac_filename).tex

    rac_json:
        @colbert_rapport_activite.py $(calendar) -d $(date_debut) -f $(date_fin) \
            -l $(rac_label) -r "$(ref_facture)" > $(rac_filename).json

    purge:	clean
        @for ext in ".tex" ".pdf" ; do\
            [ -e $(filename)$${ext} ] && rm $(filename)$${ext} || [ 1 ] ;\
            [ -e $(rac_filename)$${ext} ] && rm $(rac_filename)$${ext} || [ 1 ] ;\
        done

    clean:
        @for ext in ".out" ".aux" ".log" ".tns"; do\
            [ -e $(filename)$${ext} ] && rm $(filename)$${ext} || [ 1 ] ;\
            [ -e $(rac_filename)$${ext} ] && rm $(rac_filename)$${ext} || [ 1 ] ;\
        done

You should take a look in the *tests/regressiontests* directory to grab the
LaTeX template.

Working with LaTeX
==================

I convert my reStructuredText files using docutils' *rst2latex.py* with the
*--table-style=booktabs* option except for the Livre-journal.

Aside each Makefile in each directory (like *TVA* or *grand-livre*) there is a
docutils configuration file *docutils.conf* and a LaTeX stylesheet
*docutils.tex*.

Because I want to right-align some columns and because docutils does not
handle that, I process the LaTeX outputs with a bit of *Sed* before the PDF
conversion.

The docutils.conf file
----------------------

Always the same::

    [latex2e writer]
    documentclass: article
    documentoptions: 11pt,a4paper,landscape
    output-encoding: utf-8
    stylesheet: docutils.tex

The docutils.tex stylesheet
---------------------------

Almost always::

    \usepackage{fullpage}
    \usepackage[french]{babel}
    \usepackage{array}

If the LaTeX compiler complains about utf-8 you may add the *ucs* package.

You may want to precisely control the header and the footer with *fancyhdr*
package::

    \usepackage{fancyhdr}
    \fancyhf{}
    \pagestyle{fancy}
    \lhead{\large{MyBusiness S.A.R.L.}\\
    \normalsize my address\\
    zipcode City}
    \cfoot{Société à responsabilité limité au capital de XXXX Euros - YYY YYY YYY R.C.S. Paris}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0.4pt}

The Sed script
--------------

The idea is to change the table(s) declaration(s) to get columns with managed
width and alignment.

In the Makefile it looks like that:

.. code-block:: make

    tex:	rst
    	@rst2latex.py --table-style=booktabs $(FILENAME).txt >  $(FILENAME).tex.tmp
    	@sed -E -f fix_table.sed < $(FILENAME).tex.tmp > $(FILENAME).tex

The Sed script depends of the TeX file. Here an example::

    s/\\begin{longtable\*}.*/\\newcolumntype{x}[1]{% \
    >{\\raggedleft\\hspace{0pt}}p{#1}}% \
    \\newcolumntype{y}[1]{% \
    >{\\raggedright\\hspace{0pt}}p{#1}}% \
    \\begin{longtable*}[c]{y{2cm}y{7.5cm}x{2cm}|y{2cm}y{7.5cm}x{2cm}}/
    s/\\\\/\\tabularnewline/

And to force the *pagestyle* for the first one I sometimes add::

    s/\\maketitle/\\maketitle\
    \\thispagestyle{fancy}/

Tests
=====

.. code-block:: bash

    cd tests
    python runtests.py

Requirements
============

- Python 3.9+
- pytz
- Python Icalendar (https://github.com/collective/icalendar)
- Docutils (SVN)
- a *LaTex* suite if you want to render the reStructuredText in PDF
- Make
- Sed
