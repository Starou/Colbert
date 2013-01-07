# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from colbert.utils import fmt_number, rst_table
from colbert.utils import DATE_FMT

from colbert.common import titre_principal_rst
from colbert.common import (DEBIT, CREDIT, SOLDE_DEBITEUR, SOLDE_CREDITEUR, DATE_DEBUT, DATE_FIN,
                            LABEL, NUMERO, CATEGORIE, RUBRIQUES, COMPTES)

BRUT = u'brut'
NET = u'net'
AMORTISSEMENT = u'amortissement'

ACTIF = u'actif'
TOTAL_ACTIF = u'total_actif'
ACTIF_IMMOBILISE = u'actif immobilisé'
IMMOBILISATIONS_INCORPORELLES = u'immobilisations incorporelles'
AUTRES_IMMOBILISATIONS_INCORPORELLES = u'autres immobilisations incorporelles'
IMMOBILISATIONS_CORPORELLES = u'immobilisations corporelles'
AUTRES_IMMOBILISATIONS_CORPORELLES = u'autres immobilisations corporelles'
IMMOBILISATIONS_FINANCIERES = u'immobilisations financières'
AUTRES_IMMOBILISATIONS_FINANCIERES = u'autres immobilisations financières'
ACTIF_CIRCULANT = u'actif circulant'
STOCK = u'stock'
CLIENT = u'client et comptes rattachés'
AUTRES_CREANCES = u'autres créances'
DISPONIBILITES = u'disponibilités'

PASSIF = 'passif'
CAPITAUX_PROPRES = u'capitaux propres'
CAPITAL = u'capital'
RESERVES = u'réserves'
REPORT_A_NOUVEAU = u'report à nouveau'
RESULTAT = u'résultat'
DETTES = u'dettes'
AUTRES_DETTES = u'autres dettes'

# Mappings qui permet d'ordonner les lignes dans le bilan dans chaque catégorie.
LIGNES_BILAN_ACTIF = [
    {
        CATEGORIE: ACTIF_IMMOBILISE, 
        RUBRIQUES: [
            (
                IMMOBILISATIONS_INCORPORELLES, [
                    AUTRES_IMMOBILISATIONS_INCORPORELLES,
                ] 
            ),
            (
                IMMOBILISATIONS_CORPORELLES, [
                    AUTRES_IMMOBILISATIONS_CORPORELLES,
                ]
            ),
            (
                IMMOBILISATIONS_FINANCIERES, [
                    AUTRES_IMMOBILISATIONS_FINANCIERES
                ]
            ),
        ]
    },
    {
        CATEGORIE: ACTIF_CIRCULANT, 
        RUBRIQUES: [
            (
                None, [
                    STOCK,
                    CLIENT,
                    AUTRES_CREANCES,
                    DISPONIBILITES,
                ]
            )
        ]
    },
]

LIGNES_BILAN_PASSIF = [
    {
        CATEGORIE: CAPITAUX_PROPRES, 
        RUBRIQUES: [
            (
                None, [
                    CAPITAL,
                    RESERVES,
                    REPORT_A_NOUVEAU,
                    RESULTAT,
                ] 
            ),
        ]
    },
    {
        CATEGORIE: DETTES, 
        RUBRIQUES: [
            (
                None, [
                    AUTRES_DETTES,
                ]
            )
        ]
    },
]

