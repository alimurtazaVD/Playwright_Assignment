"""
Pytest Configuration and Fixtures for Playwright Test Framework
"""

import os
import pytest
import uuid
from datetime import datetime
from pathlib import Path
from typing import Generator
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import logging

from src.utils.config_manager import config_manager
from src.utils.logger import setup_logging, get_logger
from src.utils.db import initialize_database, get_db_manager

setup_logging()
logger = get_logger(__name__)


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "flaky: mark test as potentially flaky")

    # Configure reporter integration strictly from config.yaml
    reporting = config_manager.get_reporting_config()
    reporter = reporting.get("reporter", "html").lower()

    # Stash selected reporter for later hooks
    config._selected_reporter = reporter


# Note: Do not add --browser here to avoid conflicts with pytest-playwright plugin


@pytest.fixture(scope="session")
def browser_type() -> str:
    """Get the browser type strictly from config"""
    return config_manager.get_browser()


@pytest.fixture(scope="session")
def headless(request) -> bool:
    """Get headless setting from command line or config"""
    # Use config by default; users can run headed via config or modify here if needed
    return config_manager.get_headless()


@pytest.fixture(scope="session")
def playwright_instance():
    """Create and manage Playwright instance"""
    playwright = sync_playwright().start()
    logger.info("Playwright instance started")
    yield playwright
    playwright.stop()
    logger.info("Playwright instance stopped")


@pytest.fixture(scope="session")
def browser(playwright_instance, browser_type, headless) -> Generator[Browser, None, None]:
    """Create and manage browser instance"""
    browser_config = config_manager.get_browser_config(browser_type)

    channel = browser_config.get('channel')
    args = browser_config.get('args', [])

    if browser_type == "chromium":
        browser = playwright_instance.chromium.launch(
            headless=headless,
            channel=channel,
            args=args,
        )
    elif browser_type == "firefox":
        browser = playwright_instance.firefox.launch(
            headless=headless,
            args=args,
        )
    elif browser_type == "webkit":
        browser = playwright_instance.webkit.launch(
            headless=headless,
            args=args,
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")
    
    logger.info(f"Browser {browser_type} launched (headless: {headless}, channel: {channel or 'default'})")
    yield browser
    browser.close()
    logger.info(f"Browser {browser_type} closed")


@pytest.fixture(scope="function")
def browser_context(browser) -> Generator[BrowserContext, None, None]:
    """Create and manage browser context for each test"""
    viewport = config_manager.get_viewport()
    
    video_dir = "artifacts/videos" if config_manager.get_video() != "off" else None
    context = browser.new_context(
        viewport=viewport,
        record_video_dir=video_dir,
    )
    
    context.set_default_timeout(config_manager.get_timeout())
    
    logger.debug("Browser context created")
    yield context
    context.close()
    logger.debug("Browser context closed")


@pytest.fixture(scope="function")
def page(browser_context) -> Generator[Page, None, None]:
    """Create and manage page for each test"""
    page = browser_context.new_page()
    
    page.on("page", lambda page: logger.debug(f"New page opened: {page.url}"))
    page.on("console", lambda msg: logger.debug(f"Console: {msg.text}"))
    
    logger.debug("Page created")
    yield page
    page.close()
    logger.debug("Page closed")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get base URL from configuration"""
    return config_manager.get_base_url()


@pytest.fixture(scope="function")
def test_data() -> dict:
    """Get test data from configuration"""
    return config_manager.get_test_data()


@pytest.fixture(scope="function")
def run_id() -> str:
    """Generate unique run ID for each test run"""
    return str(uuid.uuid4())[:8]


@pytest.fixture(scope="function")
def artifacts_dir(run_id) -> Path:
    """Create and return artifacts directory for the test run"""
    artifacts_dir = Path(f"artifacts/{run_id}")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir


def pytest_runtest_setup(item):
    """Setup before each test"""
    test_name = item.name
    logger.info(f"Starting test: {test_name}")
    item.test_start_time = datetime.now()


def pytest_runtest_teardown(item, nextitem):
    """Teardown after each test"""
    test_name = item.name
    test_duration = datetime.now() - item.test_start_time
    logger.info(f"Test {test_name} completed in {test_duration.total_seconds():.2f}s")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot and trace/video on failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            # Screenshots
            screenshot_dir = Path("artifacts/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Saved screenshot: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Unable to capture screenshot: {e}")

            # Attach into Allure if selected
            try:
                reporter = getattr(item.config, "_selected_reporter", "html")
                if reporter == "allure":
                    import allure
                    with open(screenshot_path, "rb") as img:
                        allure.attach(img.read(), name=item.name, attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    logger.info("Setting up test environment")
    
    directories = [
        "artifacts",
        "artifacts/screenshots",
        "artifacts/videos",
        "artifacts/har",
        "logs",
        "reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Test environment setup completed")


# No CLI override for reporter; config.yaml is the single source of truth
@pytest.fixture(scope="session", autouse=True)
def initialize_db_from_config():
    """Initialize DB connection using config if present."""
    db_cfg = config_manager.get_db_config()
    if not db_cfg:
        return
    dsn = db_cfg.get("dsn")
    if not dsn:
        dialect = db_cfg.get("dialect", "mysql")
        driver = db_cfg.get("driver", "pymysql")
        username = db_cfg.get("username", "root")
        password = db_cfg.get("password", "")
        host = db_cfg.get("host", "127.0.0.1")
        port = db_cfg.get("port", 3306)
        database = db_cfg.get("database", "testdb")
        dsn = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"

    initialize_database(
        dsn=dsn,
        pool_size=db_cfg.get("pool_size", 5),
        max_overflow=db_cfg.get("max_overflow", 10),
        echo=False,
    )
    logger.info("Database initialized from configuration")


@pytest.fixture(scope="function")
def db():
    """Expose DatabaseManager to tests."""
    return get_db_manager()
