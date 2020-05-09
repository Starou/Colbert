# -*- coding: utf-8 -*-

from .common import NOM, NUMERO


PLAN_COMPTABLE_GENERAL = {
    'perte': {
        NUMERO: "129",
        NOM: "résultat de l'exercice (perte)",
    },
    'benefice': {
        NUMERO: "120",
        NOM: "résultat de l'exercice (bénéfice)",
    },
    'regroupement-produits': {
        NUMERO: "127",
        NOM: "Regroupement des comptes de produits",
    },
    'regroupement-charges': {
        NUMERO: "126",
        NOM: "Regroupement des comptes de charges",
    },
    'tva-ca-factures-a-etablir': {
        NUMERO: "44587",
        NOM: "Taxes sur le CA sur factures à établir",
    },
    'tva-collectee': [
        {
            NUMERO: "44571",
            NOM: "TVA collecté",
        },
    ],
    'tva-deductible': [
        {
            NUMERO: "44562",
            NOM: "TVA sur immobilisations",
        },
        {
            NUMERO: "44566",
            NOM: "TVA déductible sur autres biens et services",
        },
    ],
    'tva-a-decaisser': {
        NUMERO: "44551",
        NOM: "TVA à décaisser",
    },
    'credit-de-tva-a-reporter': {
        NUMERO: "44567",
        NOM: "Crédit de TVA à reporter",
    },
    'produits-divers-gestion-courante': {
        NUMERO: "758",
        NOM: "Produits divers de gestion courante",
    },
    'charges-diverses-gestion-courante': {
        NUMERO: "658",
        NOM: "Charges diverses de gestion courante",
    },
}
