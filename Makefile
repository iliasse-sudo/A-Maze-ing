MAIN = a_maze_ing.py
CONFIG = config.txt
CACHE = */__pycache__ .mypy_cache maze/__pycache__ *.egg-info

build:
	python3 -m build && mv dist/*.whl .

install:
	python3 -m pip install -e .
	python3 -m pip install flake8 mypy build

install-package:
	python3 -m pip install mazegen-1.0.0-py3-none-any.whl

run:
	python3 $(MAIN) $(CONFIG)

run-installed:
	maze-run $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf build/ dist/
	rm -rf $(CACHE)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .
	mypy maze/ a_maze_ing.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 && mypy . --strict

.PHONY: build install clean run run-installed debug lint lint-strict install-package
