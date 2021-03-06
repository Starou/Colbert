# -*- coding: utf-8 -*-

from decimal import Decimal

from colbert.utils import DATE_FMT
from colbert.common import DEBIT, CREDIT, DATE, INTITULE, NOM, NUMERO
from colbert.plan_comptable_general import PLAN_COMPTABLE_GENERAL as PCG

from colbert.livre_journal import livre_journal_to_list, get_solde_compte
from colbert.livre_journal import ECRITURES, NOM_COMPTE, NUMERO_COMPTE_DEBIT, NUMERO_COMPTE_CREDIT


def solde_comptes_de_tva(livre_journal_file, date_debut, date_fin):
    """Calcule l'écriture nécessaire au solde des comptes de TVA sur une période. """

    livre_journal = livre_journal_to_list(livre_journal_file)

    tva_collectes, tva_deductibles = [], []

    for compte in PCG['tva-collectee']:
        debit, credit = get_solde_compte(livre_journal, compte[NUMERO], date_debut, date_fin)
        tva_collectes.append({
            'compte': compte,
            'debit': debit,
            'credit': credit,
        })

    for compte in PCG['tva-deductible']:
        debit, credit = get_solde_compte(livre_journal, compte[NUMERO], date_debut, date_fin)
        tva_deductibles.append({
            'compte': compte,
            'debit': debit,
            'credit': credit,
        })

    compte_tva, debit_tva, credit_tva = None, Decimal("0"), Decimal("0")

    # Ecritures.
    ecritures = []

    # Lignes d'écriture de solde des comptes de TVA.
    for solde_compte in (tva_collectes + tva_deductibles):
        ecriture = _ecriture_solde(solde_compte)
        if ecriture:
            ecritures.append(ecriture)

    # ~ Equilibrage de l'écriture ~ #

    credit_tva_collectees = reduce(lambda x, y: x+y, [tva['credit'] for tva in tva_collectes], Decimal('0.0'))
    debit_tva_deductibles = reduce(lambda x, y: x+y, [tva['debit'] for tva in tva_deductibles], Decimal('0.0'))

    if credit_tva_collectees == debit_tva_deductibles:
        pass

    # On a une dette envers l'état.
    elif credit_tva_collectees > debit_tva_deductibles:
        credit_tva = credit_tva_collectees - debit_tva_deductibles
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
    else:
        debit_tva = debit_tva_deductibles - credit_tva_collectees
        debit_tva_arrondi = Decimal(str(round(debit_tva)))

        ecritures.append({
            CREDIT: Decimal('0.00'),
            DEBIT: debit_tva_arrondi ,
            NOM_COMPTE: PCG['credit-de-tva-a-reporter'][NOM],
            NUMERO_COMPTE_CREDIT: u'',
            NUMERO_COMPTE_DEBIT: PCG['credit-de-tva-a-reporter'][NUMERO],
        })

        # L'arrondi est équilibré avec les comptes 658/758.
        if debit_tva_arrondi > debit_tva:
            ecritures.append({
                CREDIT: debit_tva_arrondi - debit_tva,
                DEBIT: Decimal('0.00'),
                NOM_COMPTE: PCG['produits-divers-gestion-courante'][NOM],
                NUMERO_COMPTE_CREDIT: PCG['produits-divers-gestion-courante'][NUMERO],
                NUMERO_COMPTE_DEBIT: u'',
            })
        elif debit_tva_arrondi < debit_tva:
            ecritures.append({
                CREDIT: Decimal('0.00'),
                DEBIT: debit_tva - debit_tva_arrondi,
                NOM_COMPTE: PCG['charges-diverses-gestion-courante'][NOM],
                NUMERO_COMPTE_CREDIT: u'',
                NUMERO_COMPTE_DEBIT: PCG['charges-diverses-gestion-courante'][NUMERO],
            })



    if ecritures:
        return {
            DATE: date_fin,
            ECRITURES: ecritures,
            INTITULE: [u"Solde des comptes de TVA du %s au %s" % (
                date_debut.strftime(DATE_FMT), date_fin.strftime(DATE_FMT))],
        }


def _ecriture_solde(solde_compte):
    if solde_compte['credit'] > solde_compte['debit']:
        return {
            CREDIT: Decimal('0.00'),
            DEBIT: solde_compte['credit'] - solde_compte['debit'],
            NOM_COMPTE: solde_compte['compte'][NOM],
            NUMERO_COMPTE_CREDIT: u'',
            NUMERO_COMPTE_DEBIT: solde_compte['compte'][NUMERO],
        }
    elif solde_compte['credit'] < solde_compte['debit']:
        return {
            CREDIT: solde_compte['debit'] - solde_compte['credit'],
            DEBIT: Decimal('0.00'),
            NOM_COMPTE: solde_compte['compte'][NOM],
            NUMERO_COMPTE_CREDIT: solde_compte['compte'][NUMERO],
            NUMERO_COMPTE_DEBIT: u'',
        }
