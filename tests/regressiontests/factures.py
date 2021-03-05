# -*- coding: utf-8 -*-

import os
import unittest
import codecs
import io
import datetime
import json
from decimal import Decimal

CURRENT_DIR = os.path.dirname(__file__)


class FacturesTestCase(unittest.TestCase):
    def test_calculer_facture(self):
        from colbert.factures import calculer_facture
        facture = codecs.open(os.path.join(CURRENT_DIR, "facture-1.json"),
                              mode="r", encoding="utf-8")

        facture = calculer_facture(json.loads(facture.read()))
        #from pprint import pprint
        #from colbert.utils import json_encoder
        #pprint(facture)
        # Uncomment to generate.
        #output = codecs.open(os.path.join(CURRENT_DIR, "facture-1_calculee.json"),
        #                              mode="w+", encoding="utf-8")
        #output.write(json.dumps(facture, default=json_encoder, indent=4))
        #output.close()
        self.assertDictEqual(
            facture,
            {'client': {'adresse': '1, Infinite Loop',
                         'code_postal': '11222',
                         'nom': 'MyClient#1',
                         'numero_compte': '4111-CL1',
                         'nom_compte': 'Clients - ventes de biens ou prestations de services',
                         'reference_commande': 'XXXXX',
                         'ville': 'Cupertino'},
             'date_debut_execution': '10/04/2011',
             'date_facture': '10/05/2011',
             'date_fin_execution': '30/04/2011',
             'date_reglement': datetime.date(2011, 7, 31),
             'date_debut_penalites': datetime.date(2011, 8, 1),
             'deja_paye': '0.00',
             'detail': [{'description': 'Prestation A.',
                          'montant_ht': Decimal('400.00'),
                          'prix_unitaire_ht': '100.00',
                          'unite': 'jours',
                          'quantite': '4',
                          'reference': 'ref-A',
                          'taux_tva': '19.6'},
                         {'description': 'Prestation B.',
                          'montant_ht': Decimal('4960.89'),
                          'prix_unitaire_ht': '450.99',
                          'unite': 'jours',
                          'quantite': '11',
                          'reference': 'ref-B',
                          'taux_tva': '19.6'}],
             'devise': 'Euro',
             'montant_ht': Decimal('5360.89'),
             'montant_ttc': Decimal('6411.62'),
             'reste_a_payer': Decimal('6411.62'),
             'nb_jours_payable_fin_de_mois': '60',
             'numero_facture': 'YYYYYYY',
             'symbole_devise': '\u20ac',
             'nom_compte': 'Produits - prestations de services',
             'numero_compte': '706',
             'taux_penalites': '11',
             'tva': {'19.6': Decimal('1050.73')}}
        )

        facture = codecs.open(os.path.join(CURRENT_DIR, "facture-2.json"),
                              mode="r", encoding="utf-8")

        facture = calculer_facture(json.loads(facture.read()))
        self.assertDictEqual(
            facture,
            {'client': {'adresse': '1, Infinite Loop',
                         'code_postal': '11222',
                         'nom': 'MyClient#1',
                         'numero_compte': '4111-CL1',
                         'nom_compte': 'Clients - ventes de biens ou prestations de services',
                         'reference_commande': 'XXXXX',
                         'ville': 'Cupertino'},
             'date_debut_execution': '10/04/2011',
             'date_facture': '10/05/2011',
             'date_fin_execution': '30/04/2011',
             'date_reglement': datetime.date(2011, 7, 31),
             'date_debut_penalites': datetime.date(2011, 8, 1),
             'deja_paye': '0.00',
             'detail': [{'description': 'Prestation A.',
                          'montant_ht': Decimal('450.00'),
                          'prix_unitaire_ht': '100.00',
                          'unite': 'jours',
                          'quantite': '4.5',
                          'reference': 'ref-A',
                          'taux_tva': '19.6'},
                         {'description': 'Prestation B.',
                          'montant_ht': Decimal('5073.64'),
                          'prix_unitaire_ht': '450.99',
                          'unite': 'jours',
                          'quantite': '11.25',
                          'reference': 'ref-B',
                          'taux_tva': '19.6'}],
             'devise': 'Euro',
             'montant_ht': Decimal('5523.64'),
             'montant_ttc': Decimal('6606.27'),
             'reste_a_payer': Decimal('6606.27'),
             'nb_jours_payable_fin_de_mois': '60',
             'numero_facture': 'YYYYYYY',
             'symbole_devise': '\u20ac',
             'nom_compte': 'Produits - prestations de services',
             'numero_compte': '706',
             'taux_penalites': '11',
             'tva': {'19.6': Decimal('1082.63')}}
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
        output = io.StringIO()
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
                  'nom_compte': 'Clients - ventes de biens ou prestations de services',
                  'numero_compte_credit': '',
                  'numero_compte_debit': '4111-CL1'},
                 {'credit': Decimal('5360.89'),
                  'debit': Decimal('0.00'),
                  'nom_compte': 'Produits - prestations de services',
                  'numero_compte_credit': '706',
                  'numero_compte_debit': ''},
                 {'credit': Decimal('1050.73'),
                  'debit': Decimal('0.00'),
                  'nom_compte': 'Taxes sur le CA sur factures à établir',
                  'numero_compte_credit': '44587',
                  'numero_compte_debit': ''}
             ],
             'intitule': ['Facture YYYYYYY MyClient#1']}
        )


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(FacturesTestCase)
    return suite
