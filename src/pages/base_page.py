"""
Base Page Class for Playwright Test Framework
Provides common functionality for all page objects
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.sync_api import Page, Locator
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page, page_name: str, task_name: str = None):
        self.page = page
        self.page_name = page_name
        self.task_name = task_name
        self.locators = self._load_locators()
        self.base_url = None
    
    def _load_locators(self) -> Dict[str, Any]:
        """Load locators from YAML file with task-specific path support"""
        try:
            # If task_name is provided, use task-specific folder structure
            if self.task_name:
                locator_file = Path(f"locators/{self.task_name}/{self.page_name}.yaml")
            else:
                # Fallback to old structure for backward compatibility
                locator_file = Path(f"locators/{self.page_name}.yaml")
            
            if not locator_file.exists():
                logger.warning(f"Locator file not found: {locator_file}")
                return {}
            
            with open(locator_file, 'r', encoding='utf-8') as file:
                locators = yaml.safe_load(file)
            
            return locators.get(self.page_name, {})
            
        except Exception as e:
            logger.error(f"Failed to load locators for {self.page_name}: {e}")
            return {}
    
    def get_locator(self, key: str) -> str:
        """Get a locator by key"""
        locator = self.locators.get(key)
        if not locator:
            raise KeyError(f"Locator '{key}' not found in {self.page_name}")
        return locator
    
    def find_element(self, key: str) -> Locator:
        """Find an element using a locator key"""
        locator = self.get_locator(key)
        return self.page.locator(locator)
    
    def click(self, key: str) -> None:
        """Click an element using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Clicking element: {key}")
        element.click()
    
    def type_text(self, key: str, text: str) -> None:
        """Type text into an element using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Typing '{text}' into element: {key}")
        element.fill(text)
    
    def get_text(self, key: str) -> str:
        """Get text from an element using a locator key"""
        element = self.find_element(key)
        text = element.text_content()
        logger.debug(f"Got text '{text}' from element: {key}")
        return text or ""
    
    def is_visible(self, key: str) -> bool:
        """Check if an element is visible using a locator key"""
        element = self.find_element(key)
        return element.is_visible()
    
    def is_enabled(self, key: str) -> bool:
        """Check if an element is enabled using a locator key"""
        element = self.find_element(key)
        return element.is_enabled()
    
    def wait_for_element(self, key: str, timeout: int = 30000) -> None:
        """Wait for an element to be visible using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Waiting for element: {key}")
        element.wait_for(state="visible", timeout=timeout)
    
    def wait_for_element_hidden(self, key: str, timeout: int = 30000) -> None:
        """Wait for an element to be hidden using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Waiting for element to be hidden: {key}")
        element.wait_for(state="hidden", timeout=timeout)
    
    def get_attribute(self, key: str, attribute: str) -> Optional[str]:
        """Get an attribute value from an element using a locator key"""
        element = self.find_element(key)
        return element.get_attribute(attribute)
    
    def hover(self, key: str) -> None:
        """Hover over an element using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Hovering over element: {key}")
        element.hover()
    
    def select_option(self, key: str, value: str) -> None:
        """Select an option from a dropdown using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Selecting option '{value}' from element: {key}")
        element.select_option(value=value)
    
    def check(self, key: str) -> None:
        """Check a checkbox using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Checking element: {key}")
        element.check()
    
    def uncheck(self, key: str) -> None:
        """Uncheck a checkbox using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Unchecking element: {key}")
        element.uncheck()
    
    def is_checked(self, key: str) -> bool:
        """Check if a checkbox is checked using a locator key"""
        element = self.find_element(key)
        return element.is_checked()
    
    def take_screenshot(self, name: str = None) -> str:
        """Take a screenshot of the current page"""
        screenshot_name = name or f"{self.page_name}_{self.page.url.split('/')[-1]}"
        screenshot_path = f"artifacts/screenshots/{screenshot_name}.png"
        
        # Create directory if it doesn't exist
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def wait_for_url(self, url: str, timeout: int = 30000) -> None:
        """Wait for the page URL to match the expected URL"""
        logger.debug(f"Waiting for URL: {url}")
        self.page.wait_for_url(url, timeout=timeout)
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000) -> None:
        """Wait for the page to reach a specific load state"""
        logger.debug(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL"""
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_for_load_state()
    
    def refresh_page(self) -> None:
        """Refresh the current page"""
        logger.debug("Refreshing page")
        self.page.reload()
        self.wait_for_load_state()
    
    def go_back(self) -> None:
        """Go back to the previous page"""
        logger.debug("Going back to previous page")
        self.page.go_back()
        self.wait_for_load_state()
    
    def go_forward(self) -> None:
        """Go forward to the next page"""
        logger.debug("Going forward to next page")
        self.page.go_forward()
        self.wait_for_load_state()
    
    def get_page_title(self) -> str:
        """Get the page title"""
        return self.page.title()
    
    def get_page_url(self) -> str:
        """Get the current page URL"""
        return self.page.url
    
    def accept_dialog(self) -> None:
        """Accept any dialog that appears"""
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_dialog(self) -> None:
        """Dismiss any dialog that appears"""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    def wait_for_timeout(self, timeout: int) -> None:
        """Wait for a specific amount of time"""
        logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
    
    def scroll_to_element(self, key: str) -> None:
        """Scroll to an element using a locator key"""
        element = self.find_element(key)
        logger.debug(f"Scrolling to element: {key}")
        element.scroll_into_view_if_needed()
    
    def get_element_count(self, key: str) -> int:
        """Get the count of elements matching a locator key"""
        elements = self.page.locator(self.get_locator(key))
        return elements.count()
    
    def assert_element_visible(self, key: str, message: str = None) -> None:
        """Assert that an element is visible"""
        assert self.is_visible(key), message or f"Element {key} should be visible"
    
    def assert_element_not_visible(self, key: str, message: str = None) -> None:
        """Assert that an element is not visible"""
        assert not self.is_visible(key), message or f"Element {key} should not be visible"
    
    def assert_text_contains(self, key: str, expected_text: str, message: str = None) -> None:
        """Assert that element text contains expected text"""
        actual_text = self.get_text(key)
        assert expected_text in actual_text, message or f"Text '{expected_text}' not found in '{actual_text}'"
    
    def assert_text_equals(self, key: str, expected_text: str, message: str = None) -> None:
        """Assert that element text equals expected text"""
        actual_text = self.get_text(key)
        assert actual_text == expected_text, message or f"Expected '{expected_text}', got '{actual_text}'"
