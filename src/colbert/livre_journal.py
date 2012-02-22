# -*- coding: utf-8 -*-

import re
import datetime
from decimal import Decimal
from colbert.utils import fmt_number, DATE_FMT
from colbert.common import DEBIT, CREDIT, DATE, INTITULE, NOM, NUMERO

ECRITURES = u'ecritures'

def check_livre_journal(livre_journal_file):
    """Vérifie l'équilibre de chaque écriture du Livre-Journal. """

    livre_journal = livre_journal_to_list(livre_journal_file)
    checks = []

    for ecriture in livre_journal:
        total_debit, total_credit = Decimal("0.0"), Decimal("0.0")
        check = [u"%s - %s" % (ecriture[DATE].strftime(DATE_FMT),
                               ecriture[INTITULE])]
        for e in ecriture[ECRITURES]:
            total_debit += e[DEBIT]
            total_credit += e[CREDIT]
        if total_debit == total_credit:
            check.append(u"OK : débit = crédit (%s)." % fmt_number(total_credit))
        else:
            check.append(u"ERREUR : débit (%s) != crédit (%s)." % (fmt_number(total_debit),
                                                                   fmt_number(total_credit)))
        checks.append(check)

    return checks
    

COMPTE_PERTE = '129'
COMPTE_BENEFICE = '120'
RESULTAT_EXERCICE_PERTE = u"résultat de l'exercice (perte)"
RESULTAT_EXERCICE_BENEFICE = u"résultat de l'exercice (bénéfice)"

COMPTE_REGROUPEMENT_PRODUITS = '127'
COMPTE_REGROUPEMENT_CHARGES = '126'
REGROUPEMENT_PRODUITS = u"Regroupement des comptes de produits"
REGROUPEMENT_CHARGES = u"Regroupement des comptes de charges"

