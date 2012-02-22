# -*- coding: utf-8 -*-

from utils import rst_title, DATE_FMT

DEBIT = u'debit'
CREDIT = u'credit'
TOTAL_DEBIT = u'total_debit'
TOTAL_CREDIT = u'total_credit'
SOLDE_DEBITEUR = u'solde_debiteur'
SOLDE_CREDITEUR = u'solde_crediteur'

DATE = 'date'
DATE_DEBUT = u'date_debut'
DATE_FIN = u'date_fin'

LABEL = u'label'
INTITULE = 'intitule'
NOM = u'nom'
NUMERO = u'numero'

COMPTES = u'comptes'

def titre_principal_rst(titre, date_debut, date_fin):
    return [
        rst_title(titre), "\n",
        rst_title(u"Période du %s au %s" % (date_debut,date_fin), '-'), "\n",
    ]
