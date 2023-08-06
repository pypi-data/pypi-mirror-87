.PHONY: all
all: help vars apphelp bapy green appdir ask base64auth confirmation is-pip package-info package-latest \
     package-latest-search pypifree tty-max upgrade-message github lumenbiomics nference nferx repo \
     repository wiki wiki-page info-all info-dist
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
SHELL := $(shell command -v bash)
DIR := $(shell git rev-parse --show-toplevel)
PROJECT := $(shell basename $(DIR))
APP := $(PROJECT)/__init__
ACTIVATE := $(DIR)/venv/bin/activate
COMMAND := source $(DIR)/venv/bin/activate; cd $(DIR)/$(PROJECT); python -m __init__

help: ## print Makefile help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

vars:  ## print Makefile vars
	@echo "DIR: $(DIR)"
	@echo "PROJECT: $(PROJECT)"
	@echo "APP: $(APP)"
	@echo "ACTIVATE: $(ACTIVATE)"

bapy:  ## bapy
	@echo "########################### bapy ######################################"
	@bash -c '$(COMMAND)'
	@echo "##########################################################################"

apphelp:  ## apphelp
	@echo "########################### apphelp ######################################"
	@bash -c '$(COMMAND) --help'
	@echo "##########################################################################"

green:  ## green
	@echo "########################### green ######################################"
	@bash -c '$(COMMAND) green "¡Buenas tardes!"'
	@echo "##########################################################################"

appdir:  ## appdir
	@echo "########################### appdir ######################################"
	@bash -c '$(COMMAND) appdir --stdout'
	@echo "##########################################################################"

ask:  ## ask
	@echo "########################### ask ######################################"
	@bash -c '$(COMMAND) ask "Would you like to start?"'
	@echo "##########################################################################"

base64auth:  ## base64auth
	@echo "########################### base64auth ######################################"
	@bash -c '$(COMMAND) base64auth upload upload --stdout'
	@echo "##########################################################################"

confirmation:  ## confirmation
	@echo "########################### confirmation ######################################"
	@bash -c '$(COMMAND) confirmation "Would you like to start?"'
	@echo "##########################################################################"

is-pip:  ## is-pip
	@echo "########################### is_pip ######################################"
	@bash -c '$(COMMAND) is-pip --stdout'
	@echo "##########################################################################"

package-info:  ## package-info
	@echo "########################### package-info ######################################"
	@bash -c '$(COMMAND) package-info --stdout'
	@echo "##########################################################################"

package-latest:  ## package-latest
	@echo "########################### package-latest ######################################"
	@bash -c '$(COMMAND) package-latest --stdout'
	@echo "##########################################################################"

package-latest-search:  ## package-latest-search
	@echo "########################### package-latest-search ######################################"
	@bash -c '$(COMMAND) package-latest-search --p requests --stdout'
	@echo "##########################################################################"

pypifree:  ## pypifree
	@echo "########################### pypifree ######################################"
	@bash -c '$(COMMAND) pypifree new_package_test --stdout'
	@echo "##########################################################################"

tty-max:  ## ttymax
	@echo "########################### ttymax ######################################"
	@bash -c '$(COMMAND) tty-max --stdout'
	@echo "##########################################################################"

upgrade-message:  ## upgrade-message
	@echo "########################### upgrade-message ######################################"
	@bash -c '$(COMMAND) upgrade-message'
	@echo "##########################################################################"

email:  ## email
	@echo "########################### email ######################################"
	@bash -c '$(COMMAND) email jose --stdout'
	@echo "##########################################################################"

github:  ## github
	@echo "########################### github ######################################"
	@bash -c '$(COMMAND) github --stdout'
	@echo "##########################################################################"

lumenbiomics:  ## lumenbiomics
	@echo "########################### lumenbiomics ######################################"
	@bash -c '$(COMMAND) lumenbiomics --repo bapy --stdout'
	@echo "##########################################################################"

nference:  ## nference
	@echo "########################### nference ######################################"
	@bash -c '$(COMMAND) nference --stdout'
	@echo "##########################################################################"

nferx:  ## nferx
	@echo "########################### nferx ######################################"
	@bash -c '$(COMMAND) nferx --stdout'
	@echo "##########################################################################"

repo:  ## repo
	@echo "########################### repo ######################################"
	@bash -c '$(COMMAND) repo --stdout'
	@echo "##########################################################################"

repository:  ## repository
	@echo "########################### repository ######################################"
	@bash -c '$(COMMAND) repository --stdout'
	@echo "##########################################################################"

wiki:  ## wiki
	@echo "########################### wiki ######################################"
	@bash -c '$(COMMAND) wiki --stdout'
	@echo "##########################################################################"

wiki-page:  ## wiki page
	@echo "########################### wiki page ######################################"
	@bash -c '$(COMMAND) wiki --number 1278738 --page Bapy --stdout'
	@echo "##########################################################################"

info-all:  ## info
	@echo "########################### info ######################################"
	@bash -c '$(COMMAND) info'
	@echo "##########################################################################"

info-dist:  ## info dist
	@echo "########################### info dist ######################################"
	@bash -c '$(COMMAND) info --dist bapy'
	@echo "##########################################################################"
