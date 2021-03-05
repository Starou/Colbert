# -*- coding: utf-8 -*-

import bisect
import datetime
import io
import os
import re
import sys
from decimal import Decimal
from .common import (DEBIT, CREDIT, SOLDE_DEBITEUR, SOLDE_CREDITEUR,
                     DATE, DATE_FIN, INTITULE, NOM, NUMERO, COMPTES,
                     NUMERO_LIGNE_ECRITURE_DEBUT, NUMERO_LIGNE_ECRITURE_FIN)
from .compte_de_resultat import COMPTES_DE_RESULTAT, COMPTES_DE_CHARGES, COMPTES_DE_PRODUITS
from .plan_comptable_general import PLAN_COMPTABLE_GENERAL as PCG
from .utils import fmt_number, parse_number, rst_table, rst_table_row, DATE_FMT

ECRITURES = 'ecritures'
NOM_COMPTE = 'nom_compte'
NUMERO_COMPTE_DEBIT = 'numero_compte_debit'
NUMERO_COMPTE_CREDIT = 'numero_compte_credit'


def check_livre_journal(livre_journal_file):
    """Vérifie l'équilibre de chaque écriture du Livre-Journal. """

    livre_journal = livre_journal_to_list(livre_journal_file)
    return [check_ecriture_livre_journal(e) for e in livre_journal]


def check_ecriture_livre_journal(ecriture):
    total_debit, total_credit = Decimal("0.0"), Decimal("0.0")
    check = ["%s - %s" % (ecriture[DATE].strftime(DATE_FMT),
                          ecriture[INTITULE][0])]
    for e in ecriture[ECRITURES]:
        if (e[DEBIT] and not e[NUMERO_COMPTE_DEBIT]) or (e[CREDIT] and not e[NUMERO_COMPTE_CREDIT]):
            check.append("ERREUR : incohérence entre les colonnes numéro de compte et montant")
            return check
        total_debit += e[DEBIT]
        total_credit += e[CREDIT]
    if total_debit == total_credit:
        check.append("OK : débit = crédit (%s)." % fmt_number(total_credit))
    else:
        check.append("ERREUR : débit (%s) != crédit (%s)." % (fmt_number(total_debit),
                                                              fmt_number(total_credit)))
    return check


