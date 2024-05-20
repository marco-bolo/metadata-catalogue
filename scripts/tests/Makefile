# WP5 json files
WP5_INPUT_DIR := ./scripts/tests/input/WP5_json
WP5_OUTPUT_DIR := ./scripts/tests/output/WP5_jsonld

WP5_jsonld:
	@echo "Processing files in $(WP5_INPUT_DIR):"
	@for file in $(shell ls $(WP5_INPUT_DIR)); do \
		base_name=$$(basename $$file | cut -d. -f1); \
		echo "Processing $$file"; \
		$(MAKE) populate_template INPUT_DIR=$(WP5_INPUT_DIR) OUTPUT_DIR=$(WP5_OUTPUT_DIR) FILE=$$file BASE_NAME=$$base_name; \
	done

WP3_INPUT_DIR := ./scripts/tests/input/WP3_json
WP3_OUTPUT_DIR := ./scripts/tests/output/WP3_jsonld

WP3_jsonld:
	@echo "Processing files in $(WP3_INPUT_DIR):"
	@for file in $(shell ls $(WP3_INPUT_DIR)); do \
		echo "Processing $$file"; \
		base_name=$$(basename $$file | cut -d. -f1); \
		echo "Processing $$file"; \
		$(MAKE) populate_template INPUT_DIR=$(WP3_INPUT_DIR) OUTPUT_DIR=$(WP3_OUTPUT_DIR) FILE=$$file BASE_NAME=$$base_name; \
	done

populate_template:
	@echo "Running function on file: $(FILE)"
	pysubyt --input ./$(INPUT_DIR)/$(FILE) --templates ./ --name bioship.jsonld.ldt.j2 --output ./$(OUTPUT_DIR)/$(BASE_NAME).jsonld
	@echo "Function executed on $(FILE), result: $(BASE_NAME).jsonld"