from distutils.core import setup
import os
import sys

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(
    name="Colbert",
    version="0.1",
    license='BSD Licence',
    author='Stanislas Guerra',
    author_email='stanislas.guerra@gmail.com',
    description='Accountancy utilities for your small (french) business',
    long_description = README,
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
        'src/scripts/colbert_rapport_activite.py',
        'src/scripts/colbert_rapport_activite_to_tex.py',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