def ecritures_de_cloture(balance_des_comptes):
    """Détermine les écritures à passer pour clôturer un exercice. """

    ecritures = {
        PCG['regroupement-charges'][NUMERO]: [],
        PCG['regroupement-produits'][NUMERO]: [],
    }

    # Préparation des sous-écritures à passer.
    for compte in balance_des_comptes[COMPTES]:
        if compte[NUMERO][0] not in COMPTES_DE_RESULTAT:
            continue
        if compte[NUMERO][0] == COMPTES_DE_PRODUITS:
            compte_cible = PCG['regroupement-produits'][NUMERO]
        elif compte[NUMERO][0] == COMPTES_DE_CHARGES:
            compte_cible = PCG['regroupement-charges'][NUMERO]

        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])

        if not solde_crediteur and not solde_debiteur:
            continue

        # On passe une écriture inverse.
        ecritures[compte_cible].append({
            DEBIT: solde_crediteur,
            CREDIT: solde_debiteur,
            NOM_COMPTE: compte[NOM],
            NUMERO_COMPTE_DEBIT: solde_crediteur and compte[NUMERO] or '',
            NUMERO_COMPTE_CREDIT: solde_debiteur and compte[NUMERO] or ''
        })

    # Création des écritures finales.
    ecritures_finales = []
    soldes_comptes_regroupements = {
        PCG['regroupement-produits'][NUMERO]: {
            DEBIT: Decimal("0.0"),
            CREDIT: Decimal("0.0"),
        },
        PCG['regroupement-charges'][NUMERO]: {
            DEBIT: Decimal("0.0"),
            CREDIT: Decimal("0.0"),
        }
    }

    for compte_regroupement, nom_compte in ((PCG['regroupement-produits'][NUMERO],
                                             PCG['regroupement-produits'][NOM]),
                                            (PCG['regroupement-charges'][NUMERO],
                                             PCG['regroupement-charges'][NOM])):
        ecriture_finale = {
            DATE: datetime.datetime.strptime(balance_des_comptes[DATE_FIN], DATE_FMT).date(),
            INTITULE: ["Ecritures de clôture des comptes."],
            ECRITURES: ecritures[compte_regroupement],
        }

        # Les écritures sont équilibrées aves les comptes 126/127.
        debit = Decimal("0.00")
        credit = Decimal("0.00")

        for e in ecritures[compte_regroupement]:
            debit += e[CREDIT]
            credit += e[DEBIT]

        if debit >= credit:
            debit = debit - credit
            credit = Decimal("0.0")
        elif debit < credit:
            credit = credit - debit
            debit = Decimal("0.0")

        ecriture_equilibre = {
            DEBIT: debit,
            CREDIT: credit,
            NOM_COMPTE: nom_compte,
            NUMERO_COMPTE_DEBIT: debit and compte_regroupement or '',
            NUMERO_COMPTE_CREDIT: credit and compte_regroupement or ''
        }

        # On respecte la règle du débit en premier dans une écriture.
        if debit:
            ecriture_finale[ECRITURES].insert(0, ecriture_equilibre)
        elif credit:
            ecriture_finale[ECRITURES].append(ecriture_equilibre)

        ecritures_finales.append(ecriture_finale)

        soldes_comptes_regroupements[compte_regroupement] = {
            DEBIT: debit,
            CREDIT: credit,
        }

    # Enregistrement du résultat net de l'exercice.
    ecriture_resultat = {
        DATE: datetime.datetime.strptime(balance_des_comptes[DATE_FIN], DATE_FMT).date(),
        INTITULE: ["Enregistrement du résultat net de l'exercice"],
        ECRITURES: [],
    }

    # On commence par solder les comptes de regroupement.
    for compte_regroupement, nom_compte in ((PCG['regroupement-produits'][NUMERO],
                                             PCG['regroupement-produits'][NOM]),
                                            (PCG['regroupement-charges'][NUMERO],
                                             PCG['regroupement-charges'][NOM])):
        soldes_compte_regroupement = soldes_comptes_regroupements[compte_regroupement]
        debit = soldes_compte_regroupement[CREDIT]
        credit = soldes_compte_regroupement[DEBIT]
        ecriture_resultat[ECRITURES].append(
            {
                DEBIT: debit,
                CREDIT: credit,
                NOM_COMPTE: nom_compte,
                NUMERO_COMPTE_DEBIT: debit and compte_regroupement or '',
                NUMERO_COMPTE_CREDIT: credit and compte_regroupement or ''
            }
        )

    # Que l'on équilibre avec les comptes 120 (bénéfice) ou 129 (perte).
    debit = soldes_comptes_regroupements[PCG['regroupement-produits'][NUMERO]][DEBIT] + \
        soldes_comptes_regroupements[PCG['regroupement-charges'][NUMERO]][DEBIT]

    credit = soldes_comptes_regroupements[PCG['regroupement-produits'][NUMERO]][CREDIT] + \
        soldes_comptes_regroupements[PCG['regroupement-charges'][NUMERO]][CREDIT]

    if debit >= credit:
        debit = debit - credit
        credit = Decimal("0.0")
    elif debit < credit:
        credit = credit - debit
        debit = Decimal("0.0")

    ecriture_equilibre = {
        DEBIT: debit,
        CREDIT: credit,
        NOM_COMPTE: debit and PCG['perte'][NOM] or PCG['benefice'][NOM],
        NUMERO_COMPTE_DEBIT: debit and PCG['perte'][NUMERO] or '',
        NUMERO_COMPTE_CREDIT: credit and PCG['benefice'][NUMERO] or ''
    }
    if debit:
        ecriture_resultat[ECRITURES].insert(0, ecriture_equilibre)
    elif credit:
        ecriture_resultat[ECRITURES].append(ecriture_equilibre)

    ecritures_finales.append(ecriture_resultat)

    return ecritures_finales


RX_DATE_INTITULE = re.compile(r"""^\|\|\s
                              (?P<date>\d\d/\d\d/\d\d\d\d)\s+\|\|
                              (?P<numero_compte_debit>\s+)\|\|
                              (?P<numero_compte_credit>\s+)\|\|
                              (?P<intitule>\s.+)\|\|
                              (?P<debit>\s+)\|\|
                              (?P<credit>\s+)\|
                              (?P<checked>[\w\s]+)\|
                              \s*$""", flags=(re.X | re.U))

RX_SUITE_INTITULE = re.compile(r"""^\|\|
                               (?P<date>\s+)\|\|
                               (?P<numero_compte_debit>\s+)\|\|
                               (?P<numero_compte_credit>\s+)\|\|
                               (?P<intitule>\s+.+)\|\|
                               (?P<debit>\s+)\|\|
                               (?P<credit>\s+)\|
                               (?P<checked>[\w\s]+)\|
                               \s*$""", flags=(re.X | re.U))

RX_ECRITURE = re.compile(r"""^\|\|
                         (?P<date>\s+)\|\|
                         (?P<numero_compte_debit>[\s\w-]+)\|\|
                         (?P<numero_compte_credit>[\s\w-]+)\|\|
                         \s+(?P<nom_compte>.+)\|\|
                         (?P<debit>[\d\s.]+)\|\|
                         (?P<credit>[\d\s.]+)\|
                         (?P<checked>[\w\s]+)\|
                         \s*$""", flags=(re.X | re.U))


