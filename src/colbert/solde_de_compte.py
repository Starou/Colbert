# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from .common import (DEBIT, CREDIT, DATE, DATE_DEBUT, DATE_FIN,
                     LABEL, INTITULE, NUMERO_COMPTE)
from .livre_journal import livre_journal_to_list
from .livre_journal import ECRITURES, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT
from .utils import fmt_number, rst_title, rst_section, rst_table
from .utils import DATE_FMT

SOLDE_TABLE_LEN = 134
DATE_LEN = 12
LIBELLE_LEN = 59
DEBIT_LEN = 12
CREDIT_LEN = 12
SOLDE_DEBIT_LEN = 17
SOLDE_CREDIT_LEN = 17


def solde_de_compte(livre_journal_file, output_file, comptes=None):
    """ Calcule le solde des comptes à partir du livre-journal.

    Utilisé dans le rapprochement d'écritures (ex: relevés bancaire
    vs livre-journal).

    comptes: Liste de comptes et des soldes attendus
        pour une ou plusieurs périodes.
        ex: [
              {
                  'numero_compte': "512",
                  'journaux': [
                      {
                          'label': "Avril 2011",
                          'date_debut': "01/04/2011",
                          'date_fin': "02/05/2011",
                          'debit_initial': "0.00",
                          'credit_initial': "0.00",
                          'debit_final': "1485.93",
                          'credit_final': "0.00",
                      },
                      {
                          'label': "Mai 2011",
                          'date_debut': "03/05/2011",
                          'date_fin': "01/06/2011",
                          'debit_initial': "1485.93",
                          'credit_initial': "0.00",
                          'debit_final': "1461.94",
                          'credit_final': "0.00",
                      },
                  ]
              }
          ]

    """

    lines = []
    livre_journal = livre_journal_to_list(livre_journal_file)
    for compte in comptes:
        lines.append(rst_title("Compte n°%s en Euros" % compte[NUMERO_COMPTE]))
        lines.append("\n")
        table = []
        for journal in compte['journaux']:
            lines.append(rst_section(journal[LABEL], "'"))
            # Header.
            table.append([("Date", DATE_LEN), ("Libellé", LIBELLE_LEN), ("Débit", DEBIT_LEN), ("Crédit", CREDIT_LEN),
                          ("Solde débiteur", SOLDE_DEBIT_LEN), ("Solde créditeur", SOLDE_CREDIT_LEN)])

            # Solde initial.
            solde_debiteur = Decimal(journal["debit_initial"])
            solde_crediteur = Decimal(journal["credit_initial"])
            solde = solde_crediteur and -(solde_crediteur) or solde_debiteur

            table.append([
                (journal[DATE_DEBUT], DATE_LEN),
                ("Report à nouveau", LIBELLE_LEN),
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
                                          (" - ".join([i.strip() for i in ecriture[INTITULE]]), LIBELLE_LEN),
                                          (e[DEBIT] and fmt_number(e[DEBIT]) or '', DEBIT_LEN),
                                          (e[CREDIT] and fmt_number(e[CREDIT]) or '', CREDIT_LEN),
                                          (solde_debiteur and fmt_number(solde_debiteur) or '', SOLDE_DEBIT_LEN),
                                          (solde_crediteur and fmt_number(solde_crediteur) or '', SOLDE_CREDIT_LEN)])

            # Ligne du solde pour la période.
            solde = solde_debiteur or solde_crediteur
            type_solde = solde_debiteur and "débiteur" or (solde_crediteur and "créditeur" or "soldé")

            solde_debiteur_final = Decimal(journal['debit_final'])
            solde_crediteur_final = Decimal(journal['credit_final'])

            solde_final = solde_debiteur_final or solde_crediteur_final
            type_solde_final = solde_debiteur_final and "débiteur" or (solde_crediteur_final and "créditeur" or "soldé")

            solde_is_ok = False
            if (solde == solde_final) and (type_solde == type_solde_final):
                solde_is_ok = True

            last_row = "Solde final calculé (*%s €*, %s) %s solde final attendu (*%s €*, %s)%s" % (
                fmt_number(solde),
                type_solde,
                solde_is_ok and "*identique* au" or "**différent** du",
                fmt_number(solde_final),
                type_solde_final,
                "" if solde_is_ok else " : %s €" % fmt_number(solde - solde_final)
            )
            lines.append(rst_table(table))
            lines.append(rst_table([[(last_row, SOLDE_TABLE_LEN)]]))
            lines.append("\n.. raw:: latex\n\n    \\newpage\n")
            table = []

    output_file.write("\n".join(lines))
    output_file.write("\n")
    return output_file
