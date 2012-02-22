# -*- coding: utf-8 -*-

from utils import rst_title, DATE_FMT

DEBIT = u'debit'
CREDIT = u'credit'
DATE = 'date'
DATE_DEBUT = u'date_debut'
DATE_FIN = u'date_fin'
LABEL = u'label'
INTITULE = 'intitule'
NOM = u'nom'
NUMERO = u'numero'

def titre_principal_rst(titre, date_debut, date_fin):
    return [
        rst_title(titre), "\n",
        rst_title(u"Période du %s au %s" % (date_debut,date_fin), '-'), "\n",
    ]
