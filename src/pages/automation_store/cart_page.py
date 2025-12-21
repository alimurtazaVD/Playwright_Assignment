import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreCartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "cart", task_name="automation_store")

    def navigate_to_cart(self) -> None:
        self.page.locator("#cart_checkout1").click()
        self.wait_for_load_state("networkidle")

    def get_cart_items(self) -> list:
        items = []
        cart_items_xpath = self.get_locator("cart_items")
        cart_items = self.page.locator(f"xpath={cart_items_xpath}")
        count = cart_items.count()
        
        for i in range(count):
            item = cart_items.nth(i)
            name_xpath = self.get_locator("item_name")
            name_element = item.locator(f"xpath={name_xpath}")
            name = name_element.text_content().strip() if name_element.count() > 0 else ""
            
            quantity_xpath = self.get_locator("item_quantity")
            quantity_element = item.locator(f"xpath={quantity_xpath}")
            quantity = quantity_element.get_attribute("value") or "1"
            
            price_xpath = self.get_locator("item_price")
            price_element = item.locator(f"xpath={price_xpath}")
            price = price_element.text_content().strip() if price_element.count() > 0 else ""
            
            items.append({
                "name": name,
                "quantity": int(quantity) if quantity.isdigit() else 1,
                "price": price
            })
        
        return items

    def get_item_count(self) -> int:
        cart_items_xpath = self.get_locator("cart_items")
        return self.page.locator(f"xpath={cart_items_xpath}").count()

    def verify_item_in_cart(self, expected_name: str, expected_quantity: int = 1) -> dict:
        items = self.get_cart_items()
        
        for item in items:
            if expected_name.lower() in item["name"].lower():
                return item
        
        return {}

    def verify_all_items_in_cart(self, expected_items: list) -> bool:
        items = self.get_cart_items()
        found_count = 0
        
        for expected_item in expected_items:
            expected_name = expected_item.get("name", "")
            expected_quantity = expected_item.get("quantity", 1)
            
            for cart_item in items:
                if expected_name.lower() in cart_item["name"].lower():
                    if cart_item["quantity"] == expected_quantity:
                        found_count += 1
                        break
        
        return found_count == len(expected_items)

    def get_total_item_count(self) -> int:
        items = self.get_cart_items()
        return sum(item["quantity"] for item in items)

