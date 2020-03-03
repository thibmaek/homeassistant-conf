all: lint_yaml

lint_yaml: # Use yamllint to validate YAML files
	yamllint .
