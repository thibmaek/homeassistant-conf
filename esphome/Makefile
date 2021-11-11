clean:
	rm -rf build/
	find . -maxdepth 1 -type d \
		-not \( -path . \) \
		-not \( -path .. \) \
		-not \( -path ./_archive \) \
		-not \( -path ./.vscode \) \
		-not \( -path ./assets \) \
		-not \( -path ./common \) \
		-not \( -path ./devices \) \
		-not \( -path ./test_utils \) \
		-print | xargs /bin/rm -rf

dependencies:
	pip install --upgrade -r requirements.txt

test:
	./test_utils/run_tests.sh setup_mock_env && \
		./test_utils/run_tests.sh compile_all
