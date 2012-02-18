# -*- coding: utf-8 -*-

import os, sys
import unittest
import codecs
import StringIO
import datetime
import json
from colbert.utils import json_encoder
from pprint import pprint

from decimal import Decimal

CURRENT_DIR = os.path.dirname(__file__)

class CompteDeResultatTestCase(unittest.TestCase):
    def test_compte_de_resultat(self):
        from colbert.compte_de_resultat import compte_de_resultat
        balance_des_comptes = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.json"), 
                                          mode="r", encoding="utf-8")

        r = compte_de_resultat(json.loads(balance_des_comptes.read()),
                               label=u"Compte de résultat 2011 - MyBusiness")
        # Uncomment to generate.
        #output = codecs.open(os.path.join(CURRENT_DIR, "compte_de_resultat-2011.json"), 
        #                              mode="w+", encoding="utf-8")
        #output.write(json.dumps(r, default=json_encoder, indent=4))
        #output.close
        #pprint(r)
        self.maxDiff = None
        self.assertEqual(
            r,
            {u'charges': {u'exceptionnelles': {},
                          u'exploitation': {u'R\xe9mun\xe9rations du personnel': Decimal('3795.00'),
                                            u'autres services ext\xe9rieurs': Decimal('232.00'),
                                            u'fournitures non stockables': Decimal('21.44')},
                          u'financi\xe8res': {}},
             'date_debut': datetime.date(2011, 3, 1),
             'date_fin': datetime.date(2011, 12, 31),
             'label': u'Compte de r\xe9sultat 2011 - MyBusiness',
             u'produits': {u'exceptionnelles': {},
                           u'exploitation': {u'Autres produits de gestion courante': Decimal('0.34'),
                                             u'prestations de services': Decimal('40000.00')},
                           u'financi\xe8res': {}},
             'resultat': Decimal('35951.90'),
             'total_charges': Decimal('4048.44'),
             'total_produits': Decimal('40000.34')}
        )

    def test_compte_de_resultat_to_rst(self):
        from colbert.compte_de_resultat import compte_de_resultat_to_rst
        compte_de_resultat = codecs.open(os.path.join(CURRENT_DIR, "compte_de_resultat-2011.json"), 
                                          mode="r", encoding="utf-8")
        output = StringIO.StringIO()
        # Uncomment to generate the file.
        # output = codecs.open(os.path.join(CURRENT_DIR, "compte_de_resultat-2011.txt"), 
        #                                   mode="w+", encoding="utf-8")
        compte_de_resultat_to_rst(json.loads(compte_de_resultat.read()), output)
        compte_de_resultat_txt = codecs.open(os.path.join(CURRENT_DIR, "compte_de_resultat-2011.txt"), 
                                              mode="r", encoding="utf-8")
        self.maxDiff = None
        self.assertEqual(output.getvalue(), compte_de_resultat_txt.read())

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(CompteDeResultatTestCase)
    return suite
