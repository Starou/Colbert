# -*- coding: utf-8 -*-

import os, sys
import unittest
import codecs
import StringIO

CURRENT_DIR = os.path.dirname(__file__)

class SoldeDeCompteTestCase(unittest.TestCase):
    def test_solde_de_compte(self):
        from colbert.solde_de_compte import solde_de_compte
        livre_journal = codecs.open(os.path.join(CURRENT_DIR, "livre-journal.txt"), 
                                    mode="r", encoding="utf-8")
        comptes = [
            {
                'numero_compte': "512",
                'journaux': [
                    {
                        'label': "Avril 2011",
                        'date_debut': "01/04/2011",
                        'date_fin': "02/05/2011",
                        'debit_initial': "0.00",
                        'credit_initial': "0.00",
                        'debit_final': "1485.93",
                        'credit_final': "0.00",
                    },
                    {
                        'label': "Mai 2011",
                        'date_debut': "03/05/2011",
                        'date_fin': "01/06/2011",
                        'debit_initial': "1485.93",
                        'credit_initial': "0.00",
                        'debit_final': "1461.94",
                        'credit_final': "0.00",
                    },
                ]
            }
        ]
        compte_512_rst = codecs.open(os.path.join(CURRENT_DIR, "compte_512-2011.txt"), 
                                     mode="r", encoding="utf-8")
        output = StringIO.StringIO()
        # Uncomment to generate the file.
        # output = codecs.open(os.path.join(CURRENT_DIR, "compte_512-2011.txt"), 
        #                                   mode="w+", encoding="utf-8")
        solde_de_compte(livre_journal, output, comptes)
        self.maxDiff = None
        self.assertEqual(output.getvalue(), compte_512_rst.read())

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SoldeDeCompteTestCase)
    return suite
