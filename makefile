PYTHON_VERSION_NEEDED = 3.8
VENV_NAME = POS-venv
PYTHON_BIN = $(VENV_NAME)/bin/python
PIP_BIN = $(VENV_NAME)/bin/pip
REQUIREMENTS_FILE = requirements.txt
PROJECT_NAME = POS

.PHONY: setup install run run-clover clean

setup: $(VENV_NAME) install
	@echo "✅ Setup completed successfully!"

$(VENV_NAME):
	@echo "🐍 Creating common Python virtual environment..."
	python3 -m venv $(VENV_NAME)

install: $(VENV_NAME)
	@echo "📦 Installing Python dependencies from clover..."
	$(PIP_BIN) install --quiet --disable-pip-version-check -r $(REQUIREMENTS_FILE)
	@echo "✅ Dependencies installed successfully"

run: run-clover

run-clover:
	@echo " ⏳ Running Clover POS..."
	cd clover && ../$(PYTHON_BIN) main.py

clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV_NAME)
	@echo "✅ Cleaned up successfully!"