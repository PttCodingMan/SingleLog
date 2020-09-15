@echo off
cls

@rmdir /s /q dist
@rmdir /s /q single_log.egg-info
@rmdir /s /q single_log\__pycache__

python setup.py sdist
twine upload dist/*

echo Upload finish