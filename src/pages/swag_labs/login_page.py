"""
Swag Labs Login Page Object
"""

from pathlib import Path
import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class SwagLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "swag_login", task_name="swag_labs")

    def open(self, base_url: str) -> None:
        self.navigate_to(base_url)
        self.wait_for_element("username_input")

    def login(self, username: str, password: str) -> None:
        self.type_text("username_input", username)
        self.type_text("password_input", password)
        self.click("login_button")

    def is_error_visible(self) -> bool:
        try:
            return self.is_visible("error_container")
        except Exception:
            return False

    def get_error_text(self) -> str:
        if self.is_error_visible():
            return self.get_text("error_container")
        return ""

