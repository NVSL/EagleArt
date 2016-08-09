.PHONY: test_dist
test_dist:
	@echo Building source distribution
	python setup.py sdist
	rm -rf test_dist
	mkdir test_dist
	virtualenv test_dist/venv
	@echo Installing distribution in clean venv.  This will take a while...
#	@(. test_dist/venv/bin/activate; pip install dist/*-$$(cat VERSION.txt).tar.gz ); grep -q 'Failed.*Swoop' < build_test.log || (tail -10 build_test.log; echo FAILED; false)
	(. test_dist/venv/bin/activate; pip install dist/*-$$(cat VERSION.txt).tar.gz ); 
