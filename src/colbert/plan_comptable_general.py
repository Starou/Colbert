# -*- coding: utf-8 -*-

from colbert.common import NOM, NUMERO

PLAN_COMPTABLE_GENERAL = {
    'perte': {
        NUMERO: "129",
        NOM: u"résultat de l'exercice (perte)",
    },
    'benefice': {
        NUMERO: "120",
        NOM: u"résultat de l'exercice (bénéfice)",
    },
    'regroupement-produits': {
        NUMERO: "127",
        NOM: u"Regroupement des comptes de produits",
    },
    'regroupement-charges': {
        NUMERO: "126",
        NOM: u"Regroupement des comptes de charges",
    },
    'tva-ca-factures-a-etablir': {
        NUMERO: "44587",
        NOM: u"Taxes sur le CA sur factures à établir",
    },
    'tva-collectee': {
        NUMERO: "44571",
        NOM: u"TVA collecté",
    },
    'tva-deductible': {
        NUMERO: "44566",
        NOM: u"TVA déductible sur autres biens et services",
    },
    'tva-a-decaisser': {
        NUMERO: "44551",
        NOM: u"TVA à décaisser",
    },
    'produits-divers-gestion-courante': {
        NUMERO: "758",
        NOM: u"Produits divers de gestion courante",
    },
    'charges-diverses-gestion-courante': {
        NUMERO: "658",
        NOM: u"Charges diverses de gestion courante",
    },
}
