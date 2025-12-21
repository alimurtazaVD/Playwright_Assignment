import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreCategoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "category", task_name="automation_store")

    def click_category(self, category_name: str) -> None:
        if category_name.lower() == "apparel & accessories":
            self.page.locator(self.get_locator("apparel_accessories")).click()
        elif category_name.lower() in ["tshirts", "t-shirts"]:
            self.page.locator(self.get_locator("tshirts")).click()
        elif category_name.lower() == "shoes":
            self.page.locator(self.get_locator("shoes")).click()
        self.wait_for_load_state()

