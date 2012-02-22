# -*- coding: utf-8 -*-

from decimal import Decimal
from colbert.livre_journal import livre_journal_to_list
from colbert.livre_journal import ECRITURES, NOM_COMPTE, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT
from colbert.utils import DATE_FMT
from colbert.common import (DEBIT, CREDIT, SOLDE_DEBITEUR, SOLDE_CREDITEUR, DATE, DATE_DEBUT, DATE_FIN,
                            LABEL, INTITULE, NOM)

DATE_LEN = 12
LIBELLE_LEN = 45
DEBIT_LEN = 15
CREDIT_LEN = 15


def grand_livre(livre_journal_file, label, date_debut, date_fin,
                 grand_livre_precedent):
    """ 
    return = {
        'label': 'Grand-Livre 2011',
        'date_debut': datetime.date(2011, 4, 1),
        'date_fin': datetime.date(2011, 12, 31),
        'comptes': {
            u'4111-cli1': {
               'nom': u'Clients - ventes de biens ou prestations de services',
               'solde_crediteur': Decimal('0.00'),
               'solde_debiteur': Decimal('11960.00'),
               'total_credit': Decimal('0.00'),
               'total_debit': Decimal('11960.00'),
               'ecritures': [{'date': datetime.date(2011, 5, 6),
                              'debit': Decimal('4186'),
                              'intitule': u'Facture 2011-04 AdenClassifieds Prestation AdenPublish/Pages avril 2011'},
                             {'date': datetime.date(2011, 6, 3),
                              'debit': Decimal('7774'),
                              'intitule': u'Facture 2011-05 AdenClassifieds Prestation AdenPublish/Pages mai 2011'}]
            },
            ...
        }
    }
    """
    
    comptes = {}
    grand_livre = {
        LABEL: label,
        DATE_DEBUT: date_debut,
        DATE_FIN: date_fin,
        'comptes': comptes,
    }

    livre_journal = livre_journal_to_list(livre_journal_file)
    for ecriture in livre_journal:
        if date_debut <= ecriture[DATE] <= date_fin:
            for e in ecriture[ECRITURES]:
                if e[NUMERO_COMPTE_DEBIT]:
                    param, mvt = NUMERO_COMPTE_DEBIT, DEBIT
                elif e[NUMERO_COMPTE_CREDIT]:
                    param, mvt = NUMERO_COMPTE_CREDIT, CREDIT
                compte = comptes.setdefault(e[param], {NOM: e[NOM_COMPTE],
                                                       ECRITURES: []})
                compte[ECRITURES].append({DATE: ecriture[DATE], 
                                            INTITULE: ecriture[INTITULE],
                                            mvt: e[mvt]})
    
    # Calcul des soldes de chaque compte.
    for compte in comptes.values():
        compte['total_debit'] = reduce(lambda x, y: x+y, 
                                       [Decimal(e[DEBIT]) for e in \
                                            compte[ECRITURES] if e.has_key(DEBIT)],
                                       Decimal('0.00'))
        compte['total_credit'] = reduce(lambda x, y: x+y, 
                                        [Decimal(e[CREDIT]) for e in \
                                            compte[ECRITURES] if e.has_key(CREDIT)],
                                        Decimal('0.00'))

        compte[SOLDE_DEBITEUR] = compte['total_debit'] - compte['total_credit']
        if compte[SOLDE_DEBITEUR] < 0:
            compte[SOLDE_CREDITEUR] = -compte[SOLDE_DEBITEUR]
            compte[SOLDE_DEBITEUR] = Decimal('0.00')
        else:
            compte[SOLDE_CREDITEUR] = Decimal('0.00')
    return grand_livre 

def grand_livre_to_rst(grand_livre, output_file):
    """Convert a `grand_livre` json load to a RestructuredText file. """

    from colbert.utils import fmt_number, rst_table, rst_section, truncate_words
    from colbert.common import titre_principal_rst

    lines = []
    lines += titre_principal_rst(grand_livre[LABEL], grand_livre[DATE_DEBUT], grand_livre[DATE_FIN])
    
    def row(debit, credit):
        return [
            (debit and debit[0] or '', DATE_LEN),
            (debit and debit[1] or '', LIBELLE_LEN), 
            (debit and fmt_number(Decimal(debit[2])) or '', DEBIT_LEN), 
            (credit and credit[0] or '', DATE_LEN),
            (credit and credit[1] or '', LIBELLE_LEN), 
            (credit and fmt_number(Decimal(credit[2])) or '', CREDIT_LEN),
        ]

    table = []
    for numero_compte in sorted(grand_livre['comptes']):
        compte = grand_livre['comptes'][numero_compte]
        lines.append(rst_section(u"%s - *%s*" %(numero_compte, compte[NOM]), "'"))
        lines.append("\n")
        table.append([
            ("Date", DATE_LEN),
            (u"Libellé", LIBELLE_LEN), 
            (u"Débit", DEBIT_LEN), 
            ("Date", DATE_LEN),
            (u"Libellé", LIBELLE_LEN), 
            (u"Crédit", CREDIT_LEN),
        ])
        debits = [(e[DATE], e[INTITULE], e[DEBIT]) for e in compte[ECRITURES] if e.has_key(DEBIT)]
        credits = [(e[DATE], e[INTITULE], e[CREDIT]) for e in compte[ECRITURES] if e.has_key(CREDIT)]

        map(lambda d, c: table.append(row(d, c)), debits, credits)

        # Ligne du solde.
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])
        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        libelle_debit, libelle_credit = '', ''

        if not solde_debiteur and not solde_crediteur:
            libelle_debit = libelle_credit = u"*Compte soldé au %s.*" % grand_livre[DATE_FIN]
        elif solde_debiteur:
            libelle_credit = u"*Solde débiteur au %s*" % grand_livre[DATE_FIN]
        else:
            libelle_debit = u"*Solde créditeur au %s*" % grand_livre[DATE_FIN]

        table.append([
            ("", DATE_LEN),
            (libelle_debit, LIBELLE_LEN), 
            (solde_crediteur and '**%s**' % fmt_number(solde_crediteur) or '', DEBIT_LEN), 
            ("", DATE_LEN),
            (libelle_credit, LIBELLE_LEN), 
            (solde_debiteur and '**%s**' % fmt_number(solde_debiteur) or '', CREDIT_LEN),
        ])

        lines.append(rst_table(table))
        lines.append("\n.. raw:: latex\n\n    \\newpage\n")
        table = []

    output_file.write(u"\n".join(lines))
    output_file.write(u"\n")
    return output_file
