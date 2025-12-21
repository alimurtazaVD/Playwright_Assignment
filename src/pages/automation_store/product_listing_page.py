import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreProductListingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "product_listing", task_name="automation_store")

    def sort_by_price_low_to_high(self) -> None:
        self.page.locator(self.get_locator("sort_dropdown")).select_option("p.price-ASC")
        self.wait_for_load_state("networkidle")

    def sort_by_price_high_to_low(self) -> None:
        self.page.locator(self.get_locator("sort_dropdown")).select_option("p.price-DESC")
        self.wait_for_load_state("networkidle")

    def get_products_by_price_order(self, count: int, ascending: bool = True) -> list:
        products = []
        product_items = self.page.locator(self.get_locator("product_items"))
        item_count = product_items.count()
        
        for i in range(min(count, item_count)):
            product = product_items.nth(i)
            name_element = product.locator(self.get_locator("product_name"))
            name = name_element.get_attribute("title") or name_element.text_content().strip()
            
            price_element = product.locator(self.get_locator("product_price"))
            price_text = price_element.text_content().strip() if price_element.count() > 0 else ""
            
            products.append({
                "name": name,
                "price": price_text,
                "index": i
            })
        
        return products

    def click_product_by_index(self, index: int) -> None:
        product_items = self.page.locator(self.get_locator("product_items"))
        product = product_items.nth(index)
        product_link = product.locator(self.get_locator("product_link"))
        product_link.click()
        self.wait_for_load_state()

