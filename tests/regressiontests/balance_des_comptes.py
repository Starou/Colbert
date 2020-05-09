# -*- coding: utf-8 -*-

import os
import unittest
import codecs
import io
import datetime
import json

from decimal import Decimal

CURRENT_DIR = os.path.dirname(__file__)


class BalanceDesComptesTestCase(unittest.TestCase):
    def test_balance_des_comptes(self):
        from colbert.balance_des_comptes import balance_des_comptes
        grand_livre = codecs.open(os.path.join(CURRENT_DIR, "grand_livre-2011.json"),
                                  mode="r", encoding="utf-8")

        bdc = balance_des_comptes(json.loads(grand_livre.read()),
                                  label="Balance des comptes 2011 - MyBusiness")
        # Uncomment to generate.
        #from colbert.utils import json_encoder
        #output = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.json"),
        #                              mode="w+", encoding="utf-8")
        #output.write(json.dumps(bdc, default=json_encoder, indent=4))
        #output.close
        self.maxDiff = None
        self.assertEqual(
            bdc, {
                'comptes': [
                    {'nom': "Capital et compte de l'exploitant",
                     'numero': '100',
                     'solde_crediteur': Decimal('1500.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('1500.00'),
                     'total_debit': Decimal('0.00')},
                    {'nom': 'Clients - ventes de biens ou prestations de services',
                     'numero': '4111-CL1',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('24518.00'),
                     'total_debit': Decimal('24518.00')},
                    {'nom': 'Clients - ventes de biens ou prestations de services',
                     'numero': '4111-CL2',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('1794.00'),
                     'total_debit': Decimal('1794.00')},
                    {'nom': 'Clients - ventes de biens ou prestations de services',
                     'numero': '4111-CL3',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('8372.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('8372.00')},
                    {'nom': 'Clients - Factures \xe0 \xe9tablir',
                     'numero': '4181',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('13156.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('13156.00')},
                    {'nom': 'TVA \xe0 d\xe9caisser',
                     'numero': '44551',
                     'solde_crediteur': Decimal('3038.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('4278.00'),
                     'total_debit': Decimal('1240.00')},
                    {'nom': 'T.V.A. d\xe9ductible sur autres biens et services',
                     'numero': '44566',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('33.66'),
                     'total_debit': Decimal('33.66')},
                    {'nom': 'T.V.A. Collect\xe9e',
                     'numero': '44571',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('4312.00'),
                     'total_debit': Decimal('4312.00')},
                    {'nom': 'Taxes sur le CA sur factures \xe0 \xe9tablir',
                     'numero': '44587',
                     'solde_crediteur': Decimal('3528.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('7840.00'),
                     'total_debit': Decimal('4312.00')},
                    {'nom': 'Associ\xe9s - Comptes courants',
                     'numero': '455',
                     'solde_crediteur': Decimal('189.45'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('189.45'),
                     'total_debit': Decimal('0.00')},
                    {'nom': 'Banques',
                     'numero': '512',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('22679.35'),
                     'total_credit': Decimal('5132.65'),
                     'total_debit': Decimal('27812.00')},
                    {'nom': 'Achats - Fournitures de bureau',
                     'numero': '60225',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('21.44'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('21.44')},
                    {'nom': "Achats - Frais d'actes et de contentieux",
                     'numero': '6227',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('160.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('160.00')},
                    {'nom': 'Autres frais de commission sur prestations de services',
                     'numero': '6278-LCL',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('72.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('72.00')},
                    {'nom': 'Charges - Salaires et appointements',
                     'numero': '6411',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('3000.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('3000.00')},
                    {'nom': 'Charges - cotisations RSI',
                     'numero': '6411-RSI',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('393.00'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('393.00')},
                    {'nom': 'Charges - cotisations URSSAF - Allocations familliales',
                     'numero': '6411-URSF1',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('161.80'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('161.80')},
                    {'nom': 'Charges - cotisations URSSAF - CSG/RDS d\xe9ductible',
                     'numero': '6411-URSF2',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('153.31'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('153.31')},
                    {'nom': 'Charges - cotisations URSSAF - CSG/RDS non-d\xe9ductible',
                     'numero': '6411-URSF3',
                     'solde_crediteur': Decimal('0.00'),
                     'solde_debiteur': Decimal('86.89'),
                     'total_credit': Decimal('0.00'),
                     'total_debit': Decimal('86.89')},
                    {'nom': 'Produits - prestations de services',
                     'numero': '706',
                     'solde_crediteur': Decimal('40000.00'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('40000.00'),
                     'total_debit': Decimal('0.00')},
                    {'nom': 'Produits divers de gestion courante',
                     'numero': '758',
                     'solde_crediteur': Decimal('0.34'),
                     'solde_debiteur': Decimal('0.00'),
                     'total_credit': Decimal('0.34'),
                     'total_debit': Decimal('0.00')}
                ],
                'date_debut': datetime.date(2011, 3, 1),
                'date_fin': datetime.date(2011, 12, 31),
                'label': 'Balance des comptes 2011 - MyBusiness',
                'total_credits': Decimal('89598.10'),
                'total_debits': Decimal('89598.10'),
                'total_soldes_crediteurs': Decimal('48255.79'),
                'total_soldes_debiteurs': Decimal('48255.79')
            }
        )

    def test_balance_des_comptes_to_rst(self):
        from colbert.balance_des_comptes import balance_des_comptes_to_rst
        balance_des_comptes = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.json"),
                                          mode="r", encoding="utf-8")
        output = io.StringIO()
        # Uncomment to generate the file.
        #output = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.txt"),
        #                                      mode="w+", encoding="utf-8")
        balance_des_comptes_to_rst(json.loads(balance_des_comptes.read()), output)
        balance_des_comptes_txt = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.txt"),
                                              mode="r", encoding="utf-8")
        self.maxDiff = None
        self.assertEqual(output.getvalue(), balance_des_comptes_txt.read())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BalanceDesComptesTestCase)
    return suite
