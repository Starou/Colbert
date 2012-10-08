# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from colbert.utils import d_round
from colbert.utils import DATE_FMT
from colbert.common import DEBIT, CREDIT, DATE, INTITULE, NOM, NUMERO
from colbert.plan_comptable_general import PLAN_COMPTABLE_GENERAL as PCG
from colbert.livre_journal import ECRITURES

def calculer_facture(facture):
    """ Complète la facture en calculant :
        > `montant_ht' de chaque ligne ;
        > `montant_ht` et `montant_ttc' total ;
        > `tva` totale de la facture.
        > Diverses dates.
    """
    
    facture["montant_ht"] = Decimal("0.00")
    facture["montant_ttc"] = Decimal("0.00")
    facture["tva"] = {}

    # Calcul du montant de chaque ligne et du montant HT total.
    for ligne in facture["detail"]:
        ligne["montant_ht"] = Decimal(ligne["prix_unitaire_ht"]) * Decimal(ligne["quantite"])
        facture["montant_ht"] += ligne["montant_ht"]
        facture["tva"].setdefault(ligne["taux_tva"], Decimal("0.00"))
        tva = d_round(ligne["montant_ht"] * Decimal(ligne["taux_tva"]) / Decimal("100.0"), 2)
        facture["tva"][ligne["taux_tva"]] += tva
        facture["montant_ttc"] += (ligne["montant_ht"] + tva)
        facture["reste_a_payer"] = facture["montant_ttc"] - Decimal(facture["deja_paye"])

    # Date de réglement.
    facture["date_reglement"] = date_reglement_facture(facture["date_facture"],
                                                      int(facture["nb_jours_payable_fin_de_mois"]))
    facture["date_debut_penalites"] = facture["date_reglement"] + datetime.timedelta(1)

    return facture

def date_reglement_facture(date_facture, nb_jours_payable_fin_de_mois):
    """Calcul de la date butoir de réglement d'une facture sur le principe de `n jours fin de mois'. """
    date_reglement = datetime.datetime.strptime(date_facture, DATE_FMT).date() + \
                     datetime.timedelta(nb_jours_payable_fin_de_mois)

    # Premier du mois suivant moins 1 jour pour avoir le dernier jour du mois.
    year = date_reglement.year + (date_reglement.month / 12)
    month = (date_reglement.month % 12) + 1

    date_reglement = datetime.date(year, month, 1)
    date_reglement = date_reglement - datetime.timedelta(1)

    return date_reglement

def facture_to_tex(facture, tex_template, output_file):
    """Produce a TeX file from a template and a json facture. """

    kwargs = facture.copy()

    # Flatten the facture dict.
    for k, v in kwargs["client"].items():
        kwargs["client_%s"%k] = v

    # Lignes de facturation.
    kwargs["lignes_facture"] = u"\n".join([
      u"& %s &  %s %s & \\numprint{%s} & \\numprint{%s} \\\\" % (
          l["description"],
          l["quantite"],
          l["unite"],
          l["prix_unitaire_ht"],
          l["montant_ht"],
      ) for l in kwargs["detail"] 
    ])

    # Lignes de TVA.
    kwargs["lignes_tva"] = u"\\cline{3-5}".join([
        u"\\multicolumn{2}{l|}{} & \\multicolumn{2}{|l|}{\sc TVA %s\\%%} & \\numprint{%s}\\\\" % (
            taux_tva, 
            tva
      ) for taux_tva, tva in kwargs["tva"].items() 
    ])

    # Période d'exécution de la prestation.
    # TODO: cas où exécuté en un jour.
    # TODO: put in a function and write a test.
    date_debut = datetime.datetime.strptime(kwargs["date_debut_execution"], DATE_FMT).date()
    date_fin = datetime.datetime.strptime(kwargs["date_fin_execution"], DATE_FMT).date()
    date_fin_fmt = u"%A %d %B %Y"
    date_debut_fmt = u"%A %d"
    if date_debut.month != date_fin.month:
        date_debut_fmt += " u%B"
    if date_debut.year != date_fin.year:
        date_debut_fmt += u" %Y"
    kwargs["periode_execution"] = u"Du %s au %s" % (date_debut.strftime(date_debut_fmt.encode("utf-8")).decode("utf-8"),
                                                    date_fin.strftime(date_fin_fmt.encode("utf-8")).decode("utf-8"))
    
    # Reformatage des dates.
    for d in ("date_facture", "date_reglement", "date_debut_penalites"):
        kwargs[d] = datetime.datetime.strptime(kwargs[d], DATE_FMT).date().strftime(date_fin_fmt.encode("utf-8")).decode("utf-8")

    tex_string = tex_template.read() % kwargs
    output_file.write(tex_string)

def ecriture_facture(facture):
    date_facture = datetime.datetime.strptime(facture["date_facture"], DATE_FMT).date()
    compte_tva = PCG['tva-ca-factures-a-etablir']

    ecritures = [
        {
            'nom_compte': facture["client"]["nom_compte"],
            'debit': Decimal(facture["montant_ttc"]),
            'credit': Decimal('0.00'),
            'numero_compte_debit': facture["client"]["numero_compte"],
            'numero_compte_credit': u'',
        },
        {
            'nom_compte': facture["nom_compte"],
            'debit': Decimal('0.00'),
            'credit': Decimal(facture["montant_ht"]),
            'numero_compte_debit': u'',
            'numero_compte_credit': facture["numero_compte"],
        },
        {
            'nom_compte': compte_tva[NOM],
            'debit': Decimal('0.00'),
            'credit': Decimal(facture["montant_ttc"]) - Decimal(facture["montant_ht"]),
            'numero_compte_debit': u'',
            'numero_compte_credit': compte_tva[NUMERO],
        },
    ]
    
    return {
        DATE: date_facture,
        ECRITURES: ecritures,
        INTITULE: u"Facture %s %s" % (facture["numero_facture"],
                                      facture["client"]["nom"])
    }
