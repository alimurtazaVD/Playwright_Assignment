import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "home", task_name="automation_store")

    def navigate_to_home(self, base_url: str) -> None:
        self.page.locator(f"xpath={self.get_locator('home_link')}").click()
        self.wait_for_load_state()

    def click_dove_brand(self) -> None:
        self.page.locator(f"xpath={self.get_locator('dove_brand_link')}").click()
        self.wait_for_load_state()


