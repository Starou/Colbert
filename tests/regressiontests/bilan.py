# -*- coding: utf-8 -*-

import os
import unittest
import codecs
import io
import datetime
import json
from decimal import Decimal

CURRENT_DIR = os.path.dirname(__file__)


class BilanTestCase(unittest.TestCase):
    def test_bilan(self):
        from colbert.bilan import bilan
        balance_des_comptes = codecs.open(os.path.join(CURRENT_DIR, "balance_des_comptes-2011.json"),
                                          mode="r", encoding="utf-8")

        b = bilan(json.loads(balance_des_comptes.read()), label="Bilan 2011 - MyBusiness")
        # Uncomment to generate.
        #from colbert.utils import json_encoder
        #output = codecs.open(os.path.join(CURRENT_DIR, "bilan-2011.json"),
        #                              mode="w+", encoding="utf-8")
        #output.write(json.dumps(b, default=json_encoder, indent=4))
        #output.close()
        #pprint(b)
        self.maxDiff = None
        self.assertEqual(b, {
            'actif': [['actif circulant',
                       [None,
                        ('client et comptes rattach\xe9s',
                         {'amortissement': Decimal('0.00'),
                          'brut': Decimal('21528.00'),
                          'net': Decimal('21528.00')}),
                        ('disponibilit\xe9s',
                         {'amortissement': Decimal('0.00'),
                          'brut': Decimal('22679.35'),
                          'net': Decimal('22679.35')})]]],
            'date_debut': datetime.date(2011, 3, 1),
            'date_fin': datetime.date(2011, 12, 31),
            'label': 'Bilan 2011 - MyBusiness',
            'passif': [['capitaux propres',
                        [None,
                         ('capital',
                          {'amortissement': Decimal('0.00'),
                           'brut': Decimal('1500.00'),
                           'net': Decimal('1500.00')}),
                         ('r\xe9sultat',
                          {'amortissement': Decimal('0.00'),
                           'brut': Decimal('35951.90'),
                           'net': Decimal('35951.90')})]],
                       ['dettes',
                        [None,
                         ('autres dettes',
                          {'amortissement': Decimal('0.00'),
                           'brut': Decimal('6755.45'),
                           'net': Decimal('6755.45')})]]],
            'total_actif': {'amortissement': Decimal('0.00'),
                            'brut': Decimal('44207.35'),
                            'net': Decimal('44207.35')}
        })

    def test_bilan_to_rst(self):
        import json
        from colbert.bilan import bilan_to_rst
        bilan = codecs.open(os.path.join(CURRENT_DIR, "bilan-2011.json"),
                            mode="r", encoding="utf-8")
        output = io.StringIO()
        # Uncomment to generate the file.
        # output = codecs.open(os.path.join(CURRENT_DIR, "bilan-2011.txt"),
        #                                   mode="w+", encoding="utf-8")
        bilan_to_rst(json.loads(bilan.read()), output)
        bilan_txt = codecs.open(os.path.join(CURRENT_DIR, "bilan-2011.txt"),
                                mode="r", encoding="utf-8")
        self.maxDiff = None
        self.assertEqual(output.getvalue(), bilan_txt.read())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BilanTestCase)
    return suite
