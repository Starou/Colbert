from distutils.core import setup
import os
import sys


setup(
    name="Colbert",
    version="0.1",
    author='Stanislas Guerra',
    author_email='stanislas.guerra@gmail.com',
    description='',
    long_description = '',
    package_dir={'': 'src'},
    packages=['colbert', 
    ],
    data_files=[],
    scripts = [
        'src/scripts/colbert_check_livre_journal.py',
        'src/scripts/colbert_solde_de_compte.py',
        'src/scripts/colbert_grand_livre.py',
        'src/scripts/colbert_grand_livre_to_rst.py',
        'src/scripts/colbert_balance_des_comptes.py',
        'src/scripts/colbert_balance_des_comptes_to_rst.py',
        'src/scripts/colbert_bilan.py',
        'src/scripts/colbert_bilan_to_rst.py',
        'src/scripts/colbert_compte_de_resultat.py',
        'src/scripts/colbert_compte_de_resultat_to_rst.py',
        'src/scripts/colbert_ecritures_de_cloture.py',
        'src/scripts/colbert_ecritures_to_livre_journal.py',
        'src/scripts/colbert_solder_tva.py',
        'src/scripts/colbert_calculer_facture.py',
        'src/scripts/colbert_facture_to_tex.py',
        'src/scripts/colbert_ecriture_facture.py',
    ],
)