MAPPING_COMPTE_TO_BILAN = {
    '100': {
        CREDIT: (PASSIF, CAPITAUX_PROPRES, None, CAPITAL, BRUT),
    },
    '106': {
        CREDIT: (PASSIF, CAPITAUX_PROPRES, None, RESERVES, BRUT),
    },
    '11': {
        CREDIT: (PASSIF, CAPITAUX_PROPRES, None, REPORT_A_NOUVEAU, BRUT),
    },
    '20': {
        DEBIT: (ACTIF, ACTIF_IMMOBILISE, IMMOBILISATIONS_INCORPORELLES, AUTRES_IMMOBILISATIONS_INCORPORELLES, BRUT),
    },
    '21': {
        DEBIT: (ACTIF, ACTIF_IMMOBILISE, IMMOBILISATIONS_CORPORELLES, AUTRES_IMMOBILISATIONS_CORPORELLES, BRUT),
    },
    '26': {
        DEBIT: (ACTIF, ACTIF_IMMOBILISE, IMMOBILISATIONS_FINANCIERES, AUTRES_IMMOBILISATIONS_FINANCIERES, BRUT),
    },
    '41': {
        DEBIT: (ACTIF, ACTIF_CIRCULANT, None, CLIENT, BRUT),
    },
    '44': {
        DEBIT: (ACTIF, ACTIF_CIRCULANT, None, AUTRES_CREANCES, BRUT),
        CREDIT: (PASSIF, DETTES, None, AUTRES_DETTES, BRUT),
    },
    '455': {
        CREDIT: (PASSIF, DETTES, None, AUTRES_DETTES, BRUT), #FIXME : vérifier que c'est bien là.
    },
    '51': {
        DEBIT: (ACTIF, ACTIF_CIRCULANT, None, DISPONIBILITES, BRUT),
        CREDIT: (PASSIF, DETTES, None, AUTRES_DETTES, BRUT), # TODO
    },
}

COMPTES_DE_BILAN = ['1', '2', '3', '4', '5']

def bilan(balance_des_comptes, label="Bilan"):
    """Elaboration du bilan à partir de la balance des comptes. 
    
    return = {
        'label': "",
        'date_debut': Datetime(),
        'date_fin': Datetime(),
        'total_actif': Decimal(),
        'resultat': Decimal(),
        'actif': [
            ['actif_immobilise',  # CATEGORIE.
                ['immobilisations_incorporelles', # RUBRIQUE.
                    ('stuff', {'brut': Decimal("1500.00"),
                               'immobilisation': Decimal("500.00"),
                               'net': Decimal("1000.00")}),
                    ('happens', {'brut': Decimal("1500.00"),
                                 'immobilisation': Decimal("500.00"),
                                 'net': Decimal("1000.00")}),
                ],       
                ['immobilisations_corporelles',
                    ('terrains', {'brut': Decimal("1500.00"),
                                  'immobilisation': Decimal("500.00"),
                                  'net': Decimal("1000.00")}),
                    ('constructions', {'brut': Decimal("1500.00"),
                                       'immobilisation': Decimal("500.00"),
                                       'net': Decimal("1000.00")}),
                ],       
            ],
            ['actif_circulant', [...]]
        ],
        'passif': [
            ['capitaux_propres', 
                [None,
                    ('capital', {'brut': Decimal("1500.00"),
                                 'immobilisation': Decimal("500.00"),
                                 'net': Decimal("1000.00")}),
                    ('resultat_exercice', {'brut': Decimal("1500.00"),
                                           'immobilisation': Decimal("500.00"),
                                           'net': Decimal("1000.00")}),
                ]       
            ],
        ]
    }
    
    """

    actif, passif = {}, {}
    bilan = {
        LABEL: label,
        DATE_DEBUT: datetime.datetime.strptime(balance_des_comptes[DATE_DEBUT], DATE_FMT).date(),
        DATE_FIN: datetime.datetime.strptime(balance_des_comptes[DATE_FIN], DATE_FMT).date(),
        ACTIF: actif,
        PASSIF: passif,
    }

    def get_ligne_bilan(compte, solde, mapping):
        numero_compte = compte[NUMERO]

        # Recherche de la ligne de rattachement du compte dans le bilan
        # en utilisant la notion de spécialisation des numéros de compte
        # du plan comptable général.
        # ex : numero = 4111. Recherches : 4111, 411, 41 puis 4.
        while numero_compte:
            #print numero_compte
            try:
                ligne_bilan = mapping[numero_compte]
            except KeyError:
                numero_compte = numero_compte[:-1]
            else:
                return ligne_bilan[solde]
        raise BaseException, "Impossible de dispatcher le numero de compte '%s' dans le bilan" % compte[NUMERO]

    for compte in balance_des_comptes[COMPTES]:
        if compte[NUMERO][0] not in COMPTES_DE_BILAN:
            continue
        solde_debiteur = Decimal(compte[SOLDE_DEBITEUR])
        solde_crediteur = Decimal(compte[SOLDE_CREDITEUR])
    
        # Actif.
        if solde_debiteur:
            solde = DEBIT
            montant = solde_debiteur

        # Passif ou amortissement.
        elif solde_crediteur:
            solde = CREDIT
            montant = solde_crediteur

        else:
            continue
        
        path_ligne_bilan = get_ligne_bilan(compte, solde, MAPPING_COMPTE_TO_BILAN) 
        cote, categorie, rubrique, ligne, colonne = path_ligne_bilan

        # Structure intermediaire ou les lignes sont dans un mapping plutôt que dans une 
        # liste car enrichissement itératif.
        #   'actif': {
        #       'actif_immobilise': {
        #           'immobilisations_corporelles': {
        #               'terrains': {'brut':x, 'immobilisation':y, 'net':z},
        #           ...
        #           } 
        #       } 
        #   } 

        categorie = bilan[cote].setdefault(categorie, {})
        rubrique = categorie.setdefault(rubrique, {})
        ligne = rubrique.setdefault(ligne, {BRUT: Decimal("0.00"),
                                            AMORTISSEMENT: Decimal("0.00"),
                                            NET: Decimal("0.00")})
        # màj du brut ou de l'amortissement.
        ligne[colonne] += montant
        ligne[NET] = ligne[BRUT] - ligne[AMORTISSEMENT]
        
    # Résultat, totaux.
    total_actif, total_passif_avant_resultat, resultat = resultat_bilan(bilan)
    bilan[TOTAL_ACTIF] = total_actif
    capitaux_propres = bilan[PASSIF].setdefault(CAPITAUX_PROPRES, {None: {}})
    capitaux_propres[None][RESULTAT] = {
        NET: resultat,
        AMORTISSEMENT: Decimal("0.00"),
        BRUT: resultat
    }

    bilan = ordered_bilan(bilan)
    return bilan

