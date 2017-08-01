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


import argparse
import io
import os
import sys
from colbert.livre_journal import livre_journal_to_list, ecritures_to_livre_journal_md


def path(string):
    if not os.path.exists(string):
        msg = "%r does not exist" % string
        raise argparse.ArgumentTypeError(msg)
    return string


def main():
    parser = argparse.ArgumentParser(description="Convert a RestructuredText Livre Journal into Pandoc's MarkDown.",
            epilog='Generate PDF with `pandoc -f markdown+multiline_tables --variable geometry="margin=0.3cm" --variable fontfamily="ebgaramond-maths" livre-journal.md -o livre-journal.pdf`')
    parser.add_argument("--livre-journal", dest='livre_journal_path',
                        type=path, default=os.environ.get("COLBERT_LJ_PATH"))
    args = parser.parse_args()

    with io.open(args.livre_journal_path, mode="r", encoding="utf-8") as lj_file:
        ecritures = livre_journal_to_list(lj_file, string_only=True)
        lines = ecritures_to_livre_journal_md(ecritures)

    sys.stdout.writelines([l.encode('utf-8') + '\n' for l in lines])


if __name__ == "__main__":
    main()
