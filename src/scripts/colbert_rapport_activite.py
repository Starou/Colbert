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
Génère un fichier d'activité au format JSON à partir d'un calendrier iCal.

"""

import sys, locale, codecs
from optparse import OptionParser
import datetime
import json

from colbert.utils import DATE_FMT
from colbert.utils import json_encoder
from colbert.utils import decode_as_ecriture as as_ecriture


def main():
    usage = "usage: %prog [options] calendar.ics"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version, description=__doc__)

    parser.add_option("-l", "--label", dest="label", default=u"Rapport d\'activite", 
                      help=u"Titre à faire apparaitre sur le rapport")
    parser.add_option("-r", "--ref-facture", dest="ref_facture", default=u"Référence facture", 
                      help=u"Titre à faire apparaitre sur le rapport")
    parser.add_option("-d", "--date-debut", dest="date_debut", 
                      help=u"date de début de la période au format jj/mm/aaaa.")
    parser.add_option("-f", "--date-fin", dest="date_fin", 
                      help=u"date de fin de la période au format jj/mm/aaaa.")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error(u"Vous devez passer en argument le chemin d'un calendrier "
                     u"iCal.")
    else:
        from colbert.rapports import rapport_activite
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

        livre_journal = codecs.open(args[0], mode="r", encoding="utf-8")
        grand_livre_precedent = None
        date_debut = datetime.datetime.strptime(options.date_debut, DATE_FMT).date()
        date_fin = datetime.datetime.strptime(options.date_fin, DATE_FMT).date()

        calendrier = open(args[0], mode="r")
        rapport = rapport_activite(calendrier, 
                                   date_debut,
                                   date_fin,
                                   options.label,
                                   options.ref_facture)

        json.dump(rapport, sys.stdout, default=json_encoder, indent=4)

if __name__ == "__main__":
    main()
