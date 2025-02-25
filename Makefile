# Define the script path based on the OS
ifeq ($(OS),Windows_NT)
	SCRIPT_DIR := .\\scripts\\windows\\
	EXT := .bat
else
	SCRIPT_DIR := ./scripts/
	EXT := .sh
endif

all: install test

install:
	$(SCRIPT_DIR)install$(EXT)

test:
	$(SCRIPT_DIR)test$(EXT)
