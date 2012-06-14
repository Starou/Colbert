# -*- coding: utf-8 -*-

import os, sys
import unittest
import codecs
import StringIO
import json
from decimal import Decimal
import datetime

CURRENT_DIR = os.path.dirname(__file__)

VERSION_INFO = sys.version_info

class UtilsTestCase(unittest.TestCase):
    def test_rst_table(self):
        from colbert.utils import rst_table
        
        # Simple table.
        result = rst_table([
            [
                ("1-1", 8),
                ("1-2", 6),
                ("1-3", 14),
            ],
            [
                ("2-1", 8),
                ("2-2", 6),
                ("2-3", 14),
            ],
            [
                ("3-1", 8),
                ("3-2", 6),
                ("3-3", 14),
            ],
        ])
        self.assertEqual(result,
u"""+--------+------+--------------+
| 1-1    | 1-2  | 1-3          |
+========+======+==============+
| 2-1    | 2-2  | 2-3          |
+--------+------+--------------+
| 3-1    | 3-2  | 3-3          |
+--------+------+--------------+""")

        # Multilines table.
        result = rst_table([
            [
                [("1-1-1", 8), ("1-2-1", 9), ("1-3-1", 14)],
                [("1-1-2", 8), ("1-2-2", 9), ("1-3-2", 14)],
                [("1-1-3", 8), ("1-2-3", 9), ("1-3-3", 14)],
            ],
            [
                [("2-1-1", 8), ("2-2-1", 9), ("2-3-1", 14)],
                [("2-1-2", 8), ("2-2-2", 9), ("2-3-2", 14)],
                [("2-1-3", 8), ("2-2-3", 9), ("2-3-3", 14)],
            ],
            [
                [("3-1-1", 8), ("3-2-1", 9), ("3-3-1", 14)],
                [("3-1-2", 8), ("3-2-2", 9), ("3-3-2", 14)],
                [("3-1-3", 8), ("3-2-3", 9), ("3-3-3", 14)],
            ],
        ])
        self.maxDiff = None
        self.assertEqual(result,
u"""+--------+---------+--------------+
|| 1-1-1 || 1-2-1  || 1-3-1       |
|| 1-1-2 || 1-2-2  || 1-3-2       |
|| 1-1-3 || 1-2-3  || 1-3-3       |
+========+=========+==============+
|| 2-1-1 || 2-2-1  || 2-3-1       |
|| 2-1-2 || 2-2-2  || 2-3-2       |
|| 2-1-3 || 2-2-3  || 2-3-3       |
+--------+---------+--------------+
|| 3-1-1 || 3-2-1  || 3-3-1       |
|| 3-1-2 || 3-2-2  || 3-3-2       |
|| 3-1-3 || 3-2-3  || 3-3-3       |
+--------+---------+--------------+""")

    def test_decode_as_ecriture(self):
        from colbert.utils import decode_as_ecriture as as_ecriture

        grand_livre_json = """{
            "comptes": {
                "4181": {
                    "solde_crediteur": "13156.00", 
                    "nom": "Clients - Factures \u00e0 \u00e9tablir", 
                    "total_debit": "0.00", 
                    "solde_debiteur": "0.00", 
                    "total_credit": "13156.00", 
                    "ecritures": [
                        {
                            "date": "01/01/2012", 
                            "intitule": "Prestation MyClient1 d\u00e9cembre 2011", 
                            "credit": "13156.00"
                        }
                    ]
                }, 
                "706": {
                    "solde_crediteur": "11000.00", 
                    "nom": "Produits - prestations de services", 
                    "total_debit": "11000.00", 
                    "solde_debiteur": "0.00", 
                    "total_credit": "22000.00", 
                    "ecritures": [
                        {
                            "date": "01/01/2012", 
                            "intitule": "Prestation MyClient1 d\u00e9cembre 2011", 
                            "debit": "11000.00"
                        }, 
                        {
                            "date": "03/01/2012", 
                            "intitule": "Facture 2012-01 MyClient1 Prestation d\u00e9cembre 2011", 
                            "credit": "11000.00"
                        }, 
                        {
                            "date": "20/03/2012", 
                            "intitule": "Facture 2012-03 MyClient2 Prestation f\u00e9vrier 2012", 
                            "credit": "11000.00"
                        }
                    ]
                }
            }, 
            "date_fin": "31/12/2012", 
            "date_debut": "01/01/2012", 
            "label": "Grand-Livre 2012"
        }
        """

        grand_livre = json.loads(grand_livre_json, object_hook=as_ecriture)
        self.assertEqual(grand_livre, {
            u'comptes': {u'4181': {u'ecritures': [{u'credit': Decimal('13156.00'),
                                                   u'date': datetime.date(2012, 1, 1),
                                                   u'intitule': u'Prestation MyClient1 d\xe9cembre 2011'}],
                                   u'nom': u'Clients - Factures \xe0 \xe9tablir',
                                   u'solde_crediteur': Decimal('13156.00'),
                                   u'solde_debiteur': Decimal('0.00'),
                                   u'total_credit': Decimal('13156.00'),
                                   u'total_debit': Decimal('0.00')},
                         u'706': {u'ecritures': [{u'date': datetime.date(2012, 1, 1),
                                                  u'debit': Decimal('11000.00'),
                                                  u'intitule': u'Prestation MyClient1 d\xe9cembre 2011'},
                                                 {u'credit': Decimal('11000.00'),
                                                  u'date': datetime.date(2012, 1, 3),
                                                  u'intitule': u'Facture 2012-01 MyClient1 Prestation d\xe9cembre 2011'},
                                                 {u'credit': Decimal('11000.00'),
                                                  u'date': datetime.date(2012, 3, 20),
                                                  u'intitule': u'Facture 2012-03 MyClient2 Prestation f\xe9vrier 2012'}],
                                  u'nom': u'Produits - prestations de services',
                                  u'solde_crediteur': Decimal('11000.00'),
                                  u'solde_debiteur': Decimal('0.00'),
                                  u'total_credit': Decimal('22000.00'),
                                  u'total_debit': Decimal('11000.00')}},
            u'date_debut': datetime.date(2012, 1, 1),
            u'date_fin': datetime.date(2012, 12, 31),
            u'label': u'Grand-Livre 2012'
        })                         

    def test_latex_escape(self):
        from colbert.utils import latex_escape
        self.assertEqual(latex_escape("Bonnie & Clyde"), "Bonnie \\& Clyde")
        self.assertEqual(latex_escape("Johnny Ca$h"), "Johnny Ca\\$h")
        self.assertEqual(latex_escape("#9"), "\\#9")
        self.assertEqual(latex_escape("100%"), "100\\%")
        self.assertEqual(latex_escape("_lame_"), "\\_lame\\_")
        self.assertEqual(latex_escape("{TeX}"), "\\{TeX\\}")
        self.assertEqual(latex_escape("~almost"), "\\~almost")
        self.assertEqual(latex_escape("^-^"), "\\^-\\^")

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)
    return suite
