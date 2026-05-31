install:
	pip install -e . --quiet

test:
	python -m pytest tests/unit/$(filter-out $@,$(MAKECMDGOALS)) -v

cover:
	python -m pytest tests/unit/ --cov=. --cov-config=.coveragerc --cov-report=html --cov-report=term-missing

lint:
	flake8 . --max-line-length=120 --exclude=tests,build,.venv

fmt:
	black . --line-length=120

validate:
	$(MAKE) fmt
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) cover