def livre_journal_to_list(livre_journal_file, string_only=False):
    """
    return : [
      {'date': datetime.date(2011, 3, 31),
       'ecritures': [{'credit': Decimal('0.00'),
                      'debit': Decimal('5980'),
                      'nom_compte': u'Clients - ventes de biens ou prestations de services',
                      'numero_compte_credit': u'',
                      'numero_compte_debit': u'4111-cli1'},
                     {'credit': Decimal('5000'),
                      'debit': Decimal('0.00'),
                      'nom_compte': u'Produits - prestations de services',
                      'numero_compte_credit': u'706',
                      'numero_compte_debit': u''},
                     {'credit': Decimal('980'),
                      'debit': Decimal('0.00'),
                      'nom_compte': u'T.V.A. Collect\xe9e',
                      'numero_compte_credit': u'44571',
                      'numero_compte_debit': u''}],
       'intitule': u'Facture 2011-01 Client-1 Prestation Foo, mars 2011'},
       {...}, {...}, ...
    ]
    """

    livre_journal = []
    ecriture = {}
    for line_index, line in enumerate(livre_journal_file):
        if line[0] == '+':
            # Fin d'écriture.
            if ecriture:
                ecriture[NUMERO_LIGNE_ECRITURE_FIN] = line_index
                livre_journal.append(ecriture.copy())
                ecriture = {}
            # Début d'écriture.
            continue
        # Header
        elif line[0:2] == '| ':
            continue
        elif line[0:2] == '||':
            ecriture.setdefault(NUMERO_LIGNE_ECRITURE_DEBUT, line_index)
            # Première ligne d'écriture, doit indiquer la date et l'intitulé.
            if DATE not in ecriture:
                m = RX_DATE_INTITULE.match(line)
                if not m:
                    sys.stderr.write(line)
                    raise BaseException("La première ligne d'une écriture doit mentionner la date et l'intitulé.")
                m = m.groupdict()
                if string_only:
                    ecriture[DATE] = m[DATE]
                else:
                    try:
                        ecriture[DATE] = datetime.datetime.strptime(m[DATE], DATE_FMT).date()
                    except BaseException as e:
                        sys.stderr.write(line)
                        raise e
                ecriture[INTITULE] = [m[INTITULE].rstrip()]
                ecriture[ECRITURES] = []
            elif RX_SUITE_INTITULE.match(line):
                if ecriture[ECRITURES]:
                    raise BaseException("Les lignes supplémentaires d'intitulé doivent apparaitre exclusivement sous la première ligne.")
                m = RX_SUITE_INTITULE.match(line).groupdict()
                ecriture[INTITULE].append(m[INTITULE].rstrip())
            else:
                try:
                    m = RX_ECRITURE.match(line).groupdict()
                except BaseException as e:
                    sys.stderr.write("La ligne suivante n'est pas valide:\n%s" % line)
                    raise e
                m = dict([(k, v.strip()) for k, v in list(m.items())])
                sous_ecriture = {
                    NUMERO_COMPTE_DEBIT: m[NUMERO_COMPTE_DEBIT],
                    NUMERO_COMPTE_CREDIT: m[NUMERO_COMPTE_CREDIT],
                    NOM_COMPTE: m[NOM_COMPTE],
                    DEBIT: (m[DEBIT] or '0.00') if string_only else (Decimal(m[DEBIT].replace(' ', '') or '0.00')),
                    CREDIT: (m[CREDIT] or '0.00') if string_only else (Decimal(m[CREDIT].replace(' ', '') or '0.00')),
                }
                ecriture[ECRITURES].append(sous_ecriture)

    return livre_journal


LIVRE_JOURNAL_LEN = 153
DATE_LEN = 13
COMPTE_DEBIT_LEN = 17
COMPTE_CREDIT_LEN = 17
INTITULE_LEN = 62
DEBIT_LEN = 17
CREDIT_LEN = 17
CHECK_LEN = 4


def ecritures_to_livre_journal(ecritures, output_file=None, label="Ecritures pour le Livre-journal"):
    """Converti une liste d'écritures JSON dans le format reStructuredText du Livre-journal. """

    table = [[(label, LIVRE_JOURNAL_LEN)]]
    for ecriture in ecritures:
        table.append(ecriture_to_livre_journal(ecriture))

    lines = rst_table(table)

    if not output_file:
        return lines
    output_file.write(lines)
    output_file.write("\n\n")
    return output_file