def ecritures_de_cloture(balance_des_comptes):
    """Détermine les écritures à passer pour clôturer un exercice. """
    
    from colbert.compte_de_resultat import COMPTES_DE_RESULTAT, COMPTES_DE_CHARGES, COMPTES_DE_PRODUITS
    from colbert.bilan import DEBIT, CREDIT

    ecritures = {
        COMPTE_REGROUPEMENT_CHARGES: [],
        COMPTE_REGROUPEMENT_PRODUITS: [],
    }
    
    # Préparation des sous-écritures à passer.
    for compte in balance_des_comptes['comptes']:
        if compte[NUMERO][0] not in COMPTES_DE_RESULTAT:
            continue
        if compte[NUMERO][0] == COMPTES_DE_PRODUITS:
            compte_cible = COMPTE_REGROUPEMENT_PRODUITS
        elif compte[NUMERO][0] == COMPTES_DE_CHARGES:
            compte_cible = COMPTE_REGROUPEMENT_CHARGES

        solde_debiteur = Decimal(compte['solde_debiteur'])
        solde_crediteur = Decimal(compte['solde_crediteur'])

        if not solde_crediteur and not solde_debiteur:
            continue

        # On passe une écriture inverse.
        ecritures[compte_cible].append({
            DEBIT: solde_crediteur,
            CREDIT: solde_debiteur,
            'nom_compte': compte[NOM],
            'numero_compte_debit': solde_crediteur and compte[NUMERO] or u'',
            'numero_compte_credit': solde_debiteur and compte[NUMERO] or u'' 
        })
    
    # Création des écritures finales.
    ecritures_finales = []
    soldes_comptes_regroupements = {
        COMPTE_REGROUPEMENT_PRODUITS: {
            DEBIT: Decimal("0.0"),
            CREDIT: Decimal("0.0"),
        },
        COMPTE_REGROUPEMENT_CHARGES: {
            DEBIT: Decimal("0.0"),
            CREDIT: Decimal("0.0"),
        }
    }

    for compte_regroupement, nom_compte in ((COMPTE_REGROUPEMENT_PRODUITS, REGROUPEMENT_PRODUITS), 
                                            (COMPTE_REGROUPEMENT_CHARGES, REGROUPEMENT_CHARGES)):
        ecriture_finale = {
            DATE: datetime.datetime.strptime(balance_des_comptes['date_fin'], DATE_FMT).date(),
            INTITULE: u"Ecritures de clôture des comptes.",
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
            'nom_compte': nom_compte,
            'numero_compte_debit': debit and compte_regroupement or u'',
            'numero_compte_credit': credit and compte_regroupement or u'' 
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
        DATE: datetime.datetime.strptime(balance_des_comptes['date_fin'], DATE_FMT).date(),
        INTITULE: u"Enregistrement du résultat net de l'exercice",
        ECRITURES: [],
    }

    # On commence par solder les comptes de regroupement.
    for compte_regroupement, nom_compte in ((COMPTE_REGROUPEMENT_PRODUITS, REGROUPEMENT_PRODUITS), 
                                            (COMPTE_REGROUPEMENT_CHARGES, REGROUPEMENT_CHARGES)):
        soldes_compte_regroupement = soldes_comptes_regroupements[compte_regroupement] 
        debit = soldes_compte_regroupement[CREDIT]
        credit = soldes_compte_regroupement[DEBIT]
        ecriture_resultat[ECRITURES].append(
            {
                DEBIT: debit,
                CREDIT: credit,
                'nom_compte': nom_compte,
                'numero_compte_debit': debit and compte_regroupement or u'',
                'numero_compte_credit': credit and compte_regroupement or u'' 
            }
        )

    # Que l'on équilibre avec les comptes 120 (bénéfice) ou 129 (perte).
    debit = soldes_comptes_regroupements[COMPTE_REGROUPEMENT_PRODUITS][DEBIT] + \
                 soldes_comptes_regroupements[COMPTE_REGROUPEMENT_CHARGES][DEBIT]

    credit = soldes_comptes_regroupements[COMPTE_REGROUPEMENT_PRODUITS][CREDIT] + \
                 soldes_comptes_regroupements[COMPTE_REGROUPEMENT_CHARGES][CREDIT]

    if debit >= credit:
        debit = debit - credit
        credit = Decimal("0.0")
    elif debit < credit:
        credit = credit - debit
        debit = Decimal("0.0")

    ecriture_equilibre = {
        DEBIT: debit,
        CREDIT: credit,
        'nom_compte': debit and RESULTAT_EXERCICE_PERTE or RESULTAT_EXERCICE_BENEFICE,
        'numero_compte_debit': debit and COMPTE_PERTE or u'',
        'numero_compte_credit': credit and COMPTE_BENEFICE or u'' 
    }
    if debit:
        ecriture_resultat[ECRITURES].insert(0, ecriture_equilibre)
    elif credit:
        ecriture_resultat[ECRITURES].append(ecriture_equilibre)

    ecritures_finales.append(ecriture_resultat)

    return ecritures_finales


RX_DATE_INTITULE  = re.compile(ur"""^\|\|\s
                               (?P<date>\d\d/\d\d/\d\d\d\d)\s+\|\|
                               (?P<numero_compte_debit>\s+)\|\|
                               (?P<numero_compte_credit>\s+)\|\|
                               \s(?P<intitule>.+)\|\|
                               (?P<debit>\s+)\|\|
                               (?P<credit>\s+)\|\s*$""", flags=(re.X | re.U))

RX_SUITE_INTITULE = re.compile(ur"""^\|\|
                               (?P<date>\s+)\|\|
                               (?P<numero_compte_debit>\s+)\|\|
                               (?P<numero_compte_credit>\s+)\|\|
                               \s+(?P<intitule>.+)\|\|
                               (?P<debit>\s+)\|\|
                               (?P<credit>\s+)\|\s*$""", flags=(re.X | re.U))

RX_ECRITURE       = re.compile(ur"""^\|\|
                               (?P<date>\s+)\|\|
                               (?P<numero_compte_debit>[\s\w-]+)\|\|
                               (?P<numero_compte_credit>[\s\w-]+)\|\|
                               \s+(?P<nom_compte>.+)\|\|
                               (?P<debit>[\d\s.]+)\|\|
                               (?P<credit>[\d\s.]+)\|\s*$""", flags=(re.X | re.U))

