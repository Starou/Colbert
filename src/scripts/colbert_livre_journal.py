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
Commande d'ajout d'entrées dans le livre journal par duplication.
"""

import codecs
import itertools
import json
import locale
import os
import sys

from colbert.livre_journal import livre_journal_to_list, ecritures_to_livre_journal
from colbert.utils import json_encoder
from optparse import OptionParser

LJ_PATH_ENV = "COLBERT_LJ_PATH"


def main():
    usage = ("usage: %prog [search|add][options]\n"
             "examples:\n"
             "\t%prog search `lowercase expression'")
    version = "%prog 0.9"
    parser = OptionParser(usage=usage, version=version, description=__doc__)
    parser.add_option("-l", "--livre-journal", dest="livre_journal_path",
                      default=os.environ.get(LJ_PATH_ENV),
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

    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

    livre_journal_file = codecs.open(options.livre_journal_path,
                                     mode="r", encoding="utf-8")
    livre_journal = livre_journal_to_list(livre_journal_file, string_only=True)

    if action == 'search':
        rechercher(expression, livre_journal)


def rechercher(expression, livre_journal):
    filtered = itertools.ifilter(lambda l: expression in l["intitule"].lower(),
                                 livre_journal)

    #print li
    #import pprint
    #pprint.pprint(list(filtered)[:1])
    #filtered_json = json.dumps(list(filtered), default=json_encoder)
    #print filtered_json
    lines = ecritures_to_livre_journal(list(filtered))
    lines_txt = u"\n".join(lines)
    print lines_txt
    #pprint.pprint(lines)
    #print u"\n".join(lines)


if __name__ == "__main__":
    main()
