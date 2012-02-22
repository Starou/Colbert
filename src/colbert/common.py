# -*- coding: utf-8 -*-

from utils import rst_title, DATE_FMT

def titre_principal_rst(titre, date_debut, date_fin):
    return [
        rst_title(titre), "\n",
        rst_title(u"Période du %s au %s" % (date_debut,date_fin), '-'), "\n",
    ]
