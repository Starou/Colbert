# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from itertools import zip_longest
from .common import titre_principal_rst
from .common import (SOLDE_DEBITEUR, SOLDE_CREDITEUR, DATE_DEBUT, DATE_FIN,
                     LABEL, NUMERO, COMPTES)
from .utils import fmt_number, rst_table
from .utils import DATE_FMT

TOTAL_CHARGES = 'total_charges'
TOTAL_PRODUITS = 'total_produits'
RESULTAT = 'resultat'

EXPLOITATION = "exploitation"
FINANCIERES = "financières"
EXCEPTIONNELLES = "exceptionnelles"
AMMORTISSEMENTS_ET_PROVISIONS = "ammortissements et provisions"

CHARGES = "charges"
PRODUITS = "produits"
CHARGES_EXPLOITATION = "charges d'exploitation"
FOURNITURES_NON_STOCKABLES = "fournitures non stockables"
ACHATS_DE_MARCHANDISES = "achats de marchandises"
SERVICES_EXTERIEURS = "services extérieurs"
AUTRES_SERVICES_EXTERIEURS = "autres services extérieurs"
AUTRES_IMPOTS = "Autres impôts, taxes et versements assimilés"
REMUNERATIONS_DU_PERSONNEL = "Rémunérations du personnel"
AUTRES_CHARGES_GESTION_COURANTE = "autres charges de gestion courante"

CHARGES_FINANCIERES = "charges financières"

CHARGES_EXCEPTIONNELLES = "charges exceptionnelles"
CHARGES_EXCEPTIONNELLES_OPERATIONS_GESTION = "Charges exceptionnelles sur opérations de gestion"
DOTATIONS_AUX_AMMORTISSEMENTS_ET_PROVISIONS = "dotations aux ammortissements et provisions"
IMMOBILISATIONS_CORPORELLES = "immobilisations corporelles"

CHARGES_IMPOT_SOCIETES = "impôt sur les sociétés"

#

PRODUITS_EXPLOITATION = "produits d'exploitation"
AUTRES_PRODUITS_GESTION_COURANTE = "Autres produits de gestion courante"

PRODUITS_FINANCIERS = "produits financiers"
REVENUS_VALEURS_MOBILIERES_DE_PLACEMENT = "Revenus des valeurs mobilières de placement"
REPRISES_SUR_AMMORTISSEMENTS_ET_PROVISIONS = "reprises sur amortissements et provisions"

PRODUITS_EXCEPTIONNELS = "produits exceptionnels"

PRESTATIONS_DE_SERVICES = "prestations de services"

LIGNES_RESULTAT = {
    CHARGES: {
        EXPLOITATION: {
            LABEL: CHARGES_EXPLOITATION,
            COMPTES: [
                REMUNERATIONS_DU_PERSONNEL,
                FOURNITURES_NON_STOCKABLES,
                ACHATS_DE_MARCHANDISES,
                SERVICES_EXTERIEURS,
                AUTRES_SERVICES_EXTERIEURS,
                AUTRES_IMPOTS,
                AUTRES_CHARGES_GESTION_COURANTE,
            ]
        },
        FINANCIERES: {
            LABEL: CHARGES_FINANCIERES,
            COMPTES: [
            ]
        },
        EXCEPTIONNELLES: {
            LABEL: CHARGES_EXCEPTIONNELLES,
            COMPTES: [
                CHARGES_EXCEPTIONNELLES_OPERATIONS_GESTION,
            ]
        },
        AMMORTISSEMENTS_ET_PROVISIONS: {
            LABEL: DOTATIONS_AUX_AMMORTISSEMENTS_ET_PROVISIONS,
            COMPTES: [
                IMMOBILISATIONS_CORPORELLES,
            ]
        },
        CHARGES_IMPOT_SOCIETES: {
            LABEL: CHARGES_IMPOT_SOCIETES,
            COMPTES: [
                CHARGES_IMPOT_SOCIETES,
            ]
        }
    },
    PRODUITS: {
        EXPLOITATION: {
            LABEL: PRODUITS_EXPLOITATION,
            COMPTES: [
                PRESTATIONS_DE_SERVICES,
                AUTRES_PRODUITS_GESTION_COURANTE,
            ]
        },
        FINANCIERES: {
            LABEL: PRODUITS_FINANCIERS,
            COMPTES: [
                REVENUS_VALEURS_MOBILIERES_DE_PLACEMENT,
            ]
        },
        EXCEPTIONNELLES: {
            LABEL: PRODUITS_EXCEPTIONNELS,
            COMPTES: []
        },
        AMMORTISSEMENTS_ET_PROVISIONS: {
            LABEL: REPRISES_SUR_AMMORTISSEMENTS_ET_PROVISIONS,
            COMPTES: []
        },
    },
}

