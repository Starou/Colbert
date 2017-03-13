# -*- coding: utf-8 -*-

import os
import unittest
import codecs
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
            {
                'date': datetime.date(2011, 6, 30),
                'intitule': [u'Solde des comptes de TVA du 18/03/2011 au 30/06/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('294.00'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'},
                    {
                        'credit': Decimal('33.66'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('260.0'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA à décaisser',
                        'numero_compte_credit': '44551',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.34'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'Produits divers de gestion courante',
                        'numero_compte_credit': '758',
                        'numero_compte_debit': u''
                    }
                ]
            }
        )

        # Charge diverse pour équilibrer.
        livre_journal.seek(0)
        solde_tva = solde_comptes_de_tva(livre_journal,
                                         date_debut=datetime.date(2011, 4, 18),
                                         date_fin=datetime.date(2011, 6, 30))
        self.assertEqual(
            solde_tva,
            {
                'date': datetime.date(2011, 6, 30),
                'intitule': [u'Solde des comptes de TVA du 18/04/2011 au 30/06/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('294.00'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'
                    },
                    {
                        'credit': Decimal('4.21'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('290.0'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA à décaisser',
                        'numero_compte_credit': '44551',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('0.21'),
                        'nom_compte': u'Charges diverses de gestion courante',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '658'
                    }
                ]
            }
        )

        # Ecritures TVA plusieurs comptes, crédit en déduction.
        livre_journal = codecs.open(os.path.join(CURRENT_DIR, "livre-journal-tva.txt"),
                                    mode="r", encoding="utf-8")
        solde_tva = solde_comptes_de_tva(livre_journal,
                                         date_debut=datetime.date(2011, 3, 18),
                                         date_fin=datetime.date(2011, 6, 30))
        self.assertEqual(
            solde_tva,
            {
                'date': datetime.date(2011, 6, 30),
                'intitule': [u'Solde des comptes de TVA du 18/03/2011 au 30/06/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('294.00'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'
                    },
                    {
                        'credit': Decimal('36.46'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('258.0'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA à décaisser',
                        'numero_compte_credit': '44551',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('0.46'),
                        'nom_compte': u'Charges diverses de gestion courante',
                        'numero_compte_debit': '658',
                        'numero_compte_credit': u''
                    }
                ]
            }
        )

        # Remboursement de TVA en juillet.
        livre_journal.seek(0)
        solde_tva = solde_comptes_de_tva(livre_journal,
                                         date_debut=datetime.date(2011, 3, 18),
                                         date_fin=datetime.date(2011, 7, 31))
        self.assertEqual(
            solde_tva,
            {
                'date': datetime.date(2011, 7, 31),
                'intitule': [u'Solde des comptes de TVA du 18/03/2011 au 31/07/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('294.00'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'
                    },
                    {
                        'credit': Decimal('33.66'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('260.0'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA à décaisser',
                        'numero_compte_credit': '44551',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.34'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'Produits divers de gestion courante',
                        'numero_compte_credit': '758',
                        'numero_compte_debit': u''
                    }
                ]
            }
        )

        # Achat immobilisation en septembre, autre compte de TVA déductible.
        livre_journal.seek(0)
        solde_tva = solde_comptes_de_tva(livre_journal,
                                         date_debut=datetime.date(2011, 3, 18),
                                         date_fin=datetime.date(2011, 8, 31))
        self.assertEqual(
            solde_tva,
            {
                'date': datetime.date(2011, 8, 31),
                'intitule': [u'Solde des comptes de TVA du 18/03/2011 au 31/08/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('294.00'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'
                    },
                    {
                        'credit': Decimal('80.67'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA sur immobilisations',
                        'numero_compte_credit': '44562',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('33.66'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('180.0'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA à décaisser',
                        'numero_compte_credit': '44551',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('0.33'),
                        'nom_compte': u'Charges diverses de gestion courante',
                        'numero_compte_debit': '658',
                        'numero_compte_credit': u''
                    }
                ],
             }
        )

        # Créance en décembre
        livre_journal.seek(0)
        solde_tva = solde_comptes_de_tva(livre_journal,
                                         date_debut=datetime.date(2011, 12, 1),
                                         date_fin=datetime.date(2011, 12, 31))
        self.assertEqual(
            solde_tva,
            {
                'date': datetime.date(2011, 12, 31),
                'intitule': [u'Solde des comptes de TVA du 01/12/2011 au 31/12/2011'],
                'ecritures': [
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('2.02'),
                        'nom_compte': u'TVA collecté',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44571'
                    },
                    {
                        'credit': Decimal('8.20'),
                        'debit': Decimal('0.00'),
                        'nom_compte': u'TVA déductible sur autres biens et services',
                        'numero_compte_credit': '44566',
                        'numero_compte_debit': u''
                    },
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('6.0'),
                        'nom_compte': u'Crédit de TVA à reporter',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '44567'
                    },
                    {
                        'credit': Decimal('0.00'),
                        'debit': Decimal('0.18'),
                        'nom_compte': u'Charges diverses de gestion courante',
                        'numero_compte_credit': u'',
                        'numero_compte_debit': '658'
                    }
                ]
            }
        )


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TVATestCase)
    return suite
