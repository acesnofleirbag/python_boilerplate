.PHONY: test

run:
	unicorn ...

test:
	coverage run -m pytest

coverage:
	coverage report

linter:
	@isort --gitignore -n -l 80 --honor-noqa --color --om -q --sg .venv --sg docker .
	-@mypy --config-file mypy.ini ./src
	@black -l 80 --color --exclude "/(\.venv|__pycache__|docker)/" -q .
	@echo "[+] linter successfully executed"

clean:
	@find . -name '__pycache__' -exec rm -rf {} \;
