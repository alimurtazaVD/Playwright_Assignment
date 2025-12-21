# Playwright Test Framework - Repository Structure

## 📁 Complete Directory Structure

```
Playwright_Framework/
├── 📁 config/
│   └── 📄 config.yaml                    # Configuration file with environments
├── 📁 src/
│   ├── 📁 pages/                         # Page Object Models
│   │   ├── 📄 __init__.py                # Package initialization
│   │   ├── 📄 base_page.py               # Base page class with common methods
│   │   └── 📄 login_page.py              # Login page implementation
│   ├── 📁 utils/                         # Utility modules
│   │   ├── 📄 __init__.py                # Package initialization
│   │   ├── 📄 config_manager.py          # Configuration management
│   │   ├── 📄 logger.py                  # Structured logging utilities
│   │   └── 📄 db.py                      # Database connectivity (SQLAlchemy)
│   └── 📄 __init__.py                    # Package initialization
├── 📁 locators/                          # Element locators (YAML)
│   └── 📄 login.yaml                     # Login page locators
├── 📁 tests/                             # Test files
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 test_login.py                  # Login functionality tests
│   └── 📄 test_example.py                # Example tests
├── 📁 .github/                           # GitHub configuration
│   └── 📁 workflows/                     # CI/CD workflows
│       └── 📄 tests.yml                  # GitHub Actions workflow
├── 📁 artifacts/                         # Test artifacts (auto-generated)
│   ├── 📁 screenshots/                   # Screenshots on failure
│   ├── 📁 videos/                        # Test execution videos
│   └── 📁 har/                           # HTTP Archive files
├── 📁 logs/                              # Log files (auto-generated)
├── 📁 reports/                           # Test reports (auto-generated)
│   ├── 📄 report.html                    # HTML test report
│   └── 📁 allure/                        # Allure reports
├── 📄 requirements.txt                   # Python dependencies
├── 📄 pytest.ini                        # Pytest configuration
├── 📄 conftest.py                       # Pytest fixtures and configuration
├── 📄 .pre-commit-config.yaml           # Pre-commit hooks configuration
├── 📄 README.md                          # Main documentation
└── 📄 REPOSITORY_STRUCTURE.md            # This file
```

## 🏗️ Architecture Overview

### Core Components

1. **Configuration Management** (`config/config.yaml`)
   - Environment-specific settings
   - Browser configurations
   - Test data and timeouts
   - Reporting options

2. **Page Object Model** (`src/pages/`)
   - `BasePage`: Common functionality for all pages
   - `LoginPage`: Specific login page implementation
   - Locator management via YAML files

3. **Utilities** (`src/utils/`)
   - `ConfigManager`: Load and manage configuration
   - `Logger`: Structured logging with JSON and console output
   - `DatabaseManager`: SQLAlchemy-based database operations

4. **Test Framework** (`tests/`)
   - Pytest-based test structure
   - Page Object usage examples
   - Data-driven testing
   - Test markers (smoke, regression, flaky)

5. **CI/CD Integration** (`.github/workflows/`)
   - Multi-browser testing
   - Parallel execution
   - Artifact management
   - Code quality checks

## 🔧 Key Features

### Cross-Browser Support
- **Chromium**: Chrome-based browser
- **Firefox**: Mozilla Firefox
- **WebKit**: Safari engine

### Test Execution
- **Sequential**: Single-threaded execution
- **Parallel**: Multi-worker execution
- **Markers**: Test categorization and filtering
- **Retries**: Automatic retry on failure

### Reporting
- **HTML Reports**: Self-contained HTML reports
- **Allure Reports**: Rich interactive reports
- **JUnit XML**: CI/CD integration
- **Screenshots**: Automatic capture on failure
- **Videos**: Test execution recordings

### Configuration
- **Environment Variables**: Runtime configuration
- **YAML Config**: Structured configuration files
- **Browser Override**: Command-line browser selection
- **Headless Mode**: Background execution option

