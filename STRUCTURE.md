# Playwright Test Framework - Repository Structure

## 📁 Directory Structure

```
Playwright_Framework/
├── config/config.yaml              # Configuration with environments
├── src/
│   ├── pages/                      # Page Object Models
│   │   ├── base_page.py            # Base page class
│   │   └── login_page.py           # Login page
│   └── utils/                      # Utilities
│       ├── config_manager.py       # Configuration management
│       ├── logger.py               # Logging utilities
│       └── db.py                   # Database operations
├── locators/login.yaml             # Element locators
├── tests/                          # Test files
│   ├── test_login.py               # Login tests
│   └── test_example.py             # Example tests
├── conftest.py                     # Pytest configuration
├── pytest.ini                      # Pytest settings
├── requirements.txt                 # Dependencies
├── .pre-commit-config.yaml         # Code quality hooks
├── .github/workflows/tests.yml     # CI/CD workflow
└── README.md                       # Documentation
```

## 🚀 Key Features

- **Cross-browser testing** (Chromium, Firefox, WebKit)
- **Page Object Model** architecture
- **Centralized configuration** via YAML
- **HTML/Allure reporting** with artifacts
- **Database integration** with SQLAlchemy
- **Structured logging** and CI/CD ready

## 🧪 Usage

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run tests
pytest                           # All tests
pytest --browser=firefox        # Specific browser
pytest -m smoke                 # Smoke tests only
pytest -n auto                  # Parallel execution

# Generate HTML report
pytest -v --html=reports/report.html --self-contained-html
```

## 🔧 Configuration

Set environment via `ENV` variable:
- `ENV=dev` - Development environment
- `ENV=stage` - Staging environment  
- `ENV=prod` - Production environment

## 📊 Reports

- HTML reports: `reports/report.html`
- Allure reports: `reports/allure/`
- Screenshots on failure: `artifacts/screenshots/`
- Test videos: `artifacts/videos/`
