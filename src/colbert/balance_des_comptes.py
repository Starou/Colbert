# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from colbert.utils import DATE_FMT
from colbert.common import DEBIT, CREDIT, DATE_DEBUT, DATE_FIN, LABEL


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
        'comptes': comptes,
        'total_debits': Decimal('0.00'),
        'total_credits': Decimal('0.00'),
        'total_soldes_debiteurs': Decimal('0.00'),
        'total_soldes_crediteurs': Decimal('0.00'),
    }

    for numero_compte in sorted(grand_livre['comptes']):
        compte = grand_livre['comptes'][numero_compte]

        solde_debiteur = Decimal(compte['solde_debiteur'])
        solde_crediteur = Decimal(compte['solde_crediteur'])
        total_debit = Decimal(compte['total_debit'])
        total_credit = Decimal(compte['total_credit'])

        balance['total_debits'] += total_debit
        balance['total_credits'] += total_credit
        balance['total_soldes_debiteurs'] += solde_debiteur
        balance['total_soldes_crediteurs'] += solde_crediteur

        comptes.append({
            'numero': numero_compte,
            'nom': compte['nom'],
            'solde_debiteur': solde_debiteur,
            'solde_crediteur': solde_crediteur,
            'total_debit': total_debit,
            'total_credit': total_credit,
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
    """Convert a `balance_des_comptes` json load to a RestructuredText file. """

    from colbert.utils import fmt_number, rst_table
    from colbert.common import titre_principal_rst

    lines = []
    lines += titre_principal_rst(balance_des_comptes["label"],
                                 balance_des_comptes["date_debut"], 
                                 balance_des_comptes["date_fin"])
    
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

    for compte in balance_des_comptes['comptes']:
        total_debit = Decimal(compte['total_debit'])
        total_credit = Decimal(compte['total_credit'])
        solde_debiteur = Decimal(compte['solde_debiteur'])
        solde_crediteur = Decimal(compte['solde_crediteur'])

        table.append([
            (compte['numero'], NUMERO_COMPTE_LEN), 
            (compte['nom'], LIBELLE_COMPTE_LEN), 
            (total_debit and fmt_number(total_debit) or '', DEBIT_LEN),
            (total_credit and fmt_number(total_credit) or '', CREDIT_LEN),
            (solde_debiteur and fmt_number(solde_debiteur) or '', DEBIT_LEN),
            (solde_crediteur and fmt_number(solde_crediteur) or '', CREDIT_LEN),
        ])

    # Dernière ligne de totaux.
    total_debits = Decimal(balance_des_comptes['total_debits'])
    total_credits = Decimal(balance_des_comptes['total_credits'])
    total_soldes_debiteurs = Decimal(balance_des_comptes['total_soldes_debiteurs'])
    total_soldes_crediteurs = Decimal(balance_des_comptes['total_soldes_crediteurs'])

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
