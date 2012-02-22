# -*- coding: utf-8 -*-

from colbert.common import NOM, NUMERO

PLAN_COMPTABLE_GENERAL = {
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
