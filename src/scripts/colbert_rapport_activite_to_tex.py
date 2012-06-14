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


import sys, locale, codecs
from optparse import OptionParser
import json

from colbert.utils import json_encoder
from colbert.rapports import rapport_activite_to_tex

def main():
    usage = "usage: %prog [options] rapport_activite.json modele-rapport.tex"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version, description=__doc__)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error(u"Vous devez passer en argument le chemin d'un fichier "
                     u"`rapport d\'activité' au format JSON et un modèle de "
                     u"rapport au format LaTeX.")
    else:
        locale.setlocale(locale.LC_ALL, '')
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

        activite = json.loads(codecs.open(args[0], mode="r", encoding="utf-8").read())
        template = codecs.open(args[1], mode="r", encoding="utf-8")
        rapport_activite_to_tex(activite, template, sys.stdout)

if __name__ == "__main__":
    main()