MAPPING_COMPTE_TO_RESULTAT = {
    '61': (CHARGES, EXPLOITATION, SERVICES_EXTERIEURS),
    '62': (CHARGES, EXPLOITATION, AUTRES_SERVICES_EXTERIEURS),
    '602': (CHARGES, EXPLOITATION, FOURNITURES_NON_STOCKABLES),
    '60611': (CHARGES, EXPLOITATION, FOURNITURES_NON_STOCKABLES),
    '6063': (CHARGES, EXPLOITATION, FOURNITURES_NON_STOCKABLES),
    '6064': (CHARGES, EXPLOITATION, FOURNITURES_NON_STOCKABLES),
    '607': (CHARGES, EXPLOITATION, ACHATS_DE_MARCHANDISES),
    '635': (CHARGES, EXPLOITATION, AUTRES_IMPOTS),
    '641': (CHARGES, EXPLOITATION, REMUNERATIONS_DU_PERSONNEL),
    '65': (CHARGES, EXPLOITATION, AUTRES_CHARGES_GESTION_COURANTE),

    '671': (CHARGES, EXCEPTIONNELLES, CHARGES_EXCEPTIONNELLES_OPERATIONS_GESTION),
    '68112': (CHARGES, AMMORTISSEMENTS_ET_PROVISIONS, IMMOBILISATIONS_CORPORELLES),

    '695': (CHARGES, CHARGES_IMPOT_SOCIETES, CHARGES_IMPOT_SOCIETES),

    '706': (PRODUITS, EXPLOITATION, PRESTATIONS_DE_SERVICES),
    '75': (PRODUITS, EXPLOITATION, AUTRES_PRODUITS_GESTION_COURANTE),
    '764': (PRODUITS, FINANCIERES, REVENUS_VALEURS_MOBILIERES_DE_PLACEMENT),
}

COMPTES_DE_CHARGES = '6'
COMPTES_DE_PRODUITS = '7'
COMPTES_DE_RESULTAT = (COMPTES_DE_CHARGES, COMPTES_DE_PRODUITS)


def compte_de_resultat(balance_des_comptes, label="Compte de résultat"):
    """Elaboration du compte de résultat à partir de la balance des comptes.

    return = {
        'label': "",
        'date_debut': Datetime(),
        'date_fin': Datetime(),
        total_charges: "1500",
        total_produits: "5000",
        resultat: "3500",
        charges: {
            'exploitation': [
                ('libellé des comptes de charges', "1100.00"),
                ('libellé des comptes de charges 2', "1500.00"),
                ...
            ],
            'financieres': [
            ],
            'exceptionnelles': [
            ]
        },
        produits: {
            'exploitation': [
                ('libellé des comptes de produits', "2222.00"),
                ('libellé des comptes de produits2', "111.00"),
                ...
            ],
            'financieres': [
            ],
            'exceptionnelles': [
            ]
        }
    }

    """

    compte_de_resultat = {
        LABEL: label,
        DATE_DEBUT: datetime.datetime.strptime(balance_des_comptes[DATE_DEBUT], DATE_FMT).date(),
        DATE_FIN: datetime.datetime.strptime(balance_des_comptes[DATE_FIN], DATE_FMT).date(),
        CHARGES: {
            EXPLOITATION: {},
            FINANCIERES: {},
            EXCEPTIONNELLES: {},
            AMMORTISSEMENTS_ET_PROVISIONS: {},
            CHARGES_IMPOT_SOCIETES: {}
        },
        PRODUITS: {
            EXPLOITATION: {},
            FINANCIERES: {},
            EXCEPTIONNELLES: {},
            AMMORTISSEMENTS_ET_PROVISIONS: {},
        },
    }

    def get_ligne_resultat(compte, mapping):
        numero_compte = compte[NUMERO]

        # Recherche de la ligne de rattachement du compte dans le bilan
        # en utilisant la notion de spécialisation des numéros de compte
        # du plan comptable général.
        # ex : numero = 4111. Recherches : 4111, 411, 41 puis 4.
        while numero_compte:
            try:
                ligne_bilan = mapping[numero_compte]
            except KeyError:
                numero_compte = numero_compte[:-1]
            else:
                return ligne_bilan
        raise BaseException("Impossible de dispatcher le numero de compte %s dans le compte de resultat"
                            % compte[NUMERO])

    total_charges, total_produits = Decimal("0.00"), Decimal("0.00")
    for compte in balance_des_comptes[COMPTES]:
        if compte[NUMERO][0] not in COMPTES_DE_RESULTAT:
            continue
        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])

        path_ligne_resultat = get_ligne_resultat(compte, MAPPING_COMPTE_TO_RESULTAT)
        cote, categorie, ligne = path_ligne_resultat

        montant = Decimal("0.00")
        if cote == CHARGES:
            if solde_crediteur:
                montant = -solde_crediteur
            elif solde_debiteur:
                montant = solde_debiteur
            total_charges += montant
        elif cote == PRODUITS:
            if solde_debiteur:
                montant = -solde_debiteur
            elif solde_crediteur:
                montant = solde_crediteur
            total_produits += montant

        compte_de_resultat[cote][categorie].setdefault(ligne, Decimal("0.00"))
        compte_de_resultat[cote][categorie][ligne] += montant

    compte_de_resultat[TOTAL_CHARGES] = total_charges
    compte_de_resultat[TOTAL_PRODUITS] = total_produits
    compte_de_resultat[RESULTAT] = total_produits - total_charges

    return compte_de_resultat


