import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.sync_api import Page, Locator
import logging

logger = logging.getLogger(__name__)


class BasePage:
    
    def __init__(self, page: Page, page_name: str, task_name: str = None):
        self.page = page
        self.page_name = page_name
        self.task_name = task_name
        self.locators = self._load_locators()
        self.base_url = None
    
    def _load_locators(self) -> Dict[str, Any]:
        try:
            if self.task_name:
                locator_file = Path(f"locators/{self.task_name}/{self.page_name}.yaml")
            else:
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
        locator = self.locators.get(key)
        if not locator:
            raise KeyError(f"Locator '{key}' not found in {self.page_name}")
        return locator
    
    def find_element(self, key: str) -> Locator:
        locator = self.get_locator(key)
        return self.page.locator(locator)
    
    def click(self, key: str) -> None:
        element = self.find_element(key)
        element.click()
    
    def type_text(self, key: str, text: str) -> None:
        element = self.find_element(key)
        element.fill(text)
    
    def get_text(self, key: str) -> str:
        element = self.find_element(key)
        text = element.text_content()
        return text or ""
    
    def is_visible(self, key: str) -> bool:
        element = self.find_element(key)
        return element.is_visible()
    
    def is_enabled(self, key: str) -> bool:
        element = self.find_element(key)
        return element.is_enabled()
    
    def wait_for_element(self, key: str, timeout: int = 30000) -> None:
        element = self.find_element(key)
        element.wait_for(state="visible", timeout=timeout)
    
    def wait_for_element_hidden(self, key: str, timeout: int = 30000) -> None:
        element = self.find_element(key)
        element.wait_for(state="hidden", timeout=timeout)
    
    def get_attribute(self, key: str, attribute: str) -> Optional[str]:
        element = self.find_element(key)
        return element.get_attribute(attribute)
    
    def hover(self, key: str) -> None:
        element = self.find_element(key)
        element.hover()
    
    def select_option(self, key: str, value: str) -> None:
        element = self.find_element(key)
        element.select_option(value=value)
    
    def check(self, key: str) -> None:
        element = self.find_element(key)
        element.check()
    
    def uncheck(self, key: str) -> None:
        element = self.find_element(key)
        element.uncheck()
    
    def is_checked(self, key: str) -> bool:
        element = self.find_element(key)
        return element.is_checked()
    
    def take_screenshot(self, name: str = None) -> str:
        screenshot_name = name or f"{self.page_name}_{self.page.url.split('/')[-1]}"
        screenshot_path = f"artifacts/screenshots/{screenshot_name}.png"
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=screenshot_path)
        return screenshot_path
    
    def wait_for_url(self, url: str, timeout: int = 30000) -> None:
        self.page.wait_for_url(url, timeout=timeout)
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000) -> None:
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def navigate_to(self, url: str) -> None:
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_for_load_state()
    
    def refresh_page(self) -> None:
        self.page.reload()
        self.wait_for_load_state()
    
    def go_back(self) -> None:
        self.page.go_back()
        self.wait_for_load_state()
    
    def go_forward(self) -> None:
        self.page.go_forward()
        self.wait_for_load_state()
    
    def get_page_title(self) -> str:
        return self.page.title()
    
    def get_page_url(self) -> str:
        return self.page.url
    
    def accept_dialog(self) -> None:
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_dialog(self) -> None:
        self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    def wait_for_timeout(self, timeout: int) -> None:
        self.page.wait_for_timeout(timeout)
    
    def scroll_to_element(self, key: str) -> None:
        element = self.find_element(key)
        element.scroll_into_view_if_needed()
    
    def get_element_count(self, key: str) -> int:
        elements = self.page.locator(self.get_locator(key))
        return elements.count()
    
    def assert_element_visible(self, key: str, message: str = None) -> None:
        assert self.is_visible(key), message or f"Element {key} should be visible"
    
    def assert_element_not_visible(self, key: str, message: str = None) -> None:
        assert not self.is_visible(key), message or f"Element {key} should not be visible"
    
    def assert_text_contains(self, key: str, expected_text: str, message: str = None) -> None:
        actual_text = self.get_text(key)
        assert expected_text in actual_text, message or f"Text '{expected_text}' not found in '{actual_text}'"
    
    def assert_text_equals(self, key: str, expected_text: str, message: str = None) -> None:
        actual_text = self.get_text(key)
        assert actual_text == expected_text, message or f"Expected '{expected_text}', got '{actual_text}'"
