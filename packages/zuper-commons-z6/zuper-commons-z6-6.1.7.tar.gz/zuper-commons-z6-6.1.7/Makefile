
package=zuper_commons
package_test=zuper_commons_tests
packages_cover=$(package),$(package_test)

include pypackage.mk

bump-upload:
	$(MAKE) bump
	$(MAKE) upload

bump:
	bumpversion patch
	git push --tags
	git push --all

upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload dist/*


black:
	black -l 110 src
