# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from colbert.utils import fmt_number, rst_table
from colbert.utils import DATE_FMT
from colbert.common import titre_principal_rst
from colbert.common import (DEBIT, CREDIT, TOTAL_DEBIT, TOTAL_CREDIT, SOLDE_DEBITEUR, SOLDE_CREDITEUR,
                            DATE_DEBUT, DATE_FIN, LABEL, NOM, NUMERO, COMPTES)

TOTAL_DEBITS = u'total_debits'
TOTAL_CREDITS = u'total_credits'
TOTAL_SOLDES_DEBITEURS = u'total_soldes_debiteurs'
TOTAL_SOLDES_CREDITEURS = u'total_soldes_crediteurs'

def balance_des_comptes(grand_livre, label="Balance des comptes"):
    """ Calcule la balance des comptes à partir du Grand-Livre.

    return = {
        'label': 'Balance des comptes',
        'date_debut': datetime.date(2011, 4, 1),
        'date_fin': datetime.date(2011, 12, 31),
        'total_soldes_crediteurs': Decimal('0.00'),
        'total_soldes_debiteurs': Decimal('11960.00'),
        'total_credits': Decimal('0.00'),
        'total_debits': Decimal('11960.00'),
        'comptes': [
            {
                'numero': '4111-cli1',
                'nom': u'Clients - ventes de biens ou prestations de services',
                'solde_crediteur': Decimal('0.00'),
                'solde_debiteur': Decimal('11960.00'),
                'total_credit': Decimal('0.00'),
                'total_debit': Decimal('11960.00'),
            },
            ...
        ]
    }
    """
    comptes = []
    balance = {
        LABEL: label,
        DATE_DEBUT: datetime.datetime.strptime(grand_livre[DATE_DEBUT], DATE_FMT).date(),
        DATE_FIN: datetime.datetime.strptime(grand_livre[DATE_FIN], DATE_FMT).date(),
        COMPTES: comptes,
        TOTAL_DEBITS: Decimal('0.00'),
        TOTAL_CREDITS: Decimal('0.00'),
        TOTAL_SOLDES_DEBITEURS: Decimal('0.00'),
        TOTAL_SOLDES_CREDITEURS: Decimal('0.00'),
    }

    for numero_compte in sorted(grand_livre[COMPTES]):
        compte = grand_livre[COMPTES][numero_compte]

        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])
        total_debit = Decimal(compte[TOTAL_DEBIT])
        total_credit = Decimal(compte[TOTAL_CREDIT])

        balance[TOTAL_DEBITS] += total_debit
        balance[TOTAL_CREDITS] += total_credit
        balance[TOTAL_SOLDES_DEBITEURS] += solde_debiteur
        balance[TOTAL_SOLDES_CREDITEURS] += solde_crediteur

        comptes.append({
            NUMERO: numero_compte,
            NOM: compte[NOM],
            SOLDE_DEBITEUR: solde_debiteur,
            SOLDE_CREDITEUR: solde_crediteur,
            TOTAL_DEBIT: total_debit,
            TOTAL_CREDIT: total_credit,
        })

    return balance

TABLE_LEN = 153
COMPTES_LEN = 79
TOTAUX_LEN = 33
SOLDES_LEN = 33
NUMERO_COMPTE_LEN = 14
LIBELLE_COMPTE_LEN = 67
DEBIT_LEN = 18
CREDIT_LEN = 18

def balance_des_comptes_to_rst(balance_des_comptes, output_file):
    """Convert a `balance_des_comptes` json load to a reStructuredText file. """

    lines = []
    lines += titre_principal_rst(balance_des_comptes[LABEL],
                                 balance_des_comptes[DATE_DEBUT], 
                                 balance_des_comptes[DATE_FIN])
    
    table = [
        # BUG dans la largeur du tableau pour conversion en PDF
        # [(u"**Comptes**", COMPTES_LEN), (u"**Totaux**", TOTAUX_LEN), (u"**Soldes**", SOLDES_LEN)],
        [(u"N°", NUMERO_COMPTE_LEN),
         (u"Libellé", LIBELLE_COMPTE_LEN), 
         (u"Total débit", DEBIT_LEN),
         (u"Total crédit", CREDIT_LEN),
         (u"Solde débit", DEBIT_LEN),
         (u"Solde crédit", CREDIT_LEN)]
    ]

    for compte in balance_des_comptes[COMPTES]:
        total_debit = Decimal(compte[TOTAL_DEBIT])
        total_credit = Decimal(compte[TOTAL_CREDIT])
        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])

        table.append([
            (compte[NUMERO], NUMERO_COMPTE_LEN), 
            (compte[NOM], LIBELLE_COMPTE_LEN), 
            (total_debit and fmt_number(total_debit) or '', DEBIT_LEN),
            (total_credit and fmt_number(total_credit) or '', CREDIT_LEN),
            (solde_debiteur and fmt_number(solde_debiteur) or '', DEBIT_LEN),
            (solde_crediteur and fmt_number(solde_crediteur) or '', CREDIT_LEN),
        ])

    # Dernière ligne de totaux.
    total_debits = Decimal(balance_des_comptes[TOTAL_DEBITS])
    total_credits = Decimal(balance_des_comptes[TOTAL_CREDITS])
    total_soldes_debiteurs = Decimal(balance_des_comptes[TOTAL_SOLDES_DEBITEURS])
    total_soldes_crediteurs = Decimal(balance_des_comptes[TOTAL_SOLDES_CREDITEURS])

    table.append([
        ('', NUMERO_COMPTE_LEN), 
        (u"**Totaux**", LIBELLE_COMPTE_LEN), 
        (total_debits and u"**%s**" % fmt_number(total_debits) or '', DEBIT_LEN),
        (total_credits and u"**%s**" % fmt_number(total_credits) or '', CREDIT_LEN),
        (total_soldes_debiteurs and u"**%s**" % fmt_number(total_soldes_debiteurs) or '', DEBIT_LEN),
        (total_soldes_crediteurs and u"**%s**" % fmt_number(total_soldes_crediteurs) or '', CREDIT_LEN),
    ])

    lines.append(rst_table(table))

    output_file.write(u"\n".join(lines))
    output_file.write(u"\n\n")

    return output_file
