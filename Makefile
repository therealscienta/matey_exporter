################################################################################
# Makefile for the matey_exporter project.
#
# This Makefile provides the following targets:
# - `help`: Displays a help message with the available targets.
# - `build`: Builds the project using PyInstaller, creating a standalone executable.
# - `test`: Runs the project's test suite using pytest.
# - `install`: Runs the `test` and `build` targets, then executes the `install.sh` script.
# - `clean`: Removes all generated files and directories, including the virtual environment.
#
# The Makefile also checks that the required Python version (>= 3.11) is installed and available in the system's PATH.
################################################################################

# TODO


.PHONY = help build test install clean
.DEFAULT_GOAL = help
PYTHON=$(shell command -v python3)
GREEN="\n\n\033[0;32m\#\#\# "
NC=" \#\#\#\033[0m\n"

# Check if Python is available in the system's PATH
ifeq (, $(PYTHON))
    $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif


# Check for supporten Python version
PYTHON_VERSION_MIN=3.10
PYTHON_VERSION_CUR=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys; cur_ver = sys.version_info[0:2]; min_ver = tuple(map(int, "$(PYTHON_VERSION_MIN)".split("."))); print(int(cur_ver >= min_ver))')
ifeq ($(PYTHON_VERSION_OK), 0)
    $(error "Need python version >= $(PYTHON_VERSION_MIN). Current version is $(PYTHON_VERSION_CUR)")
endif

# Check for python-venv package
PYTHON_VENV_CHECK := $(shell dpkg-query -W -f='${Version}' python$(PYTHON_VERSION_CUR)-venv >/dev/null 2>&1 && echo "0" || echo "1")
ifeq ($(PYTHON_VENV_CHECK), 0)
    $(error "python$(PYTHON_VERSION_CUR)-venv package is not installed. Install it with: sudo apt-get install python$(PYTHON_VERSION_CUR)-venv")
endif

VENV_ROOT=venv
VENV_BIN=$(VENV_ROOT)/bin
VENV_PIP=$(VENV_BIN)/pip3
VENV_PYTHON=$(VENV_BIN)/python
APP_VERSION=$(shell $(VENV_PYTHON) -c 'import matey_exporter; print(matey_exporter.__version__)')


# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To build the project type make build"
	@echo "To install the project type make install"
	@echo "------------------------------------"


$(VENV)/bin/activate: requirements.txt
	@echo $(GREEN)Checking if Python virtual environment needs to be set up...$(NC)
	@if [ ! -d "venv" ]; then $(PYTHON) -m venv $(VENV_ROOT); fi
	$(VENV_PIP) install -r requirements.txt


test: $(VENV)/bin/activate
	@echo $(GREEN)Running tests...$(NC)
	@$(VENV_PYTHON) -m pytest


build: $(VENV)/bin/activate
	@echo $(GREEN)Building project...$(NC)
	@$(VENV_BIN)/pyinstaller -F -n matey_exporter-$(APP_VERSION) -c "app.py"


install: test build
	
	@echo $(GREEN)Running install script...$(NC)
	@chmod +x install.sh
	@./install.sh $(APP_VERSION)

clean:
	@echo $(GREEN)Cleaning up...$(NC)
	@rm -rf __pycache__ build/ .pytest_cache/ main.spec $(VENV)
