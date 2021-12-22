SETUP_PY=setup.cfg
REQUIREMENTS_TXT=requirements.dev


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2021.12.16/Makefile.venv"
	echo "8315a9dea1d018a67569abb2c40253b61bd42606f9334043af0d941cc87b5b64 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv


ifeq (Windows_NT,$(OS))
# https://github.com/tox-dev/tox/issues/1550
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
endif


.PHONY: test
test: test-tox


.PHONY: test-tox
test-tox: | venv $(VENV)/tox
	$(VENV)/tox $(TOX_ARGS)


.PHONY: test-pytest
test-pytest: | venv $(VENV)/pytest
	$(VENV)/pytest $(PYTEST_ARGS)


samples/%.png samples/%.svg: samples/%.py | venv
	$(VENV)/python $< $@


.PHONY: package build
package build: dist
dist: src setup.cfg pyproject.toml README.md LICENSE
dist: | venv $(VENV)/build
	-$(RM) -rv dist
	$(VENV)/python -m build


.PHONY: clean
clean:
	-$(RM) -rv dist


.PHONY: upload
upload: dist | $(VENV)/twine
	$(VENV)/twine upload --repository testpypi $(TWINE_ARGS) dist/*
	$(VENV)/twine upload $(TWINE_ARGS) dist/*