def resultat_bilan(pre_bilan):
    """Calcul le résultat de l'exercice. """

    def calcul_total(cote_bilan):
        total_brut, total_amortissement, total_net = Decimal("0.00"), Decimal("0.00"), Decimal("0.00")
        for categorie in pre_bilan[cote_bilan].values():
            for rubrique in categorie.values():
                for values in rubrique.values():
                    total_brut += values[BRUT]
                    total_amortissement += values[AMORTISSEMENT]
                    total_net += values[NET]
        return {BRUT: total_brut,
                AMORTISSEMENT: total_amortissement,
                NET: total_net}

    total_actif = calcul_total(ACTIF)
    total_passif_avant_resultat = calcul_total(PASSIF)
    resultat = total_actif[NET] - total_passif_avant_resultat[NET]

    return total_actif, total_passif_avant_resultat, resultat 

def ordered_bilan(pre_bilan):
    """Finalise le bilan en transfomant les mappings ACTIF et PASSIF en listes ordonnées
        pour respecter l'ordre du plan comptable général.

    """
    for cote, mapping in ((ACTIF, LIGNES_BILAN_ACTIF), (PASSIF, LIGNES_BILAN_PASSIF)):
        ordered_cote = []
        for categorie_mapping in mapping:
            categorie = categorie_mapping[CATEGORIE]
            if not pre_bilan[cote].has_key(categorie):
                continue
            ordered_categorie = [categorie,]
            for rubrique, lignes in categorie_mapping[RUBRIQUES]:
                if not pre_bilan[cote][categorie].has_key(rubrique):
                    continue
                ordered_rubrique = [rubrique,]
                lignes = [(ligne, pre_bilan[cote][categorie][rubrique][ligne]) \
                          for ligne in lignes if pre_bilan[cote][categorie][rubrique].has_key(ligne)]
                ordered_rubrique += lignes
                ordered_categorie.append(ordered_rubrique)

            ordered_cote.append(ordered_categorie)
        pre_bilan[cote] = ordered_cote

    return pre_bilan

