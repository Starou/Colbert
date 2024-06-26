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


import sys
import json
from colbert.bilan import bilan
from colbert.utils import json_encoder
from optparse import OptionParser
from pathlib import Path


def main():
    usage = "usage: %prog [options] balance-des-comptes.json"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version, description=__doc__)

    parser.add_option("-l", "--label", dest="label", default="Bilan",
                      help="Titre à faire apparaitre sur le bilan")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Vous devez passer en argument le chemin d'un fichier "
                     "de balance des comptes au format JSON.")
    else:
        balance_des_comptes = json.loads(Path(args[0]).read_text())
        b = bilan(balance_des_comptes, options.label)
        json.dump(b, sys.stdout, default=json_encoder, indent=4)


if __name__ == "__main__":
    main()
