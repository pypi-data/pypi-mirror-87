rm -rf dist
python3 setup.py bdist_wheel
python3 setup.py sdist
twine upload dist/*whl dist/*gz
