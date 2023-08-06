default_targets=tox
test: $(default_targets)
.PHONY: test

tox:
	@python3 -m venv .env
	@.env/bin/pip install tox
	@.env/bin/tox -e py27,py36,py37,flake8,flake8python2 --parallel=auto ${TOX_POSARGS}
.PHONY: tox
