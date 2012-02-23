# -*- coding: utf-8 -*-

import re
import datetime
from decimal import Decimal

from colbert.utils import fmt_number
from colbert.utils import DATE_FMT
from colbert.common import DEBIT, CREDIT, DATE, INTITULE, NOM, NUMERO
from colbert.plan_comptable_general import PLAN_COMPTABLE_GENERAL as PCG

from colbert.livre_journal import livre_journal_to_list, get_solde_compte
from colbert.livre_journal import ECRITURES, NOM_COMPTE, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT

def solde_comptes_de_tva(livre_journal_file, date_debut, date_fin):
    """Calcule l'écriture nécessaire au solde des comptes de TVA sur une période. """

    livre_journal = livre_journal_to_list(livre_journal_file)

    # On ne devrait avoir que du crédit en tva collecté et du débit en tva déductible.
    debit_tva_collectee, credit_tva_collectee = get_solde_compte(livre_journal,
                                                                 PCG['tva-collectee'][NUMERO],
                                                                 date_debut, date_fin)
    
    debit_tva_deductible, credit_tva_deductible = get_solde_compte(livre_journal,
                                                                   PCG['tva-deductible'][NUMERO],
                                                                   date_debut, date_fin)

    compte_tva, debit_tva, credit_tva = None, Decimal("0"), Decimal("0")

    # Ecritures.
    ecritures = []
    if credit_tva_collectee:
        ecritures.append({
            CREDIT: Decimal('0.00'),
            DEBIT: credit_tva_collectee,
            NOM_COMPTE: PCG['tva-collectee'][NOM],
            NUMERO_COMPTE_CREDIT: u'',
            NUMERO_COMPTE_DEBIT: PCG['tva-collectee'][NUMERO],
        })
    if debit_tva_deductible:
        ecritures.append({
            CREDIT: debit_tva_deductible,
            DEBIT: Decimal('0.00'),
            NOM_COMPTE: PCG['tva-deductible'][NOM],
            NUMERO_COMPTE_CREDIT: PCG['tva-deductible'][NUMERO],
            NUMERO_COMPTE_DEBIT: u'',
        })

    if credit_tva_collectee == debit_tva_deductible:
        pass

    # On a une dette envers l'état.
    elif credit_tva_collectee > debit_tva_deductible:
        credit_tva = credit_tva_collectee - debit_tva_deductible
        credit_tva_arrondi = Decimal(str(round(credit_tva)))

        ecritures.append({
            CREDIT: credit_tva_arrondi,
            DEBIT: Decimal('0.00'),
            NOM_COMPTE: PCG['tva-a-decaisser'][NOM],
            NUMERO_COMPTE_CREDIT: PCG['tva-a-decaisser'][NUMERO],
            NUMERO_COMPTE_DEBIT: u'',
        })

        # L'arrondi est équilibré avec les comptes 658/758.
        if credit_tva_arrondi > credit_tva:
            ecritures.append({
                CREDIT: Decimal('0.00'),
                DEBIT: credit_tva_arrondi - credit_tva,
                NOM_COMPTE: PCG['charges-diverses-gestion-courante'][NOM],
                NUMERO_COMPTE_CREDIT: u'',
                NUMERO_COMPTE_DEBIT: PCG['charges-diverses-gestion-courante'][NUMERO],
            })

        elif credit_tva_arrondi < credit_tva:
            ecritures.append({
                CREDIT: credit_tva - credit_tva_arrondi,
                DEBIT: Decimal('0.00'),
                NOM_COMPTE: PCG['produits-divers-gestion-courante'][NOM],
                NUMERO_COMPTE_CREDIT: PCG['produits-divers-gestion-courante'][NUMERO],
                NUMERO_COMPTE_DEBIT: u'',
            })


    # On a une créance sur l'état.
    elif credit_tva_deductible > debit_tva_collectee:
        pass # TODO

    if ecritures:
        return {
            DATE: date_fin,
            ECRITURES: ecritures,
            INTITULE: u"Solde des comptes de TVA du %s au %s" % (date_debut.strftime(DATE_FMT),
                                                                   date_fin.strftime(DATE_FMT))
        }
