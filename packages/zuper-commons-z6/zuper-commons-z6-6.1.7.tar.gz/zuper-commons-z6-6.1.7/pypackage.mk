# Generic Makefile for python package providing testing/installation.

# (common version)

.PHONY: docs all develop test

all: develop

develop:
	python3 setup.py develop

docs:
	make -C docs

coverage_dir=coverage_information
nose=nosetests --with-id
nose_parallel=--processes=16 --process-timeout=300 --process-restartworker
nose_coverage=--with-coverage --cover-html --cover-html-dir $(coverage_dir)  --cover-package=$(packages_cover)

test:
	@echo Overview for running tests for package $(package):
	@echo
	@echo - Use 'make test-failed' to redo only failed tests
	@echo - Use 'make test-parallel' to enable parallel testing
	@echo - Use 'make test-coverage' to do coverage testing
	@echo - Use the env. var. NOSE_PARAMS to pass extra arguments.
	@echo
	@echo For example:
	@echo   NOSE_PARAMS='--nologcapture -s -v' make test-failed
	@echo
	@echo

	$(MAKE) test-coverage


test-stop:
	$(nose) $(package_test) $(NOSE_PARAMS) -x

test-failed:
	$(nose) $(package_test) $(NOSE_PARAMS) --failed

test-parallel:
	$(nose) $(package_test) $(NOSE_PARAMS) $(nose_parallel)

test-parallel-stop:
	$(nose) $(package_test) $(NOSE_PARAMS) $(nose_parallel) -x

test-coverage:
	rm -f .coverage
	$(nose) $(package_test) $(NOSE_PARAMS) $(nose_coverage)

