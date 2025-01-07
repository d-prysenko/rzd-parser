docs:
	python3 scripts/DocGenerator.py

parameters.json:
	cp parametes.dist.json parametes.json

deps:
	pip install -r requirements.txt
