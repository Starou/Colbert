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

u"""
Commande d'ajout d'entrées dans le livre journal par duplication d'écritures.
"""

import bisect
import codecs
import datetime
import io
import locale
import os
import sys

from colbert.common import DATE, NUMERO_LIGNE_ECRITURE_FIN
from colbert.livre_journal import (livre_journal_to_list, ecriture_to_livre_journal,
                                   ecritures_to_livre_journal, rechercher_ecriture)
from colbert.utils import rst_table_row
from colbert.utils import DATE_FMT
from optparse import OptionParser

LJ_PATH_ENV = "COLBERT_LJ_PATH"


def main():
    usage = (
        "usage: %prog [search|add][options]\n"
        "examples:\n"
        "\t%prog search `lowercase expression'\n"
        "\t%prog add --date=21/12/2014 from-last-entry-like=cojean\n"
    )
    version = "%prog 0.9"
    parser = OptionParser(usage=usage, version=version, description=__doc__)
    parser.add_option("-l", "--livre-journal", dest="livre_journal_path",
                      default=os.environ.get(LJ_PATH_ENV),
                      help=(u"Chemin vers le fichier Livre Journal. "
                            u"Par défaut : $%s" % LJ_PATH_ENV))
    parser.add_option("--dry-run", action="store_true", default=False,
                      help=u"Affiche l'entrée qui aurait été ajoutée.")
    parser.add_option("-o", "--output",
                      help=(u"Chemin vers le fichier livre-journal de destination. "
                            u"Ecrase le fichier source si non-précisé."))
    parser.add_option("-d", "--date", default=datetime.date.today().strftime(DATE_FMT),
                      help=u"Date de l'entrée à ajouter (par défaut: %default)")
    parser.add_option("-a", "--amounts",
                      help=(u"Montant(s) des débits et crédits pour chaque compte. "
                            u"Liste des montants entrées et des sorties ou montant "
                            u"de l'entrée/sortie (si un seul compte de chaque côté). "
                            u"Si non précisés, reprend les montants de l'écriture cible."))
    parser.add_option("-f", "--from-last-entry-like",
                      help=(u"Chemin vers le fichier Livre Journal. "
                            u"Par défaut : $%s" % LJ_PATH_ENV))

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

    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
    livre_journal_file = codecs.open(options.livre_journal_path,
                                     mode="r", encoding="utf-8")
    livre_journal = livre_journal_to_list(livre_journal_file, string_only=True)

    if action == 'search':
        rechercher(expression, livre_journal)
    elif action == 'add':
        ajouter(options, livre_journal)


def rechercher(expression, livre_journal):
    filtered = rechercher_ecriture(expression, livre_journal)
    lines = ecritures_to_livre_journal(list(filtered))
    print lines


def ajouter(options, livre_journal):
    try:
        template_line = list(rechercher_ecriture(options.from_last_entry_like, livre_journal))[-1]
    except IndexError:
        print (u"Aucune écriture trouvée avec l'intitulé "
               u"ressemblant à '%s'." % options.from_last_entry_like)
        return

    # Construction de l'écriture
    template_line[DATE] = options.date

    # Recherche du point d'insertion dans le livre-journal (trié par date).
    keys = [list(reversed(r[DATE].split("/"))) for r in livre_journal]
    index = bisect.bisect_right(keys, options.date)
    numero_ligne = livre_journal[index - 1][NUMERO_LIGNE_ECRITURE_FIN]

    # Insertion dans le livre-journal.
    lines, lines_to_add = None, None
    with io.open(options.livre_journal_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        lines_to_add = rst_table_row(ecriture_to_livre_journal(template_line),
                                     stroke_char="-", add_closing_stroke=False)
        lines_to_add = [u"%s%s" % (l, os.linesep) for l in lines_to_add]
        lines[numero_ligne:numero_ligne] = lines_to_add

    output = os.path.expanduser(options.output or options.livre_journal_path)
    if not options.dry_run:
        with io.open(output, mode="w+", encoding="utf-8") as f:
            f.writelines(lines)

    # Mise à jour du livre journal.
    print u"L'écriture suivante %s été ajoutée au Livre Journal '%s' à la ligne %d:" % (
        (options.dry_run and "aurait" or "a"), output, numero_ligne
    )
    print u"".join(lines_to_add)


if __name__ == "__main__":
    main()
