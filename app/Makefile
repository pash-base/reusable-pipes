install:
	pip install -e app/ --quiet

test:
	cd app && python -m pytest tests/unit/$(filter-out $@,$(MAKECMDGOALS)) -v

cover:
	cd app && python -m pytest tests/unit/ --cov=. --cov-config=.coveragerc --cov-report=html --cov-report=term-missing

lint:
	cd app && flake8 . --max-line-length=120 --exclude=tests,build,.venv

fmt:
	cd app && black . --line-length=120

validate:
	$(MAKE) fmt
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) cover
