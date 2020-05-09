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
"""

import sys, locale, codecs
from optparse import OptionParser


def main():
    usage = "usage: %prog [options] livre-journal.txt"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version, description=__doc__)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Vous devez passer en argument le chemin d'un fichier "
                     "Livre-Journal au format reStructuredText")
    else:
        import json
        from colbert.livre_journal import check_livre_journal
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

        livre_journal = codecs.open(args[0], mode="r", encoding="utf-8")
        result = check_livre_journal(livre_journal)
        for row in result:
            print('%s\t\t%s' % (row[1], row[0]))

if __name__ == "__main__":
    main()
