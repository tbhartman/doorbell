test:
	pytest

coverage:
	pytest --cov=doorbell --cov-config=.coveragerc
	coverage html
	coverage report

.PHONY: test coverage
