# -*- coding: utf-8 -*-

import re
import datetime
from decimal import Decimal
from colbert.utils import fmt_number
from colbert.utils import DATE_FMT
from colbert.plan_comptable_general import PLAN_COMPTABLE_GENERAL as PCG

from livre_journal import livre_journal_to_list, get_solde_compte

def solde_comptes_de_tva(livre_journal_file, date_debut, date_fin):
    """Calcule l'écriture nécessaire au solde des comptes de TVA sur une période. """

    livre_journal = livre_journal_to_list(livre_journal_file)

    # On ne devrait avoir que du crédit en tva collecté et du débit en tva déductible.
    debit_tva_collectee, credit_tva_collectee = get_solde_compte(livre_journal,
                                                                 PCG['tva-collectee']['numero'],
                                                                 date_debut, date_fin)
    
    debit_tva_deductible, credit_tva_deductible = get_solde_compte(livre_journal,
                                                                   PCG['tva-deductible']['numero'],
                                                                   date_debut, date_fin)

    compte_tva, debit_tva, credit_tva = None, Decimal("0"), Decimal("0")

    # Ecritures.
    ecritures = []
    if credit_tva_collectee:
        ecritures.append({
            'credit': Decimal('0.00'),
            'debit': credit_tva_collectee,
            'nom_compte': PCG['tva-collectee']['nom'],
            'numero_compte_credit': u'',
            'numero_compte_debit': PCG['tva-collectee']['numero'],
        })
    if debit_tva_deductible:
        ecritures.append({
            'credit': debit_tva_deductible,
            'debit': Decimal('0.00'),
            'nom_compte': PCG['tva-deductible']['nom'],
            'numero_compte_credit': PCG['tva-deductible']['numero'],
            'numero_compte_debit': u'',
        })

    if credit_tva_collectee == debit_tva_deductible:
        pass

    # On a une dette envers l'état.
    elif credit_tva_collectee > debit_tva_deductible:
        credit_tva = credit_tva_collectee - debit_tva_deductible
        credit_tva_arrondi = Decimal(str(round(credit_tva)))

        ecritures.append({
            'credit': credit_tva_arrondi,
            'debit': Decimal('0.00'),
            'nom_compte': PCG['tva-a-decaisser']['nom'],
            'numero_compte_credit': PCG['tva-a-decaisser']['numero'],
            'numero_compte_debit': u'',
        })

        # L'arrondi est équilibré avec les comptes 658/758.
        if credit_tva_arrondi > credit_tva:
            ecritures.append({
                'credit': Decimal('0.00'),
                'debit': credit_tva_arrondi - credit_tva,
                'nom_compte': PCG['charges-diverses-gestion-courante']['nom'],
                'numero_compte_credit': u'',
                'numero_compte_debit': PCG['charges-diverses-gestion-courante']['numero'],
            })

        elif credit_tva_arrondi < credit_tva:
            ecritures.append({
                'credit': credit_tva - credit_tva_arrondi,
                'debit': Decimal('0.00'),
                'nom_compte': PCG['produits-divers-gestion-courante']['nom'],
                'numero_compte_credit': PCG['produits-divers-gestion-courante']['numero'],
                'numero_compte_debit': u'',
            })


    # On a une créance sur l'état.
    elif credit_tva_deductible > debit_tva_collectee:
        pass # TODO

    if ecritures:
        return {
            'date': date_fin,
            'ecritures': ecritures,
            'intitule': u"Solde des comptes de TVA du %s au %s" % (date_debut.strftime(DATE_FMT),
                                                                   date_fin.strftime(DATE_FMT))
        }
