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

    def click_skincare(self) -> None:
        self.wait_for_load_state("networkidle", timeout=30000)
        base_url = self.page.url.split('/index.php')[0] if '/index.php' in self.page.url else self.page.url.rstrip('/')
        skincare_url = f"{base_url}/index.php?rt=product/category&path=43"
        self.page.goto(skincare_url)
        self.wait_for_load_state("networkidle", timeout=30000)

    def click_men(self) -> None:
        self.wait_for_load_state("networkidle", timeout=30000)
        base_url = self.page.url.split('/index.php')[0] if '/index.php' in self.page.url else self.page.url.rstrip('/')
        men_url = f"{base_url}/index.php?rt=product/category&path=58"
        self.page.goto(men_url)
        self.wait_for_load_state("networkidle", timeout=30000)

    def click_fragrance(self) -> None:
        self.wait_for_load_state("networkidle", timeout=30000)
        base_url = self.page.url.split('/index.php')[0] if '/index.php' in self.page.url else self.page.url.rstrip('/')
        fragrance_url = f"{base_url}/index.php?rt=product/category&path=49"
        self.page.goto(fragrance_url)
        self.wait_for_load_state("networkidle", timeout=30000)

