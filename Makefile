SETUP_PY=setup.cfg


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2021.12.16/Makefile.venv"
	echo "8315a9dea1d018a67569abb2c40253b61bd42606f9334043af0d941cc87b5b64 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv


.PHONY: test
test: | venv $(VENV)/pytest
	$(VENV)/pytest $(PYTEST_ARGS)
