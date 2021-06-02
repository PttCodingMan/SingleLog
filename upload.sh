rm -r dist
rm -r single_log.egg-info
rm -r single_log\__pycache__

python3 setup.py sdist
twine upload dist/*

echo Upload finish