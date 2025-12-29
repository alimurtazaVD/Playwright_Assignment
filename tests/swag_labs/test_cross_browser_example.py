"""
Example Cross-Browser Test
This demonstrates how to run tests across multiple browsers in parallel
"""

import pytest
import logging
from src.pages.swag_labs.login_page import SwagLoginPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)


@pytest.mark.cross_browser
@pytest.mark.smoke
def test_login_cross_browser(cross_browser_page, base_url):
    """Example cross-browser test - runs on chromium, firefox, and webkit in parallel"""
    # Get browser_name from the page's context (stored during fixture creation)
    browser_name = getattr(cross_browser_page.context, '_browser_name', 'unknown')
    logger.info(f"Running login test on browser: {browser_name}")
    
    login = SwagLoginPage(cross_browser_page)
    login.open(base_url)
    
    creds = config_manager.get_test_data()["users"]
    login.login(
        creds["standard_user"]["username"],
        creds["standard_user"]["password"]
    )
    
    cross_browser_page.wait_for_url("**/inventory.html")
    assert "inventory.html" in cross_browser_page.url, f"Login failed on {browser_name}"
    
    logger.info(f"Login test passed on {browser_name}")


@pytest.mark.cross_browser(browsers=["chromium", "firefox"])
@pytest.mark.regression
def test_login_specific_browsers(cross_browser_page, base_url):
    """Example cross-browser test - runs only on chromium and firefox"""
    browser_name = getattr(cross_browser_page.context, '_browser_name', 'unknown')
    logger.info(f"Running login test on browser: {browser_name}")
    
    login = SwagLoginPage(cross_browser_page)
    login.open(base_url)
    
    creds = config_manager.get_test_data()["users"]
    login.login(
        creds["standard_user"]["username"],
        creds["standard_user"]["password"]
    )
    
    cross_browser_page.wait_for_url("**/inventory.html")
    assert "inventory.html" in cross_browser_page.url, f"Login failed on {browser_name}"
    
    logger.info(f"Login test passed on {browser_name}")

