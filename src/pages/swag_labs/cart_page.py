"""
Swag Labs Cart Page Object
"""

from typing import List
from playwright.sync_api import Page
from ..base_page import BasePage


class SwagCartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "swag_cart", task_name="swag_labs")

    def get_item_prices(self) -> List[float]:
        prices = self.page.locator(self.get_locator("cart_item_price")).all_text_contents()
        return [float(p.replace("$", "").strip()) for p in prices]

    def get_quantities(self) -> List[int]:
        qtys = self.page.locator(self.get_locator("cart_quantity")).all_text_contents()
        return [int(q.strip()) for q in qtys]

    def get_item_count(self) -> int:
        return self.page.locator(self.get_locator("cart_item")).count()

