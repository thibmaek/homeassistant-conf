.DEFAULT_GOAL := build

.PHONY: build
build: clean
	for config in devices/**/*.yaml; do \
		echo "🛠  Compiling ESPHome configuration: $$config"; \
		esphome compile $$config; \
	done

clean:
	rm -rf build/
	rm -rf devices/esp32/build
	rm -rf devices/esp8266/build
	rm -rf devices/lsc/build
	rm -rf devices/sonoff/build

dependencies:
	pip install --upgrade -r requirements.txt

test:
	./test_utils/run_tests.sh setup_mock_env && \
		./test_utils/run_tests.sh compile_all
