dependencies:
	pip install -r requirements.txt
	pre-commit install

lint:
	yamllint .
