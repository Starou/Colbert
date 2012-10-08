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

class FacturesTestCase(unittest.TestCase):
    def test_calculer_facture(self):
        from colbert.factures import calculer_facture
        facture = codecs.open(os.path.join(CURRENT_DIR, "facture-1.json"), 
                              mode="r", encoding="utf-8")

        facture = calculer_facture(json.loads(facture.read()))
        #pprint(facture)
        # Uncomment to generate.
        #output = codecs.open(os.path.join(CURRENT_DIR, "facture-1_calculee.json"), 
        #                              mode="w+", encoding="utf-8")
        #output.write(json.dumps(facture, default=json_encoder, indent=4))
        #output.close()

        self.maxDiff = None
        self.assertDictEqual(
            facture, 
            {u'client': {u'adresse': u'1, Infinite Loop',
                         u'code_postal': u'11222',
                         u'nom': u'MyClient#1',
                         u'numero_compte': u'4111-CL1',
                         u'nom_compte': u'Clients - ventes de biens ou prestations de services',
                         u'reference_commande': u'XXXXX',
                         u'ville': u'Cupertino'},
             u'date_debut_execution': u'10/04/2011',
             u'date_facture': u'10/05/2011',
             u'date_fin_execution': u'30/04/2011',
             'date_reglement': datetime.date(2011, 7, 31),
             'date_debut_penalites': datetime.date(2011, 8, 1),
             u'deja_paye': u'0.00',
             u'detail': [{u'description': u'Prestation A.',
                          'montant_ht': Decimal('400.00'),
                          u'prix_unitaire_ht': u'100.00',
                          u'unite': u'jours',
                          u'quantite': u'4',
                          u'reference': u'ref-A',
                          u'taux_tva': u'19.6'},
                         {u'description': u'Prestation B.',
                          'montant_ht': Decimal('4960.89'),
                          u'prix_unitaire_ht': u'450.99',
                          u'unite': u'jours',
                          u'quantite': u'11',
                          u'reference': u'ref-B',
                          u'taux_tva': u'19.6'}],
             u'devise': u'Euro',
             'montant_ht': Decimal('5360.89'),
             'montant_ttc': Decimal('6411.62'),
             'reste_a_payer': Decimal('6411.62'),
             u'nb_jours_payable_fin_de_mois': u'60',
             u'numero_facture': u'YYYYYYY',
             u'symbole_devise': u'\u20ac',
             u'nom_compte': u'Produits - prestations de services',
             u'numero_compte': u'706',
             u'taux_penalites': u'11',
             'tva': {u'19.6': Decimal('1050.73')}}
        )

    def test_date_reglement_facture(self):
        from colbert.factures import date_reglement_facture
        self.assertEqual(date_reglement_facture("1/1/2011", 45), datetime.date(2011, 2, 28))
        self.assertEqual(date_reglement_facture("1/10/2012", 45), datetime.date(2012, 11, 30))
        self.assertEqual(date_reglement_facture("9/10/2012", 60), datetime.date(2012, 12, 31))
        self.assertEqual(date_reglement_facture("9/10/2012", 90), datetime.date(2013, 1, 31))

    def test_facture_to_tex(self):
        from colbert.factures import facture_to_tex
        facture = codecs.open(os.path.join(CURRENT_DIR, "facture-1_calculee.json"), 
                              mode="r", encoding="utf-8")
        tex_template = codecs.open(os.path.join(CURRENT_DIR, "facture-template.tex"), 
                                               mode="r", encoding="utf-8")
        output = StringIO.StringIO()
        # Uncomment to generate the file.
        #output = codecs.open(os.path.join(CURRENT_DIR, "facture-1.tex"), 
        #                                  mode="w+", encoding="utf-8")
        facture_to_tex(json.loads(facture.read()), tex_template, output)
        facture_tex = codecs.open(os.path.join(CURRENT_DIR, "facture-1.tex"), 
                                               mode="r", encoding="utf-8")
        self.maxDiff = None
        self.assertEqual(output.getvalue(), facture_tex.read())

    def test_ecriture_facture(self):
        from colbert.factures import ecriture_facture
        facture = codecs.open(os.path.join(CURRENT_DIR, "facture-1_calculee.json"), 
                              mode="r", encoding="utf-8")
        ecriture = ecriture_facture(json.loads(facture.read())) 
        self.maxDiff = None
        self.assertEqual(
            ecriture,
            {'date': datetime.date(2011, 5, 10),
             'ecritures': [
                 {'credit': Decimal('0.00'),
                  'debit': Decimal('6411.62'),
                  'nom_compte': u'Clients - ventes de biens ou prestations de services',
                  'numero_compte_credit': u'',
                  'numero_compte_debit': u'4111-CL1'},
                 {'credit': Decimal('5360.89'),
                  'debit': Decimal('0.00'),
                  'nom_compte': u'Produits - prestations de services',
                  'numero_compte_credit': u'706',
                  'numero_compte_debit': u''},
                 {'credit': Decimal('1050.73'),
                  'debit': Decimal('0.00'),
                  'nom_compte': u'Taxes sur le CA sur factures \xe0 \xe9tablir',
                  'numero_compte_credit': '44587',
                  'numero_compte_debit': u''}
             ],
             'intitule': u'Facture YYYYYYY MyClient#1'}
        )

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(FacturesTestCase)
    return suite
