# -*- coding: utf-8 -*-

from .utils import rst_title

DEBIT = 'debit'
CREDIT = 'credit'
TOTAL_DEBIT = 'total_debit'
TOTAL_CREDIT = 'total_credit'
SOLDE_DEBITEUR = 'solde_debiteur'
SOLDE_CREDITEUR = 'solde_crediteur'

DATE = 'date'
DATE_DEBUT = 'date_debut'
DATE_FIN = 'date_fin'

LABEL = 'label'
INTITULE = 'intitule'
NOM = 'nom'
NUMERO = 'numero'
NUMERO_COMPTE = 'numero_compte'
NUMERO_LIGNE_ECRITURE_DEBUT = 'numero_ligne_debut'
NUMERO_LIGNE_ECRITURE_FIN = 'numero_ligne_fin'

CATEGORIE = 'categorie'
RUBRIQUES = 'rubriques'

COMPTES = 'comptes'


def titre_principal_rst(titre, date_debut, date_fin):
    return [
        rst_title(titre), "\n",
        rst_title("Période du %s au %s" % (date_debut, date_fin), '-'), "\n",
    ]
