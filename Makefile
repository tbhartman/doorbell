test:
	pytest

coverage:
	pytest --cov=doorbell --cov-config=.coveragerc
	coverage html
	coverage report

style:
	flake8

.PHONY: test coverage style
