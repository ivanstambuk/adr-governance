# ADR Governance — Common Tasks
# Run `make` or `make help` to see available targets.

.DEFAULT_GOAL := help

.PHONY: help install validate lint render bundle llms-full review summarize all

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

validate: ## Validate all ADR YAML files against the schema
	python3 scripts/validate-adr.py architecture-decision-log/ examples-reference/

lint: ## Run YAML lint on all ADR files
	yamllint -c .yamllint.yml architecture-decision-log/ examples-reference/

render: ## Render all ADRs to Markdown
	python3 scripts/render-adr.py --output-dir rendered/ --generate-index architecture-decision-log/
	python3 scripts/render-adr.py --output-dir examples-reference/rendered/ --generate-index examples-reference/

bundle: ## Generate the repomix bundle for AI chat
	./scripts/bundle.sh

llms-full: ## Regenerate llms-full.txt from source docs
	./scripts/generate-llms-full.sh

review: ## Generate a review prompt for an ADR (usage: make review ADR=path/to/file.yaml)
	python3 scripts/review-adr.py $(ADR)

summarize: ## Summarize ADRs for stakeholders (usage: make summarize ADR=path/to/file.yaml)
	python3 scripts/summarize-adr.py $(ADR)

all: validate lint render llms-full ## Run validate + lint + render + llms-full