## 🚀 Usage Examples

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with specific browser
pytest --browser=firefox

# Run smoke tests only
pytest -m smoke

# Run in parallel
pytest -n auto
```

### Environment-Specific Testing
```bash
# Development environment
ENV=dev pytest

# Staging environment
ENV=stage pytest

# Production environment
ENV=prod pytest
```

### HTML Report and Parallel Examples
```bash
# Install dependencies and browsers
pip install -r requirements.txt
playwright install

# Run smoke tests in parallel
pytest -m smoke -n auto -v

# Generate HTML report
pytest -v --html=reports/report.html --self-contained-html
```

## 📊 Test Structure

### Test Classes
- **TestLogin**: Login functionality tests
- **TestExample**: Framework demonstration tests

### Test Markers
- **@pytest.mark.smoke**: Critical path tests
- **@pytest.mark.regression**: Comprehensive tests
- **@pytest.mark.flaky**: Potentially unstable tests

### Test Data
- **Valid Credentials**: admin/admin
- **Invalid Credentials**: invalid/wrong
- **Empty Credentials**: ""/""

## 🔍 Monitoring and Debugging

### Logging
- **Console Output**: Colored, formatted logs
- **File Logs**: JSON-structured logs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR

### Artifacts
- **Screenshots**: Visual test state
- **Videos**: Test execution recording
- **HAR Files**: Network activity logs
- **Page Source**: HTML content on failure

### Debug Mode
```bash
# Enable debug logging
pytest --log-cli-level=DEBUG

# Run single test with verbose output
pytest -vvs tests/test_login.py::TestLogin::test_successful_login
```

## 🛠️ Development Workflow

### Pre-commit Hooks
- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Type checking
- **Pre-commit**: Automatic quality checks

### Code Quality
- **Black**: Consistent code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Isort**: Import statement sorting

### Testing Best Practices
- **Page Object Model**: Separation of concerns
- **Locator Management**: Centralized element identification
- **Test Data**: Externalized test data
- **Assertions**: Clear, descriptive assertions

## 📈 Performance and Scalability

### Parallel Execution
- **Auto-detection**: Automatic worker count detection
- **Configurable**: Manual worker count specification
- **Resource Management**: Efficient resource utilization

### Browser Management
- **Session Reuse**: Efficient browser instance management
- **Context Isolation**: Test isolation via browser contexts
- **Resource Cleanup**: Automatic cleanup of resources

### Memory Management
- **Page Cleanup**: Automatic page cleanup
- **Context Cleanup**: Context resource management
- **Browser Cleanup**: Browser instance cleanup

## 🔒 Security and Best Practices

### Data Handling
- **Environment Variables**: Secure configuration management
- **Database Isolation**: Test data isolation
- **Credential Management**: Secure test credential handling

### Test Isolation
- **Browser Contexts**: Isolated browser sessions
- **Database Transactions**: Rollback test data changes
- **File Cleanup**: Automatic artifact cleanup

### CI/CD Security
- **Secret Management**: Secure credential handling
- **Artifact Security**: Secure artifact storage
- **Access Control**: Repository access management

## 📚 Learning Resources

### Framework Components
- **BasePage**: Common page functionality
- **ConfigManager**: Configuration handling
- **Logger**: Logging utilities
- **DatabaseManager**: Database operations

### Test Patterns
- **Page Object Model**: UI interaction patterns
- **Data-Driven Testing**: Parameterized test execution
- **Test Hooks**: Setup and teardown patterns
- **Assertion Patterns**: Effective test validation

### Best Practices
- **Locator Strategy**: Reliable element identification
- **Wait Strategies**: Effective element waiting
- **Error Handling**: Robust error management
- **Test Organization**: Logical test structure

---

This framework provides a solid foundation for building scalable, maintainable test automation solutions with Playwright and Python.
