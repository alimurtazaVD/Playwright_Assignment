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


def pytest_addoption(parser):
    parser.addoption(
        "--browsers",
        action="store",
        default=None,
        help="Comma-separated list of browsers to use for cross-browser tests (e.g., chromium,firefox,webkit). Overrides browsers specified in @pytest.mark.cross_browser marker."
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "flaky: mark test as potentially flaky")
    config.addinivalue_line("markers", "cross_browser: mark test to run on multiple browsers in parallel")

    reporting = config_manager.get_reporting_config()
    reporter = reporting.get("reporter", "html").lower()
    config._selected_reporter = reporter
    
    browsers_option = config.getoption("--browsers")
    if browsers_option:
        config._cross_browser_browsers_override = [b.strip() for b in browsers_option.split(",")]
    else:
        config._cross_browser_browsers_override = None


def pytest_generate_tests(metafunc):
    cross_browser_marker = metafunc.definition.get_closest_marker("cross_browser")
    if cross_browser_marker:
        config = metafunc.config
        if hasattr(config, "_cross_browser_browsers_override") and config._cross_browser_browsers_override:
            browsers = config._cross_browser_browsers_override
        else:
            browsers = cross_browser_marker.kwargs.get("browsers", ["chromium", "firefox", "webkit"])
        
        if "cross_browser_browser" in metafunc.fixturenames:
            metafunc.parametrize("cross_browser_browser", browsers, scope="function", indirect=True)
        elif "browser_name" in metafunc.fixturenames:
            already_parametrized = any(
                marker.args[0] == "browser_name" 
                for marker in metafunc.definition.iter_markers("parametrize")
                if marker.args and len(marker.args) > 0
            )
            if not already_parametrized:
                metafunc.parametrize("browser_name", browsers, scope="function", indirect=True)


@pytest.fixture(scope="session")
def browser_type(request) -> str:
    if hasattr(request, "param"):
        return request.param
    return config_manager.get_browser()


@pytest.fixture(scope="session")
def headless(request) -> bool:
    return config_manager.get_headless()


@pytest.fixture(scope="session")
def playwright_instance():
    playwright = sync_playwright().start()
    logger.info("Playwright instance started")
    yield playwright
    playwright.stop()
    logger.info("Playwright instance stopped")


@pytest.fixture(scope="session")
def browser(playwright_instance, browser_type, headless) -> Generator[Browser, None, None]:
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
    viewport = config_manager.get_viewport()
    video_dir = "artifacts/videos" if config_manager.get_video() != "off" else None
    context = browser.new_context(
        viewport=viewport,
        record_video_dir=video_dir,
    )
    context.set_default_timeout(config_manager.get_timeout())
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context, request) -> Generator[Page, None, None]:
    page = browser_context.new_page()
    page.on("page", lambda page: logger.debug(f"New page opened: {page.url}"))
    page.on("console", lambda msg: logger.debug(f"Console: {msg.text}"))
    browser_name = getattr(request, "param", None) if hasattr(request, "param") else None
    if browser_name:
        logger.info(f"Running test on browser: {browser_name}")
    yield page
    page.close()


@pytest.fixture(scope="function")
def browser_name(request):
    if hasattr(request, "param") and request.param is not None:
        return request.param
    return config_manager.get_browser()


@pytest.fixture(scope="function")
def cross_browser_browser(request, playwright_instance, headless) -> Generator[Browser, None, None]:
    if hasattr(request, "param"):
        browser_name = request.param
    else:
        try:
            browser_name = request.getfixturevalue("browser_name")
        except:
            browser_name = config_manager.get_browser()
    
    browser_config = config_manager.get_browser_config(browser_name)
    
    channel = browser_config.get('channel')
    args = browser_config.get('args', [])
    
    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(
            headless=headless,
            channel=channel,
            args=args,
        )
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(
            headless=headless,
            args=args,
        )
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(
            headless=headless,
            args=args,
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    logger.info(f"Cross-browser test: Browser {browser_name} launched (headless: {headless})")
    yield browser
    browser.close()
    logger.info(f"Cross-browser test: Browser {browser_name} closed")


@pytest.fixture(scope="function")
def cross_browser_context(cross_browser_browser) -> Generator[BrowserContext, None, None]:
    browser_name = getattr(cross_browser_browser, "_browser_name", "unknown")
    viewport = config_manager.get_viewport()
    video_dir = "artifacts/videos" if config_manager.get_video() != "off" else None
    
    context = cross_browser_browser.new_context(
        viewport=viewport,
        record_video_dir=video_dir,
    )
    context._browser_name = browser_name
    context.set_default_timeout(config_manager.get_timeout())
    yield context
    context.close()


@pytest.fixture(scope="function")
def cross_browser_page(cross_browser_context) -> Generator[Page, None, None]:
    browser_name = getattr(cross_browser_context, "_browser_name", "unknown")
    page = cross_browser_context.new_page()
    logger.info(f"Cross-browser test page created for browser: {browser_name}")
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return config_manager.get_base_url()


@pytest.fixture(scope="function")
def test_data() -> dict:
    return config_manager.get_test_data()


@pytest.fixture(scope="function")
def run_id() -> str:
    return str(uuid.uuid4())[:8]


@pytest.fixture(scope="function")
def artifacts_dir(run_id) -> Path:
    artifacts_dir = Path(f"artifacts/{run_id}")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir


def pytest_runtest_setup(item):
    test_name = item.name
    logger.info(f"Starting test: {test_name}")
    item.test_start_time = datetime.now()


def pytest_runtest_teardown(item, nextitem):
    test_name = item.name
    test_duration = datetime.now() - item.test_start_time
    logger.info(f"Test {test_name} completed in {test_duration.total_seconds():.2f}s")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            screenshot_dir = Path("artifacts/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Saved screenshot: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Unable to capture screenshot: {e}")

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


@pytest.fixture(scope="session", autouse=True)
def initialize_db_from_config():
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
    return get_db_manager()