CHARGES_LEN = 60
PRODUITS_LEN = 60
MONTANT_LEN = 25


def compte_de_resultat_to_rst(compte_de_resultat, output_file):
    """Convert a `compte de résultat` json load to a reStructuredText file. """

    lines = []
    lines += titre_principal_rst(compte_de_resultat[LABEL],
                                 compte_de_resultat[DATE_DEBUT],
                                 compte_de_resultat[DATE_FIN])

    table = [
        [("Charges", CHARGES_LEN),
         ("Montant", MONTANT_LEN),
         ("Produits", PRODUITS_LEN),
         ("Montant", MONTANT_LEN)],
    ]

    def row(compte_de_resultat, categorie, ligne_charges, ligne_produits):
        charges = compte_de_resultat[CHARGES][categorie].get(ligne_charges)
        produits = compte_de_resultat[PRODUITS][categorie].get(ligne_produits)

        return [
            ((ligne_charges and charges) and ligne_charges.capitalize() or '', CHARGES_LEN),
            (charges and fmt_number(Decimal(charges)) or '', MONTANT_LEN),
            ((ligne_produits and produits) and ligne_produits.capitalize() or '', CHARGES_LEN),
            (produits and fmt_number(Decimal(produits)) or '', MONTANT_LEN),
        ]

    for categorie in (EXPLOITATION, FINANCIERES, EXCEPTIONNELLES, AMMORTISSEMENTS_ET_PROVISIONS):
        table.append([
            ("*%s*" % LIGNES_RESULTAT[CHARGES][categorie][LABEL].capitalize(), CHARGES_LEN),
            ("", MONTANT_LEN),
            ("*%s*" % LIGNES_RESULTAT[PRODUITS][categorie][LABEL].capitalize(), PRODUITS_LEN),
            ("", MONTANT_LEN),
        ])
        # La structure du tableau est donnée par le mapping LIGNES_RESULTAT.
        for charge, produit in zip_longest(LIGNES_RESULTAT[CHARGES][categorie][COMPTES], LIGNES_RESULTAT[PRODUITS][categorie][COMPTES]):
            table.append(row(compte_de_resultat, categorie, charge, produit))

        table.append([("", CHARGES_LEN), ("", MONTANT_LEN), ("", PRODUITS_LEN), ("", MONTANT_LEN)])

    # Ligne de l'impôt sur les sociétés.
    montant_is = Decimal(compte_de_resultat[CHARGES][CHARGES_IMPOT_SOCIETES].get(CHARGES_IMPOT_SOCIETES, "0.00"))
    table.append([
        ("*Impôt sur les sociétés*", CHARGES_LEN),
        ("%s" % fmt_number(montant_is), MONTANT_LEN),
        ("", PRODUITS_LEN),
        ("", MONTANT_LEN),
    ])
    table.append([("", CHARGES_LEN), ("", MONTANT_LEN), ("", PRODUITS_LEN), ("", MONTANT_LEN)])

    # Dernières lignes.
    table.append([("**Sous-total charges**", CHARGES_LEN),
                  (fmt_number(Decimal(compte_de_resultat[TOTAL_CHARGES])), MONTANT_LEN),
                  ("**Sous-total produits**", PRODUITS_LEN),
                  (fmt_number(Decimal(compte_de_resultat[TOTAL_PRODUITS])), MONTANT_LEN)])

    resultat = Decimal(compte_de_resultat[RESULTAT])
    if resultat >= 0:
        table.append([("**Résultat (bénéfice)**", CHARGES_LEN),
                      (fmt_number(resultat), MONTANT_LEN),
                      ("", PRODUITS_LEN),
                      ("", MONTANT_LEN)])
    else:
        table.append([("", CHARGES_LEN),
                      ("", MONTANT_LEN),
                      ("**Résultat (perte)**", PRODUITS_LEN),
                      (fmt_number(-resultat), MONTANT_LEN)])

    lines.append(rst_table(table))

    output_file.write("\n".join(lines))
    output_file.write("\n\n")

    return output_file