def livre_journal_to_list(livre_journal_file):
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
    for line in livre_journal_file:
        if line[0] == '+':
            # Fin d'écriture.
            if ecriture:
                livre_journal.append(ecriture.copy()) # .copy()
                ecriture = {}
            # Début d'écriture.
            continue
        # Header
        elif line[0:2] == '| ':
            continue
        elif line[0:2] == '||':
            # Première ligne d'écriture, doit indiquer la date et l'intitulé.
            if not ecriture.has_key(DATE):
                m = RX_DATE_INTITULE.match(line)
                if not m:
                    raise BaseException, u"La première ligne d'une écriture doit mentionner la date et l'intitulé."
                m = m.groupdict()
                ecriture[DATE] = datetime.datetime.strptime(m[DATE], "%d/%m/%Y").date()
                ecriture[INTITULE] = m[INTITULE].strip()
                ecriture[ECRITURES] = []
            elif RX_SUITE_INTITULE.match(line):
                if ecriture[ECRITURES]:
                    raise BaseException, u"Les lignes supplémentaires d'intitulé doivent apparaitre exclusivement sous la première ligne."
                m = RX_SUITE_INTITULE.match(line).groupdict()
                ecriture[INTITULE] += u" %s" % m[INTITULE].strip()
            else:
                m = RX_ECRITURE.match(line).groupdict()
                m = dict([(k, v.strip()) for k,v in m.items()])
                sous_ecriture = {
                    'numero_compte_debit': m['numero_compte_debit'],
                    'numero_compte_credit': m['numero_compte_credit'],
                    'nom_compte': m['nom_compte'],
                    DEBIT: Decimal(m[DEBIT].replace(' ', '') or '0.00'),
                    CREDIT: Decimal(m[CREDIT].replace(' ', '') or '0.00'),
                }
                ecriture[ECRITURES].append(sous_ecriture)

    return livre_journal

LIVRE_JOURNAL_LEN = 148
DATE_LEN = 13
COMPTE_DEBIT_LEN = 17
COMPTE_CREDIT_LEN = 17
INTITULE_LEN = 62
DEBIT_LEN = 17
CREDIT_LEN = 17

def ecritures_to_livre_journal(ecritures, output_file, label=u"Ecriture(s) pour le Livre-journal"):
    """Converti une liste d'écritures JSON dans le format RestructuredText du Livre-journal. """

    from colbert.utils import fmt_number, rst_table
    from colbert.bilan import DEBIT, CREDIT

    lines = []
    table = [[(label, LIVRE_JOURNAL_LEN)]]
    for ecriture in ecritures:
        multiline_row = [
            [
                (ecriture[DATE], DATE_LEN),
                (u"", COMPTE_DEBIT_LEN),
                (u"", COMPTE_CREDIT_LEN),
                (ecriture[INTITULE], INTITULE_LEN),
                (u"", DEBIT_LEN),
                (u"", CREDIT_LEN),
            ],
        ]
        for e in ecriture[ECRITURES]:
            debit = Decimal(e[DEBIT])
            credit = Decimal(e[CREDIT])

            multiline_row.append(
                [
                    (u"", DATE_LEN),
                    (debit and e['numero_compte_debit'] or u"", COMPTE_DEBIT_LEN),
                    (credit and e['numero_compte_credit'] or u"", COMPTE_CREDIT_LEN),
                    (u"%s%s" % (credit and u"    " or u"", e['nom_compte']), INTITULE_LEN),
                    (debit and fmt_number(debit) or u"", DEBIT_LEN),
                    (credit and fmt_number(credit) or u"", CREDIT_LEN),
                ]
            )
        table.append(multiline_row)

    lines.append(rst_table(table))
    
    output_file.write(u"\n".join(lines))
    output_file.write(u"\n\n")

    return output_file

def get_solde_compte(livre_journal, numero_compte, date_debut, date_fin):
    debit, credit = Decimal("0.00"), Decimal("0.00")
    for ecriture in livre_journal:
        if (date_debut <= ecriture[DATE] <= date_fin):
            for e in ecriture[ECRITURES]:
                if e['numero_compte_debit'] == numero_compte:
                    debit += e[DEBIT]
                elif e['numero_compte_credit'] == numero_compte:
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
