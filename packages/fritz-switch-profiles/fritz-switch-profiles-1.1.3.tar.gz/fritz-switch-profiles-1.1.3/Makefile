.PHONY: clean beta lint
init:
	python -m pip install --upgrade pip flit
	flit install
	pre-commit install
build:
	flit build
clean:
	rm -rf dist/
publish:
	flit --repository pypi publish
beta:
	flit --repository testpypi publish
lint:
	flake8 fritz_switch_profiles
	pylint --rcfile=.pylintrc fritz_switch_profiles
	black --check fritz_switch_profiles
typing:
	mypy fritz_switch_profiles
all: lint
