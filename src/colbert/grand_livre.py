# -*- coding: utf-8 -*-

from decimal import Decimal
from livre_journal import livre_journal_to_list

GD_LIVRE_TABLE_LEN = 149
DATE_FMT = "%d/%m/%Y"
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
        'label': label,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'comptes': comptes,
    }

    livre_journal = livre_journal_to_list(livre_journal_file)
    for ecriture in livre_journal:
        if date_debut <= ecriture['date'] <= date_fin:
            for e in ecriture["ecritures"]:
                if e['numero_compte_debit']:
                    param, mvt = 'numero_compte_debit', 'debit'
                elif e['numero_compte_credit']:
                    param, mvt = 'numero_compte_credit', 'credit'
                compte = comptes.setdefault(e[param], {'nom': e['nom_compte'],
                                                       'ecritures': []})
                compte['ecritures'].append({'date': ecriture['date'], 
                                            'intitule': ecriture['intitule'],
                                            mvt: e[mvt]})
    
    # Calcul des soldes de chaque compte.
    for compte in comptes.values():
        compte['total_debit'] = reduce(lambda x, y: x+y, 
                                       [Decimal(e['debit']) for e in \
                                            compte['ecritures'] if e.has_key('debit')],
                                       Decimal('0.00'))
        compte['total_credit'] = reduce(lambda x, y: x+y, 
                                        [Decimal(e['credit']) for e in \
                                            compte['ecritures'] if e.has_key('credit')],
                                        Decimal('0.00'))

        compte['solde_debiteur'] = compte['total_debit'] - compte['total_credit']
        if compte['solde_debiteur'] < 0:
            compte['solde_crediteur'] = -compte['solde_debiteur']
            compte['solde_debiteur'] = Decimal('0.00')
        else:
            compte['solde_crediteur'] = Decimal('0.00')
    return grand_livre 

def grand_livre_to_rst(grand_livre, output_file):
    """Convert a `grand_livre` json load to a RestructuredText file. """

    from colbert.utils import fmt_number, rst_table, truncate_words
    from colbert.common import titre_principal_rst

    lines = []
    lines += titre_principal_rst(grand_livre["label"], grand_livre["date_debut"], grand_livre["date_fin"])
    
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
        table.append([
            (u"%s - *%s*" %(numero_compte, compte['nom']), GD_LIVRE_TABLE_LEN)
        ])
        table.append([
            ("*Date*", DATE_LEN),
            (u"*Libellé*", LIBELLE_LEN), 
            (u"*Débit*", DEBIT_LEN), 
            ("*Date*", DATE_LEN),
            (u"*Libellé*", LIBELLE_LEN), 
            (u"*Crédit*", CREDIT_LEN),
        ])
        debits = [(e['date'], e['intitule'], e['debit']) for e in compte['ecritures'] if e.has_key('debit')]
        credits = [(e['date'], e['intitule'], e['credit']) for e in compte['ecritures'] if e.has_key('credit')]

        map(lambda d, c: table.append(row(d, c)), debits, credits)

        # Ligne du solde.
        solde_crediteur = Decimal(compte['solde_crediteur'])
        solde_debiteur = Decimal(compte['solde_debiteur'])
        libelle_debit, libelle_credit = '', ''

        if not solde_debiteur and not solde_crediteur:
            libelle_debit = libelle_credit = u"*Compte soldé au %s.*" % grand_livre['date_fin']
        elif solde_debiteur:
            libelle_credit = u"*Solde débiteur au %s*" % grand_livre['date_fin']
        else:
            libelle_debit = u"*Solde créditeur au %s*" % grand_livre['date_fin']

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
