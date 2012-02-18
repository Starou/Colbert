all:	build

install:	all
	@python setup.py install

uninstall-home:
	@rm -rf ${HOME}/lib/python/colbert;
	@rm -rf ${HOME}/lib/python/colbert*;
	@rm -rf ${HOME}/bin/colbert_*;
	@echo "Colbert successfully uninstalled from your Home !"

install-home:	uninstall-home all
	@python setup.py install --home=~
	@echo "!!! Don't forget to add in ~/.bashrc : export PYTHONPATH=\$HOME/lib/python "
	@echo "!!! And check that PATH include ~/bin "

build:
	@python setup.py build

clean:
	@find . -name "*~" -exec rm -f {} \;
	@find . -name "*.pyc" -exec rm -f {} \;
	@find . -name "*.pyo" -exec rm -f {} \;
	@find . -name "*.swp" -exec rm -f {} \;

clean-build:
	@rm -rf ./build;
