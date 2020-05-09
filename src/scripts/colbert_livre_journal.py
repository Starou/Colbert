#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Stanislas Guerra <stanislas.guerra@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Commande d'ajout d'entrées dans le livre journal par duplication d'écritures.
"""

import codecs
import copy
import datetime
import io
import locale
import os
import sys

from colbert.livre_journal import (livre_journal_to_list, ecritures_to_livre_journal,
                                   rechercher_ecriture, ajouter_ecriture, update_ecriture)
from colbert.utils import DATE_FMT
from optparse import OptionParser

LJ_PATH_ENV = "COLBERT_LJ_PATH"


def main():
    usage = (
        "usage: %prog [search|add][options]\n"
        "examples:\n"
        "\t%prog search `lowercase expression'\n"
        "\t%prog add --date=21/12/2014 from-last-entry-like=cojean\n"
        "\t%prog add --date=21/12/2014 from-last-entry-like=cojean -a 12.40\n"
        "\t%prog add --date=21/12/2014 from-last-entry-like=cojean -a '12.40,10.00,2.40'\n"
    )
    version = "%prog 0.9"
    parser = OptionParser(usage=usage, version=version, description=__doc__)
    parser.add_option("-l", "--livre-journal", dest="livre_journal_path",
                      default=os.environ.get(LJ_PATH_ENV),
                      help=("Chemin vers le fichier Livre Journal. "
                            "Par défaut : $%s" % LJ_PATH_ENV))
    parser.add_option("--dry-run", action="store_true", default=False,
                      help="Affiche l'entrée qui aurait été ajoutée.")
    parser.add_option("-o", "--output",
                      help=("Chemin vers le fichier livre-journal de destination. "
                            "Ecrase le fichier source si non-précisé."))
    parser.add_option("-d", "--date", default=datetime.date.today().strftime(DATE_FMT),
                      help="Date de l'entrée à ajouter (par défaut: %default)")
    parser.add_option("-a", "--amounts",
                      help=("Liste des montants des entrées/sorties (séparés par une virgule) "
                            "ou montant de l'entrée/sortie (si un seul compte de chaque côté). "
                            "Si non précisés, reprend les montants de l'écriture cible."))
    parser.add_option("-f", "--from-last-entry-like",
                      help=("Chemin vers le fichier Livre Journal. "
                            "Par défaut : $%s" % LJ_PATH_ENV))

    # Catch --help which does not play well with encoding.
    parser.parse_args()

    # Set encoding first.
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)
    for i, a in enumerate(sys.argv):
        sys.argv[i] = str(a.decode(encoding))

    (options, args) = parser.parse_args()

    if not len(args) or args[0] not in ['search', 'add']:
        parser.error("Vous devez passer une action en argument parmi [search|add].")
        return

    if not options.livre_journal_path:
        parser.error("Vous devez préciser le chemin vers le Livre Journal.\n"
                     "Option -l ou variable d'environnement $%s." % LJ_PATH_ENV)

    action = args[0]
    if action == 'search':
        try:
            expression = args[1]
        except IndexError:
            parser.error("Vous devez passer une expression de recherche en paramètre.")
    elif action == 'add':
        if not options.from_last_entry_like:
            parser.error("Vous devez passer une expression de recherche (option -f).")

    if action == 'search':
        rechercher(expression, options.livre_journal_path)
    elif action == 'add':
        ajouter(options)


def rechercher(expression, livre_journal_path):
    with io.open(livre_journal_path, mode="r", encoding="utf-8") as lj_file:
        lj_as_list = livre_journal_to_list(lj_file, string_only=True)
        filtered = rechercher_ecriture(expression, lj_as_list)
        lines = ecritures_to_livre_journal(list(filtered))
        print(lines)


def ajouter(options):
    with io.open(options.livre_journal_path, mode="r", encoding="utf-8") as lj_file:
        lj_as_list = livre_journal_to_list(lj_file, string_only=True)
        try:
            template_line = list(rechercher_ecriture(options.from_last_entry_like,
                                                     lj_as_list))[-1]
        except IndexError:
            print(("Aucune écriture trouvée avec l'intitulé "
                   "ressemblant à '%s'." % options.from_last_entry_like))
            return
        else:
            template_line = copy.deepcopy(template_line)

    amounts = options.amounts and options.amounts.split(",") or None

    update_ecriture(template_line, options.date, amounts)
    ajouter_ecriture(template_line, options.livre_journal_path, lj_as_list,
                     options.output, options.dry_run, verbose=True)


if __name__ == "__main__":
    main()
