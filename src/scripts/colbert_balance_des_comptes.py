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
    
"""

import sys, locale, codecs
from optparse import OptionParser
import datetime
from decimal import Decimal


def main():
    usage = "usage: %prog [options] grand-livre.json"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version, description=__doc__)

    parser.add_option("-l", "--label", dest="label", default="Balance des comptes", 
                      help=u"Titre à faire apparaitre sur la balance des comptes")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Vous devez passer en argument le chemin d'un fichier "
                     "Grand-Livre au format JSON.")
    else:
        import json
        from colbert.utils import json_encoder
        from colbert.balance_des_comptes import balance_des_comptes
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

        grand_livre = json.loads(codecs.open(args[0], mode="r", encoding="utf-8").read())
        bdc = balance_des_comptes(grand_livre, options.label)
        
        json.dump(bdc, sys.stdout, default=json_encoder, indent=4)

if __name__ == "__main__":
    main()
