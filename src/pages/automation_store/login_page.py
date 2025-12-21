import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "login", task_name="automation_store")

    def open(self, base_url: str) -> None:
        self.navigate_to(base_url)
        self.wait_for_load_state()

    def click_login_link(self) -> None:
        self.page.locator(f"xpath={self.get_locator('login_link')}").click()
        self.wait_for_load_state()

    def login(self, username: str, password: str) -> None:
        self.page.locator(f"xpath={self.get_locator('username_input')}").fill(username)
        self.page.locator(f"xpath={self.get_locator('password_input')}").fill(password)
        self.page.locator(f"xpath={self.get_locator('login_button')}").click()
        self.wait_for_load_state()

