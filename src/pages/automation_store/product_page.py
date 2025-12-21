import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "product", task_name="automation_store")

    def sort_by_newest(self) -> None:
        self.page.locator(f"xpath={self.get_locator('sort_dropdown')}").select_option("date_modified-DESC")
        self.wait_for_load_state()
        current_url = self.page.url
        if "manufacturer_id" in current_url:
            manufacturer_id = self._extract_manufacturer_id(current_url)
            base_url = current_url.split("?")[0] if "?" in current_url else current_url.rstrip("/")
            sorted_url = f"{base_url}?rt=product/manufacturer&manufacturer_id={manufacturer_id}&sort=date_modified-DESC&limit=20"
            self.page.goto(sorted_url)
            self.wait_for_load_state("networkidle")

    def _extract_manufacturer_id(self, url: str) -> str:
        if "manufacturer_id=" in url:
            return url.split("manufacturer_id=")[1].split("&")[0]
        return "18"

    def get_newest_product(self) -> dict:
        self.sort_by_newest()
        self.page.wait_for_load_state("networkidle")
        
        product_container = self.page.locator(f"xpath={self.get_locator('product_items')}").first
        name_xpath = self.get_locator("product_name")
        name_element = product_container.locator(f"xpath={name_xpath}")
        product_name = name_element.get_attribute("title") or name_element.text_content().strip() if name_element.count() > 0 else ""
        
        price_xpath = self.get_locator("product_price")
        price_element = product_container.locator(f"xpath={price_xpath}")
        product_price = price_element.text_content().strip() if price_element.count() > 0 else ""
        
        return {"name": product_name, "price": product_price}

    def click_newest_product(self) -> None:
        self.sort_by_newest()
        self.page.wait_for_load_state("networkidle")
        
        product_container = self.page.locator(f"xpath={self.get_locator('product_items')}").first
        name_xpath = self.get_locator("product_name")
        product_link = product_container.locator(f"xpath={name_xpath}")
        product_link.click()
        self.wait_for_load_state()

    def add_to_cart(self) -> None:
        self.wait_for_load_state("networkidle")
        add_to_cart = self.page.locator(f"xpath={self.get_locator('add_to_cart_button')}").first
        add_to_cart.click()
        self.wait_for_load_state("networkidle")


