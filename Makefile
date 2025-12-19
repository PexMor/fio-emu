.PHONY: help build run-server run-fiocli run-inject clean

# Docker image name
IMAGE_NAME := fio-emu

# Detect OS for default host
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    DEFAULT_HOST := 172.17.0.1
else
    DEFAULT_HOST := 127.0.0.1
endif

# Configurable variables
HOST ?= $(DEFAULT_HOST)
PORT ?= 8080
CONTAINER_NAME := fio-emu-container

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker build -t $(IMAGE_NAME) .

run-server: build ## Run the API server (use HOST=... PORT=... to override defaults)
	@echo "Starting API server on $(HOST):$(PORT) (container listens on 0.0.0.0:8080)"
	docker run --rm -dt \
		--name $(CONTAINER_NAME) \
		-p $(HOST):$(PORT):8080 \
		-v $(HOME)/.config/fioemu:/root/.config/fioemu \
		$(IMAGE_NAME) \
		uv run fioemu --host 0.0.0.0 --port 8080

run-fiocli: build ## Run fiocli with arguments (use: make run-fiocli ARGS="--help")
	@if [ -z "$(ARGS)" ]; then \
		echo "Error: ARGS is required. Example: make run-fiocli ARGS='--help'"; \
		exit 1; \
	fi
	docker run --rm -it \
		-v $(HOME)/.config/fioemu:/root/.config/fioemu \
		-v $(PWD)/tmp:/app/tmp \
		$(IMAGE_NAME) \
		uv run fiocli $(ARGS)

run-inject: build ## Run the r01_make_inject.sh script inside the container (use API_HOST=... API_PORT=... to override defaults)
	@echo "🚀 Running inject script..."
	@docker run --rm -it \
		-v $(HOME)/.config/fioemu:/root/.config/fioemu \
		-v $(PWD)/tmp:/app/tmp \
		--network host \
		-e API_HOST=$(HOST) \
		-e API_PORT=$(PORT) \
		$(IMAGE_NAME) \
		bash -c "chmod +x /app/r01_make_inject.sh && /app/r01_make_inject.sh"
	@echo ""
	@echo "✅ Inject script completed successfully!"
	@echo ""
	@echo "📋 To verify the transactions, run this curl command:"
	@echo ""
	@bash -c ' \
		UNAME_S=$$(uname -s); \
		if [ "$$UNAME_S" = "Linux" ]; then \
			SDATE=$$(date +%Y-%m-%d -d "30 days ago"); \
			EDATE=$$(date +%Y-%m-%d -d "today"); \
		else \
			if command -v gdate >/dev/null 2>&1; then \
				SDATE=$$(gdate +%Y-%m-%d -d "30 days ago"); \
				EDATE=$$(gdate +%Y-%m-%d -d "today"); \
			else \
				SDATE=$$(date -v-30d +%Y-%m-%d); \
				EDATE=$$(date +%Y-%m-%d); \
			fi; \
		fi; \
		printf "   \033[1;36mcurl\033[0m \033[1;33m-X GET\033[0m \033[1;32m\"http://$(HOST):$(PORT)/v1/rest/periods/test-token/$$SDATE/$$EDATE/transactions.json\"\033[0m\n"; \
		printf "\n"; \
		printf "💡 Or use jq to format the JSON output:\n"; \
		printf "   \033[1;36mcurl\033[0m \033[1;33m-s\033[0m \033[1;32m\"http://$(HOST):$(PORT)/v1/rest/periods/test-token/$$SDATE/$$EDATE/transactions.json\"\033[0m \033[1;35m| jq\033[0m\n"; \
		printf "\n"; \
		printf "🔍 Navigate transactions with jq:\n"; \
		printf "   \033[1;36mcurl\033[0m \033[1;33m-s\033[0m \033[1;32m\"http://$(HOST):$(PORT)/v1/rest/periods/test-token/$$SDATE/$$EDATE/transactions.json\"\033[0m \033[1;35m| jq '\''.accountStatement.transactionList.transaction'\''\033[0m\n"; \
		printf "\n"'

clean: ## Remove the Docker image
	docker rmi $(IMAGE_NAME) || true
