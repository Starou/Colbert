# -*- coding: utf-8 -*-

from decimal import Decimal

from colbert.livre_journal import livre_journal_to_list
from colbert.livre_journal import ECRITURES, NOM_COMPTE, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT

from colbert.utils import fmt_number, rst_table, rst_section, truncate_words
from colbert.utils import DATE_FMT

from colbert.common import titre_principal_rst
from colbert.common import (DEBIT, CREDIT, TOTAL_DEBIT, TOTAL_CREDIT, SOLDE_DEBITEUR, SOLDE_CREDITEUR,
                            DATE, DATE_DEBUT, DATE_FIN, LABEL, INTITULE, NOM, COMPTES)

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
    if grand_livre_precedent:
        comptes = init_comptes_grand_livre_avec_precedent(grand_livre_precedent,
                                                          date_debut)
    grand_livre = {
        LABEL: label,
        DATE_DEBUT: date_debut,
        DATE_FIN: date_fin,
        COMPTES: comptes,
    }

    livre_journal = livre_journal_to_list(livre_journal_file)
    for ecriture in livre_journal:
        if grand_livre_precedent and (grand_livre_precedent[DATE_DEBUT] <= ecriture[DATE] <= grand_livre_precedent[DATE_FIN]):
            # Certaines écritures sont passées en fin d'exercice N-1 lors de l'exercice N et
            # n'apparaissent donc pas dans le grand_livre N-1.
            for e in ecriture[ECRITURES]:
                if not ecriture_journal_in_grand_livre(e, ecriture[DATE], ecriture[INTITULE], grand_livre_precedent):
                    ajouter_ecriture_to_comptes(e, ecriture[DATE], ecriture[INTITULE], comptes)
        if date_debut <= ecriture[DATE] <= date_fin:
            for e in ecriture[ECRITURES]:
                ajouter_ecriture_to_comptes(e, ecriture[DATE], ecriture[INTITULE], comptes)
    
    # Calcul des soldes de chaque compte.
    for compte in comptes.values():
        compte[TOTAL_DEBIT] = reduce(lambda x, y: x+y, 
                                       [Decimal(e[DEBIT]) for e in \
                                            compte[ECRITURES] if e.has_key(DEBIT)],
                                       Decimal('0.00'))
        compte[TOTAL_CREDIT] = reduce(lambda x, y: x+y, 
                                        [Decimal(e[CREDIT]) for e in \
                                            compte[ECRITURES] if e.has_key(CREDIT)],
                                        Decimal('0.00'))

        compte[SOLDE_DEBITEUR] = compte[TOTAL_DEBIT] - compte[TOTAL_CREDIT]
        if compte[SOLDE_DEBITEUR] < 0:
            compte[SOLDE_CREDITEUR] = -compte[SOLDE_DEBITEUR]
            compte[SOLDE_DEBITEUR] = Decimal('0.00')
        else:
            compte[SOLDE_CREDITEUR] = Decimal('0.00')
    return grand_livre 

def ajouter_ecriture_to_comptes(ecriture_lj, date, intitule, comptes):
    ecriture_gdlivre, numero_compte = ecriture_ljournal_to_gdlivre(ecriture_lj, date, intitule)
    compte = comptes.setdefault(numero_compte, {
        NOM: ecriture_lj[NOM_COMPTE],
        ECRITURES: [],
    })
    compte[ECRITURES].append(ecriture_gdlivre)

def ecriture_ljournal_to_gdlivre(ecriture_lj, date, intitule):
    ecriture_gdlivre = {
    }
    if ecriture_lj[NUMERO_COMPTE_DEBIT]:
        numero_compte_key, mvt = NUMERO_COMPTE_DEBIT, DEBIT
    elif ecriture_lj[NUMERO_COMPTE_CREDIT]:
        numero_compte_key, mvt = NUMERO_COMPTE_CREDIT, CREDIT

    return ({
        DATE: date, 
        INTITULE: intitule,
        mvt: ecriture_lj[mvt],
    }, ecriture_lj[numero_compte_key])

def init_comptes_grand_livre_avec_precedent(grand_livre_precedent, date_report_a_nouveau):
    comptes = {}

    for numero_compte, compte_precedent in grand_livre_precedent["comptes"].iteritems():
        solde_debiteur = Decimal(compte_precedent[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte_precedent[SOLDE_CREDITEUR])
        value = Decimal("0.00")
        mvt = DEBIT
        if solde_debiteur != Decimal("0.00"):
            mvt = DEBIT
            value = solde_debiteur
        elif solde_crediteur != Decimal("0.00"):
            mvt = CREDIT
            value = solde_crediteur

        comptes[numero_compte] = {
            NOM: compte_precedent[NOM],
            ECRITURES: [
                {
                    DATE: date_report_a_nouveau,
                    INTITULE: u"Report à nouveau",
                    mvt: value,
                }
            ],
        }

    return comptes

def ecriture_journal_in_grand_livre(ecriture, date, intitule, grand_livre):
    ecriture_gdlivre, numero_compte = ecriture_ljournal_to_gdlivre(ecriture, date, intitule)
    compte = grand_livre[COMPTES].get(numero_compte)
    if not compte:
        return False
    for e in compte[ECRITURES]:
        if e == ecriture_gdlivre:
            return True
    return False

def grand_livre_to_rst(grand_livre, output_file):
    """Convert a `grand_livre` json load to a reStructuredText file. """

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
    for numero_compte in sorted(grand_livre[COMPTES]):
        compte = grand_livre[COMPTES][numero_compte]
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
