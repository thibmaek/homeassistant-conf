install:
	pip install --upgrade pre-commit yamllint
	pre-commit install

lint:
	yamllint .