ACTIF_LEN = 45
BRUT_LEN = 20
AMORTISSEMENT_LEN = 20
NET_LEN = 20
PASSIF_LEN = 45
MONTANT_LEN = 20

def bilan_to_rst(bilan, output_file):
    """Convert a `bilan` json load to a reStructuredText file. """

    lines = []
    lines += titre_principal_rst(bilan[LABEL], bilan[DATE_DEBUT], bilan[DATE_FIN])
    
    table = [
        [(u"Actif", ACTIF_LEN), 
         (u"Brut", BRUT_LEN), 
         (u"Amortissement", AMORTISSEMENT_LEN), 
         (u"Net", NET_LEN), 
         (u"Passif", PASSIF_LEN), 
         (u"Montant", MONTANT_LEN)]
    ]

    def flatten_bilan(bilan):
        """ 
        return (
            [ lignes_actifs ],
            [ lignes_passifs ]
        )
        """
        def flatten_cote_bilan(cote):
            flattened = []
            for categorie, rubriques in cote:
                flattened.append([u'**%s**' % categorie.capitalize(), '', '', ''])
                rubrique = rubriques[0]
                if rubrique:
                    flattened.append([u'*%s*' % rubrique.capitalize(), '', '', ''])
                for intitule, values in rubriques[1:]:
                    flattened.append([u'%s' % intitule.capitalize(), 
                                      Decimal(values[BRUT]),
                                      Decimal(values[AMORTISSEMENT]),
                                      Decimal(values[NET])])
            return flattened

        return flatten_cote_bilan(bilan[ACTIF]), flatten_cote_bilan(bilan[PASSIF])

    def row(ligne_actif, ligne_passif):
        return [
            (ligne_actif and ligne_actif[0] or '', ACTIF_LEN), 
            ((ligne_actif and ligne_actif[1]) and \
              fmt_number(ligne_actif[1]) or '', BRUT_LEN), 
            ((ligne_actif and ligne_actif[2]) and \
              fmt_number(ligne_actif[2]) or '', AMORTISSEMENT_LEN), 
            ((ligne_actif and ligne_actif[3]) and \
              fmt_number(ligne_actif[3]) or '', NET_LEN), 
            (ligne_passif and ligne_passif[0] or '', PASSIF_LEN), 
            ((ligne_passif and ligne_passif[1]) and \
              fmt_number(ligne_passif[1]) or '', MONTANT_LEN) 
        ]

    map(lambda actif, passif: table.append(row(actif, passif)), *flatten_bilan(bilan)) 

    # Dernière ligne.
    table.append([
        (u"*Total*", ACTIF_LEN), 
        (u"*%s*" % fmt_number(Decimal(bilan[TOTAL_ACTIF][BRUT])), BRUT_LEN), 
        (u"*%s*" % fmt_number(Decimal(bilan[TOTAL_ACTIF][AMORTISSEMENT])), AMORTISSEMENT_LEN), 
        (u"**%s**" % fmt_number(Decimal(bilan[TOTAL_ACTIF][NET])), NET_LEN), 
        (u"*Total*", PASSIF_LEN), 
        (u"**%s**"% fmt_number(Decimal(bilan[TOTAL_ACTIF][NET])), MONTANT_LEN)
    ])

    lines.append(rst_table(table))

    output_file.write(u"\n".join(lines))
    output_file.write(u"\n\n")

    return output_file
