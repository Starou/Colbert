# -*- coding: utf-8 -*-

import os, sys
import unittest
import codecs
import StringIO
import datetime
from decimal import Decimal

CURRENT_DIR = os.path.dirname(__file__)


class TVATestCase(unittest.TestCase):
    def test_solde_comptes_de_tva(self):
        from colbert.tva import solde_comptes_de_tva

        # Produits divers pour équilibrer.
        livre_journal = codecs.open(os.path.join(CURRENT_DIR, "livre-journal.txt"),
                                    mode="r", encoding="utf-8")
        solde_tva = solde_comptes_de_tva(livre_journal, 
                                         date_debut=datetime.date(2011, 3, 18),
                                         date_fin=datetime.date(2011, 6, 30))
        self.assertEqual(
            solde_tva,
            {'date': datetime.date(2011, 6, 30),
             'ecritures': [{'credit': Decimal('0.00'),
                            'debit': Decimal('294.00'),
                            'nom_compte': u'TVA collect\xe9',
                            'numero_compte_credit': u'',
                            'numero_compte_debit': '44571'},
                           {'credit': Decimal('33.66'),
                            'debit': Decimal('0.00'),
                            'nom_compte': u'TVA d\xe9ductible sur autres biens et services',
                            'numero_compte_credit': '44566',
                            'numero_compte_debit': u''},
                           {'credit': Decimal('260.0'),
                            'debit': Decimal('0.00'),
                            'nom_compte': u'TVA \xe0 d\xe9caisser',
                            'numero_compte_credit': '44551',
                            'numero_compte_debit': u''},
                           {'credit': Decimal('0.34'),
                            'debit': Decimal('0.00'),
                            'nom_compte': u'Produits divers de gestion courante',
                            'numero_compte_credit': '758',
                            'numero_compte_debit': u''}],
             'intitule': u'Solde des comptes de TVA du 18/03/2011 au 30/06/2011'}
        )

        # Charge diverse pour équilibrer.
        livre_journal.seek(0)
        solde_tva = solde_comptes_de_tva(livre_journal, 
                                         date_debut=datetime.date(2011, 4, 18),
                                         date_fin=datetime.date(2011, 6, 30))
        self.assertEqual(
            solde_tva, 
            {'date': datetime.date(2011, 6, 30),
             'ecritures': [{'credit': Decimal('0.00'),
                            'debit': Decimal('294.00'),
                            'nom_compte': u'TVA collect\xe9',
                            'numero_compte_credit': u'',
                            'numero_compte_debit': '44571'},
                           {'credit': Decimal('4.21'),
                            'debit': Decimal('0.00'),
                            'nom_compte': u'TVA d\xe9ductible sur autres biens et services',
                            'numero_compte_credit': '44566',
                            'numero_compte_debit': u''},
                           {'credit': Decimal('290.0'),
                            'debit': Decimal('0.00'),
                            'nom_compte': u'TVA \xe0 d\xe9caisser',
                            'numero_compte_credit': '44551',
                            'numero_compte_debit': u''},
                           {'credit': Decimal('0.00'),
                            'debit': Decimal('0.21'),
                            'nom_compte': u'Charges diverses de gestion courante',
                            'numero_compte_credit': u'',
                            'numero_compte_debit': '658'}],
             'intitule': u'Solde des comptes de TVA du 18/04/2011 au 30/06/2011'}
        )


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TVATestCase)
    return suite
