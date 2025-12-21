# Playwright Test Automation Framework

A production-grade test automation framework built with **Playwright + Pytest** in Python, designed to handle multiple test automation tasks with clean separation and scalability.

## 🚀 Features

- **Multi-Task Support**: Clean folder structure for multiple projects (Swag Labs, Automation Test Store, etc.)
- Cross-browser testing (Chromium, Firefox, WebKit)
- Page Object Model (POM) with task-specific YAML locators
- Centralized configuration via YAML (env-aware)
- XPath selector support for complex scenarios
- HTML/Allure reporting with screenshots on failures
- Structured logging and CI/CD ready

## 📋 Prerequisites

- Python 3.11+
- pip package manager

## 🛠️ Installation

```bash
# Clone and setup
git clone <repository-url>
cd Playwright_Framework

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## 🧪 Running Tests

### Running Swag Labs Tests (Default)

```bash
# Run all Swag Labs tests (default environment: dev)
pytest tests/swag_labs/ -v

# Or run all tests (includes all tasks)
pytest -v
```

### Running Automation Test Store Tests

**PowerShell (Windows):**
```powershell
# Set environment variable and run tests
$env:ENV = "automation_store"
pytest tests/automation_store/ -v

# Or in one line
$env:ENV="automation_store"; pytest tests/automation_store/ -v
```

**Bash/Linux/Mac:**
```bash
# Set environment variable and run tests
ENV=automation_store pytest tests/automation_store/ -v
```

### General Test Execution Options

```bash
# Run with specific browser
pytest -v --browser=chromium     # or firefox/webkit

# Run smoke or regression tests
pytest -m smoke -v
pytest -m regression -v

# Run in parallel
pytest -n auto -v

# Run specific test file
pytest tests/swag_labs/test_scenarios.py::test_scenario_1_invalid_password -v

# Generate HTML report (self-contained)
pytest -v --html=reports/report.html --self-contained-html

# Generate Allure results (choose reporter in config or CLI)
pytest -v --reporter=allure --alluredir=reports/allure
allure serve reports/allure
```

### Windows (PowerShell) quick open of report
```powershell
start .\reports\report.html
```

## ✅ Test Scenarios Covered

### Swag Labs (Sauce Demo) - `tests/swag_labs/`

- **Scenario 1**: Valid username + invalid password ⇒ assert error message
- **Scenario 2**: Valid credentials ⇒ assert dashboard loaded (`/inventory.html`)
- **Scenario 3**: Sort items low→high, add two lowest to cart ⇒ verify quantities and prices
- **Scenario 4**: Menu → About ⇒ assert text on page

### Automation Test Store - `tests/automation_store/`

- **Scenario 1**: Login → Scroll to brands → Select DOVE brand → Add newest item to cart → Verify item, quantity, and amount (using XPath selectors)

## 🏗️ Project Structure

```
Playwright_Framework/
├── config/
│   └── config.yaml                    # Multi-environment configuration
├── locators/                          # Task-specific YAML locators
│   ├── swag_labs/                    # Swag Labs locators
│   │   ├── swag_login.yaml
│   │   ├── swag_inventory.yaml
│   │   └── swag_cart.yaml
│   └── automation_store/             # Automation Test Store locators
│       ├── login.yaml
│       ├── home.yaml
│       ├── product.yaml
│       └── cart.yaml
├── src/
│   ├── pages/
│   │   ├── base_page.py              # Base page class (supports task-specific locators)
│   │   ├── swag_labs/                # Swag Labs page objects
│   │   │   ├── login_page.py
│   │   │   ├── inventory_page.py
│   │   │   └── cart_page.py
│   │   └── automation_store/         # Automation Test Store page objects
│   │       ├── login_page.py
│   │       ├── home_page.py
│   │       ├── product_page.py
│   │       └── cart_page.py
│   └── utils/                        # Utilities
│       ├── config_manager.py
│       ├── logger.py
│       └── db.py
├── tests/
│   ├── swag_labs/                    # Swag Labs tests
│   │   └── test_scenarios.py
│   └── automation_store/            # Automation Test Store tests
│       └── test_scenario_1.py
├── conftest.py                       # Pytest fixtures
├── pytest.ini                        # Pytest configuration
├── requirements.txt                  # Dependencies
└── README.md                         # This file
```

## ⚙️ Configuration

### Environments

The framework supports multiple environments defined in `config/config.yaml`:

- **`dev`**: Swag Labs (Sauce Demo) - `https://www.saucedemo.com` (default)
- **`automation_store`**: Automation Test Store - `https://automationteststore.com/`

### Switching Environments

**PowerShell (Windows):**
```powershell
# Set environment variable
$env:ENV = "automation_store"
pytest tests/automation_store/ -v

# Or in one line
$env:ENV="automation_store"; pytest tests/automation_store/ -v
```

**Bash/Linux/Mac:**
```bash
ENV=automation_store pytest tests/automation_store/ -v
```

### Browser Configuration

- Browser can be set per environment in `config/config.yaml`
- Or overridden via CLI: `--browser=chromium|firefox|webkit`

### Test Data

Test data (credentials, test users, etc.) is stored in `config/config.yaml` under the `test_data` section, organized by task.

## 📊 Reports

- Select reporter via `config/config.yaml` → `reporting.reporter: html|allure` or override with CLI `--reporter`.
- HTML reports: `reports/report.html`
- Allure results: `reports/allure/` (requires Allure CLI to view)
- Screenshots on failure: `artifacts/screenshots/`

## 📝 Logging

Structured logging to console and `logs/` (JSON). Example:
```python
from src.utils.logger import get_logger
logger = get_logger(__name__)
logger.info("Running Swag Labs tests")
```

## 🐛 Troubleshooting

```bash
# Install/update browsers
playwright install

# Increase timeout if external navigations are slow
pytest -v --timeout=90  # or adjust config/global timeout in config.yaml

# Run a single scenario
pytest -v tests/swag_labs/test_scenarios.py::test_scenario_2_valid_login

# Run Automation Test Store test (PowerShell)
$env:ENV="automation_store"; pytest tests/automation_store/test_scenario_1.py -v

# Check if environment is set correctly (PowerShell)
echo $env:ENV
```

### Common Issues

1. **Environment variable not working in PowerShell**: Use `$env:ENV = "value"` instead of `ENV=value`
2. **Locator not found**: Ensure locator files are in the correct task subfolder (`locators/task_name/`)
3. **Import errors**: Verify page objects are in the correct task subfolder (`src/pages/task_name/`)

## 🤝 Adding New Tasks/Projects

To add a new automation task:

1. **Add environment** in `config/config.yaml`:
   ```yaml
   environments:
     new_task:
       base_url: "https://example.com"
       browser: "chromium"
       timeout: 30000
   ```

2. **Create folder structure**:
   - `src/pages/new_task/` - Page objects
   - `locators/new_task/` - Locator YAML files
   - `tests/new_task/` - Test files

3. **Create page objects** following the pattern:
   ```python
   class NewTaskPage(BasePage):
       def __init__(self, page: Page):
           super().__init__(page, "page_name", task_name="new_task")
   ```

4. **Run tests**:
   ```powershell
   $env:ENV="new_task"; pytest tests/new_task/ -v
   ```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add/adjust page objects and locators as needed
4. Follow the task-based folder structure
5. Submit pull request

## 📄 License

MIT License

---

**Happy Testing! 🧪✨**
