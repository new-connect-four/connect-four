# Zmienne
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
REQUIREMENTS = requirements.txt

# Wyswietla pomoc
help:
	@echo "Dostępne komendy:"
	@echo "  make setup       - Tworzy srodowisko wirtualne i instaluje potrzebne biblioteki"
	@echo "  make terminal    - Uruchamia gre w trybie terminal"
	@echo "  make gui         - Uruchamia gre w trybie GUI"
	@echo "  make help        - Wyświetla tą pomoc"

# Tworzy srodowisko wirtualne i instaluje potrzebne biblioteki
.PHONY: setup
setup:
	@echo "Tworzenie srodowiska wirtualnego..."
	@python3 -m venv $(VENV_DIR)
	@echo "Instalowanie bibliotek..."
	@$(PIP) install -r $(REQUIREMENTS)
	@echo "Installacja zakończona."

# Uruchamia gre w trybie terminal
.PHONY: terminal
terminal:
	@$(PYTHON) -m src.terminal.main

# Run GUI module
.PHONY: gui
gui:
	@$(PYTHON) -m src.gui.main
