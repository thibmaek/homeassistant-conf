clean:
	find . -maxdepth 1 -type d \
		-not \( -path . \) \
		-not \( -path .. \) \
		-not \( -path ./_archive \) \
		-not \( -path ./.vscode \) \
		-not \( -path ./assets \) \
		-not \( -path ./common \) \
		-print | xargs /bin/rm -rf

build:
	./test_esphome.sh compile_all

install:
	pip install --upgrade -r requirements.txt
test:
	./test_esphome.sh setup_mock_env && \
		./test_esphome.sh compile_all
