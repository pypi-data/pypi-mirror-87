Building: python setup.py sdist bdist_wheel

Upload build to test: python -m twine upload --repository testpypi dist/*

Upload build: python -m twine upload dist/*

