dependencies:
	pip install --upgrade pre-commit yamllint pip
	pre-commit install

lint:
	yamllint .
