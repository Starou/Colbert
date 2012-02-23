# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from colbert.livre_journal import livre_journal_to_list
from colbert.livre_journal import ECRITURES, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT

from colbert.utils import fmt_number, rst_title, rst_section, rst_table
from colbert.utils import DATE_FMT

from colbert.common import (DEBIT, CREDIT, DATE, DATE_DEBUT, DATE_FIN, 
                            LABEL, INTITULE, NUMERO_COMPTE)

SOLDE_TABLE_LEN = 134
DATE_LEN = 12
LIBELLE_LEN = 59
DEBIT_LEN = 12
CREDIT_LEN = 12
SOLDE_DEBIT_LEN = 17
SOLDE_CREDIT_LEN = 17

def solde_de_compte(livre_journal_file, output_file, comptes=None):
    """ Calcule le solde des comptes à partir du livre-journal."""

    lines = []
    livre_journal = livre_journal_to_list(livre_journal_file)
    for compte in comptes:
        lines.append(rst_title(u"Compte n°%s en Euros" % compte[NUMERO_COMPTE]))
        lines.append(u"\n")
        table = []
        for journal in compte['journaux']:
            lines.append(rst_section(journal[LABEL], "'"))
            # Header.
            table.append([("Date", DATE_LEN), (u"Libellé", LIBELLE_LEN), (u"Débit", DEBIT_LEN), (u"Crédit", CREDIT_LEN),
                          (u"Solde débiteur", SOLDE_DEBIT_LEN), (u"Solde créditeur", SOLDE_CREDIT_LEN)])

            # Solde initial.
            solde_debiteur = Decimal(journal["debit_initial"])
            solde_crediteur = Decimal(journal["credit_initial"])
            solde = solde_crediteur and -(solde_crediteur) or solde_debiteur

            table.append([
                (journal[DATE_DEBUT], DATE_LEN),
                (u"Report à nouveau", LIBELLE_LEN),
                ('', DEBIT_LEN),
                ('', CREDIT_LEN),
                (solde_debiteur and fmt_number(solde_debiteur) or '', SOLDE_DEBIT_LEN),
                (solde_crediteur and fmt_number(solde_crediteur) or '', SOLDE_CREDIT_LEN)
            ])

            # Ajout des lignes du journal.
            date_debut = datetime.datetime.strptime(journal[DATE_DEBUT], DATE_FMT).date()
            date_fin = datetime.datetime.strptime(journal[DATE_FIN], DATE_FMT).date()
            for ecriture in livre_journal:
                if ecriture[DATE] < date_debut:
                    continue
                elif ecriture[DATE] > date_fin:
                    break
                else:
                    for e in ecriture[ECRITURES]:
                        if compte[NUMERO_COMPTE] in[e[NUMERO_COMPTE_DEBIT], e[NUMERO_COMPTE_CREDIT]]:
                            debit = e[DEBIT] and Decimal(e[DEBIT]) or Decimal("0.00")
                            credit = e[CREDIT] and Decimal(e[CREDIT]) or Decimal("0.00")

                            solde = solde + (debit or Decimal("0.00")) - (credit or Decimal("0.00"))
                            if solde >= Decimal("0.00"):
                                solde_debiteur, solde_crediteur = solde, Decimal("0.00")
                            else:
                                solde_debiteur, solde_crediteur = Decimal("0.00"), -(solde)

                            table.append([(ecriture[DATE].strftime(DATE_FMT), DATE_LEN),
                                          (ecriture[INTITULE], LIBELLE_LEN),
                                          (e[DEBIT] and fmt_number(e[DEBIT]) or '', DEBIT_LEN),
                                          (e[CREDIT] and fmt_number(e[CREDIT]) or '', CREDIT_LEN),
                                          (solde_debiteur and fmt_number(solde_debiteur) or '', SOLDE_DEBIT_LEN),
                                          (solde_crediteur and fmt_number(solde_crediteur) or '', SOLDE_CREDIT_LEN)])

            # Ligne du solde pour la période.
            solde = solde_debiteur or solde_crediteur
            type_solde = solde_debiteur and u"débiteur" or (solde_crediteur and u"créditeur" or u"soldé")

            solde_debiteur_final = Decimal(journal['debit_final'])
            solde_crediteur_final = Decimal(journal['credit_final'])

            solde_final = solde_debiteur_final or solde_crediteur_final
            type_solde_final = solde_debiteur_final and u"débiteur" or (solde_crediteur_final and u"créditeur" or u"soldé")
            
            solde_is_ok = False
            if (solde == solde_final) and (type_solde == type_solde_final):
                solde_is_ok = True

            last_row = u"Solde final calculé (*%s €*, %s) %s solde final attendu (*%s €*, %s)" % (
                fmt_number(solde), 
                type_solde, 
                solde_is_ok and u"*identique* au" or u"**différent** du",
                fmt_number(solde_final),
                type_solde_final,
            )
            lines.append(rst_table(table))
            lines.append(rst_table([[(last_row, SOLDE_TABLE_LEN)]]))
            lines.append("\n.. raw:: latex\n\n    \\newpage\n")
            table = []

    output_file.write(u"\n".join(lines))
    output_file.write(u"\n")
    return output_file
