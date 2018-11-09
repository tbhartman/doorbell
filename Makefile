test:
	pytest

coverage:
	pytest --cov=doorbell --cov-config=.coveragerc
	coverage html
	coverage report

style:
	flake8

dist:
	python2.7 setup.py sdist bdist_wheel
	python3.4 setup.py sdist bdist_wheel

pypi: dist
	twine upload dist/*

.PHONY: test coverage
