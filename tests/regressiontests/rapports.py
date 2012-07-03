# -*- coding: utf-8 -*-

import os, sys
import unittest
import codecs
import StringIO
import datetime
import json
from pprint import pprint
from decimal import Decimal

from colbert.utils import json_encoder
from colbert.utils import decode_as_ecriture as as_ecriture


CURRENT_DIR = os.path.dirname(__file__)

class RapportsTestCase(unittest.TestCase):

    def test_rapport_activite(self):
        from colbert.rapports import rapport_activite

        calendrier = open(os.path.join(CURRENT_DIR, "Work.ics"), mode="r")
        rapport = rapport_activite(calendrier, 
                                   datetime.date(2012, 6, 1),
                                   datetime.date(2012, 6, 30),
                                   u"Rapport d'activité - Juin 2012",
                                   "2012-013")
        self.maxDiff = None
        self.assertEqual(rapport, {
            'nb_jours': 6,
            'ref_facture': '2012-013',
            'titre': u"Rapport d'activit\xe9 - Juin 2012",
            'detail': [[datetime.date(2012, 6, 1),
                        [{'from': '14.00', 'intitule': u'Stuff', 'to': '15.00'},
                         {'from': '17.00', 'intitule': u'More Stuff', 'to': '18.00'}]],
                       [datetime.date(2012, 6, 4),
                        [{'from': '09.00',
                          'intitule': u'Fix the printer',
                          'to': '10.00'}]],
                       [datetime.date(2012, 6, 5),
                        [{'from': None,
                          'intitule': u'A very long task, 3 days long.',
                          'to': None},
                         {'from': '09.00',
                          'intitule': u'Make some coffee',
                          'to': '10.00'},
                         {'from': '10.00', 'intitule': u'Nothing', 'to': '11.00'},
                         {'from': '14.00',
                          'intitule': u'Change some CSS stuffs.',
                          'to': '15.00'},
                         {'from': '18.00',
                          'intitule': u'Was there at a stupid brainstorming with marketing guys.',
                          'to': '19.00'},
                         {'from': '19.00',
                          'intitule': u'Add a nice Tweeter button on a random page',
                          'to': '19.30'}]],
                       [datetime.date(2012, 6, 6),
                        [{'from': None,
                          'intitule': u'A very long task, 3 days long.',
                          'to': None}]],
                       [datetime.date(2012, 6, 7),
                        [{'from': None,
                          'intitule': u'A very long task, 3 days long.',
                          'to': None}]],
                       [datetime.date(2012, 6, 13),
                        [{'from': None,
                          'intitule': u'Dreaming all day long...',
                          'to': None}]]],
        })

    def test_rapport_activite_to_tex(self):
        from colbert.rapports import rapport_activite_to_tex
        rapport_activite_json = codecs.open(os.path.join(CURRENT_DIR, "rapport_activite-1.json"), 
                                            mode="r", encoding="utf-8")
        tex_template = codecs.open(os.path.join(CURRENT_DIR, "rapport_activite-template.tex"), 
                                   mode="r", encoding="utf-8")
        output = StringIO.StringIO()
        dest_filename = os.path.join(CURRENT_DIR, "rapport_activite-1.tex")
        # Uncomment to generate the file.
        # output = codecs.open(dest_filename, mode="w+", encoding="utf-8")
        rapport_activite_to_tex(json.loads(rapport_activite_json.read(), object_hook=as_ecriture),
                                tex_template, output)
        rapport_activite_tex = codecs.open(dest_filename, mode="r", encoding="utf-8")
        self.maxDiff = None
        self.assertEqual(output.getvalue(), rapport_activite_tex.read())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(RapportsTestCase)
    return suite
