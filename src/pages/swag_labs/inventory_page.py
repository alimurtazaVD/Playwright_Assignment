"""
Swag Labs Inventory Page Object
"""

from typing import List
from playwright.sync_api import Page
from ..base_page import BasePage


class SwagInventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "swag_inventory", task_name="swag_labs")

    def is_loaded(self) -> bool:
        return "inventory.html" in self.page.url

    def get_title_text(self) -> str:
        # support both simple and nested locator format
        try:
            locator = self.get_locator("page_title")
            if isinstance(locator, dict) and "css" in locator:
                return self.page.locator(locator["css"]).text_content() or ""
            return self.page.locator(locator).text_content() or ""
        except Exception:
            return ""

    def open_cart(self) -> None:
        self.click("cart_icon")

    def sort_low_to_high(self) -> None:
        self.select_option("filter_dropdown", "lohi")

    def get_all_prices(self) -> List[float]:
        prices = self.page.locator(self.get_locator("item_price")).all_text_contents()
        normalized = []
        for p in prices:
            try:
                normalized.append(float(p.replace("$", "").strip()))
            except Exception:
                pass
        return normalized

    def add_lowest_n_items(self, n: int = 2) -> List[float]:
        items = self.page.locator(self.get_locator("item_card"))
        count = items.count()
        price_locator = self.get_locator("item_price")
        button_locator = self.get_locator("add_to_cart_button")
        pairs = []
        for i in range(count):
            price_text = items.nth(i).locator(price_locator).text_content()
            price_val = float(price_text.replace("$", "").strip())
            pairs.append((price_val, i))
        pairs.sort(key=lambda x: x[0])
        selected = pairs[:n]
        for _, idx in selected:
            items.nth(idx).locator(button_locator).click()
        return [p for p, _ in selected]

    def open_menu(self) -> None:
        self.click("menu_button")

    def click_about(self) -> None:
        self.click("about_link")