def ecriture_to_livre_journal(ecriture, remove_lspace_intitule=False):

    def clean_intitule(text, remove_lspace_intitule):
        if remove_lspace_intitule and text[0] == ' ':
            text = text[1:]
        return text

    intitule = ecriture[INTITULE][0]

    multiline_row = [
        [
            (ecriture[DATE], DATE_LEN),
            ("", COMPTE_DEBIT_LEN),
            ("", COMPTE_CREDIT_LEN),
            (clean_intitule(ecriture[INTITULE][0], remove_lspace_intitule), INTITULE_LEN),
            ("", DEBIT_LEN),
            ("", CREDIT_LEN),
            ("", CHECK_LEN),
        ],
    ]
    # Lignes d'intitulés supp. si présentes.
    for intitule in ecriture[INTITULE][1:]:
        if remove_lspace_intitule and intitule[0] == ' ':
            del intitule[0]

        multiline_row.append(
            [
                ("", DATE_LEN),
                ("", COMPTE_DEBIT_LEN),
                ("", COMPTE_CREDIT_LEN),
                (clean_intitule(intitule, remove_lspace_intitule), INTITULE_LEN),
                ("", DEBIT_LEN),
                ("", CREDIT_LEN),
                ("", CHECK_LEN),
            ]
        )

    for e in ecriture[ECRITURES]:
        debit = Decimal(parse_number(e[DEBIT]))
        credit = Decimal(parse_number(e[CREDIT]))

        multiline_row.append(
            [
                ("", DATE_LEN),
                (debit and e[NUMERO_COMPTE_DEBIT] or "", COMPTE_DEBIT_LEN),
                (credit and e[NUMERO_COMPTE_CREDIT] or "", COMPTE_CREDIT_LEN),
                ("%s%s" % (credit and "    " or "", e[NOM_COMPTE]), INTITULE_LEN),
                (debit and fmt_number(debit) or "", DEBIT_LEN),
                (credit and fmt_number(credit) or "", CREDIT_LEN),
                ("", CHECK_LEN),
            ]
        )
    return multiline_row


def get_solde_compte(livre_journal, numero_compte, date_debut, date_fin):
    debit, credit = Decimal("0.00"), Decimal("0.00")
    for ecriture in livre_journal:
        if (date_debut <= ecriture[DATE] <= date_fin):
            for e in ecriture[ECRITURES]:
                if e[NUMERO_COMPTE_DEBIT] == numero_compte:
                    debit += e[DEBIT]
                elif e[NUMERO_COMPTE_CREDIT] == numero_compte:
                    credit += e[CREDIT]
        elif ecriture[DATE] > date_fin:
            break

    if debit > credit:
        debit = debit - credit
        credit = Decimal("0.00")
    elif credit > debit:
        credit = credit - debit
        debit = Decimal("0.00")
    else:
        debit, credit = Decimal("0.00"), Decimal("0.00")

    return debit, credit


def rechercher_ecriture(expression, livre_journal_as_list):
    return filter(lambda l: any([expression in i.lower() for i in l["intitule"]]), livre_journal_as_list)


def ajouter_ecriture(ecriture, livre_journal_path, livre_journal_as_list,
                     output=None, dry_run=False, verbose=False):
    # Recherche du point d'insertion dans le livre-journal (trié par date).
    keys = [sortable_date(r[DATE]) for r in livre_journal_as_list]
    index = bisect.bisect_right(keys, sortable_date(ecriture[DATE]))
    numero_ligne = livre_journal_as_list[index - 1][NUMERO_LIGNE_ECRITURE_FIN]

    # Ajout.
    lines, lines_to_add = None, None
    with io.open(livre_journal_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        lines_to_add = rst_table_row(ecriture_to_livre_journal(ecriture, True),
                                     stroke_char="-", add_closing_stroke=False)
        lines_to_add = ["%s%s" % (l, os.linesep) for l in lines_to_add]
        lines[numero_ligne:numero_ligne] = lines_to_add

    output = os.path.expanduser(output or livre_journal_path)
    if not dry_run:
        with io.open(output, mode="w+", encoding="utf-8") as f:
            f.writelines(lines)
    if verbose:
        print("L'écriture suivante %s été ajoutée au Livre Journal '%s' à la ligne %d:" % (
            (dry_run and "aurait" or "a"), output, numero_ligne
        ))
        print("".join(lines_to_add))


def update_ecriture(ecriture, date, montants=None):
    """
    o date = 'jj/mm/aaaa'
    o montant = ['debit1', 'debit2', ..., 'credit1', 'credit2', ...]
      Si toutes les lignes ont un montant identique, passer une liste
      avec cette seule valeur.
    """
    ecriture[DATE] = date

    if montants:
        for i, ligne_ecriture in enumerate(ecriture[ECRITURES]):
            try:
                montant = montants[i]
            except IndexError:
                montant = montants[0]
            for op in (DEBIT, CREDIT):
                if ligne_ecriture[op] != '0.00':
                    ligne_ecriture[op] = montant


def sortable_date(date_fr):
    """ '23/12/1977' -> ('1977', '12', '23') """
    return tuple(reversed(date_fr.split("/")))
