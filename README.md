# Playwright Test Automation Framework

Python-based test automation framework using Playwright and Pytest. Supports multiple projects with clean separation.

## Features

- Multi-task support (Swag Labs, Automation Test Store, etc.)
- Cross-browser testing (Chromium, Firefox, WebKit)
- BDD testing with pytest-bdd (Gherkin syntax)
- Page Object Model with YAML locators
- Environment-based configuration
- Parallel test execution
- HTML/Allure reporting

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Running Tests

> **📖 For comprehensive pytest commands reference, see [PYTEST_COMMANDS.md](PYTEST_COMMANDS.md)**

### Swag Labs (Default)

```bash
pytest tests/swag_labs/ -v
```

### Automation Test Store

**PowerShell:**
```powershell
$env:ENV = "automation_store"
pytest tests/automation_store/ -v
```

**Bash:**
```bash
ENV=automation_store pytest tests/automation_store/ -v
```

### BDD Tests (Automation Test Store)

**PowerShell:**
```powershell
# Install pytest-bdd first
pip install -r requirements.txt

# Run all BDD tests
$env:ENV = "automation_store"
pytest tests/automation_store/step_definitions/ -v

# Run with cross-browser
$env:ENV = "automation_store"
pytest tests/automation_store/step_definitions/ -v -m cross_browser --browsers chromium -n auto

# Run specific feature
$env:ENV = "automation_store"
pytest tests/automation_store/step_definitions/ -k "scenario_1" -v
```

**Bash:**
```bash
ENV=automation_store pytest tests/automation_store/step_definitions/ -v
```

### Cross-Browser Testing

**Swag Labs:**
```bash
# Single browser
pytest tests/swag_labs/test_scenarios.py -v -m cross_browser --browsers chromium -n auto

# Multiple browsers
pytest tests/swag_labs/test_scenarios.py -v -m cross_browser --browsers chromium,firefox -n auto

# All browsers (default)
pytest tests/swag_labs/test_scenarios.py -v -m cross_browser -n auto
```

**Automation Test Store:**
```bash
# Single browser
$env:ENV = "automation_store"
pytest tests/automation_store/ -v -m cross_browser --browsers chromium -n auto

# Multiple browsers
$env:ENV = "automation_store"
pytest tests/automation_store/ -v -m cross_browser --browsers chromium,firefox -n auto

# All browsers
$env:ENV = "automation_store"
pytest tests/automation_store/ -v -m cross_browser -n auto
```

**BDD Tests (Automation Test Store):**
```bash
# Single browser
$env:ENV = "automation_store"
pytest tests/automation_store/step_definitions/ -v -m cross_browser --browsers chromium -n auto

# All browsers
$env:ENV = "automation_store"
pytest tests/automation_store/step_definitions/ -v -m cross_browser -n auto
```

### Other Options

```bash
# Run specific markers
pytest -m smoke -v
pytest -m regression -v

# Run specific test
pytest tests/swag_labs/test_scenarios.py::test_scenario_2_valid_login -v

# Generate HTML report
pytest -v --html=reports/report.html --self-contained-html

# Parallel execution
pytest -n auto -v
```

## Project Structure

```
Playwright_Framework/
├── config/
│   └── config.yaml              # Environment configuration
├── locators/                    # Task-specific locators
│   ├── swag_labs/
│   └── automation_store/
├── src/
│   ├── pages/                   # Page objects
│   │   ├── base_page.py
│   │   ├── swag_labs/
│   │   └── automation_store/
│   └── utils/                   # Utilities
├── tests/                       # Test files
│   ├── swag_labs/
│   └── automation_store/
│       ├── features/            # BDD feature files (.feature)
│       └── step_definitions/    # BDD step definitions
├── conftest.py                  # Pytest fixtures
├── pytest.ini
└── requirements.txt
```

## Configuration

### Environments

Configured in `config/config.yaml`:
- `dev`: Swag Labs (default)
- `automation_store`: Automation Test Store

### Browser Selection

Set in `config.yaml` per environment or use `--browsers` flag for cross-browser tests.

### Test Data

Stored in `config/config.yaml` under `test_data` section.

## Adding New Task

1. Add environment in `config/config.yaml`
2. Create folders:
   - `src/pages/new_task/`
   - `locators/new_task/`
   - `tests/new_task/`
3. Create page objects inheriting from `BasePage`:
   ```python
   class NewTaskPage(BasePage):
       def __init__(self, page: Page):
           super().__init__(page, "page_name", task_name="new_task")
   ```
4. Run: `$env:ENV="new_task"; pytest tests/new_task/ -v`

## Reports

- HTML: `reports/report.html`
- Allure: `reports/allure/` (requires Allure CLI)
- Screenshots: `artifacts/screenshots/` (on failure)

## Troubleshooting

```bash
# Reinstall browsers
playwright install

# Check environment variable (PowerShell)
echo $env:ENV

# Run single test
pytest tests/swag_labs/test_scenarios.py::test_scenario_2_valid_login -v
```
