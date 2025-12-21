import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreProductDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "product_detail", task_name="automation_store")

    def select_size(self, size: str) -> None:
        size_mapping = {
            "small": "Small",
            "medium": "Medium",
            "large": "Large"
        }
        size_value = size_mapping.get(size.lower(), size)
        size_dropdown = self.page.locator(self.get_locator("size_dropdown")).first
        size_dropdown.select_option(label=size_value)
        self.wait_for_load_state()

    def set_quantity(self, quantity: int) -> None:
        quantity_input = self.page.locator(self.get_locator("quantity_input")).first
        quantity_input.fill(str(quantity))

    def add_to_cart(self) -> None:
        self.wait_for_load_state("networkidle")
        add_to_cart_link = self.page.locator(self.get_locator("add_to_cart_link")).first
        add_to_cart_link.click()
        self.wait_for_load_state("networkidle")

