
tag=duckietown_pondcleaner

regular_packages=duckietown_build_utils
test_packages=duckietown_build_utils_tests

include common.mk



bump: # v2
	bumpversion patch
	git push --tags
	git push

upload: # v3
	dts build_utils check-not-dirty
	dts build_utils check-tagged
	dt-check-need-upload --package duckietown-build-utils-daffy make upload-do

upload-do:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload --skip-existing --verbose dist/*


bump-upload:
	$(MAKE) bump
	$(MAKE) upload

#
#test:
#	nosetests duckietown_build_utils

test-circleci-local:
	circleci local execute --job test-3.8 \
		-e CIRCLE_PROJECT_USERNAME=duckietown \
		-e CIRCLE_PROJECT_REPONAME=aido-utils \
		-e SKIP_CODECOV=1
	#-e PIP_INDEX_URL=$(PIP_INDEX_URL)
