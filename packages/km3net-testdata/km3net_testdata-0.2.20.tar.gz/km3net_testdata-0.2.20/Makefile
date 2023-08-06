PKGNAME=km3net_testdata

default: build

all: install

install: 
	pip install .

install-dev: dependencies-dev
	pip install -e .

venv:
	python3 -m venv venv

clean:
	python3 setup.py clean --all
	rm -rf venv

test: 
	py.test --junitxml=./reports/junit.xml -o junit_suite_name=$(PKGNAME) tests

test-cov:
	py.test --cov ./$(PKGNAME) --cov-report term-missing --cov-report xml:reports/coverage.xml --cov-report html:reports/coverage tests

test-loop: 
	py.test tests
	ptw --ext=.py,.pyx --ignore=doc tests

dependencies:
	pip install -Ur requirements.txt

dependencies-dev:
	pip install -Ur requirements-dev.txt

yapf:
	yapf -i -r $(PKGNAME)
	yapf -i -r tests
	yapf -i setup.py

.PHONY: all clean install install-dev venv test test-cov test-loop dependencies dependencies-dev yapf
