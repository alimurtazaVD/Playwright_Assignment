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
        quantity_input.wait_for(state="visible", timeout=10000)
        quantity_input.clear()
        quantity_input.fill(str(quantity))
        self.page.wait_for_timeout(500)
        
        current_value = quantity_input.input_value()
        if current_value != str(quantity):
            quantity_input.fill(str(quantity))
            self.page.wait_for_timeout(500)

    def add_to_cart(self) -> None:
        self.wait_for_load_state("load")
        self.page.wait_for_timeout(1000)
        
        add_to_cart_link = self.page.get_by_role("link", name="Add to Cart", exact=False).first
        if add_to_cart_link.count() == 0:
            add_to_cart_link = self.page.locator("a:has-text('Add to Cart')").first
        if add_to_cart_link.count() == 0:
            locator = self.get_locator("add_to_cart_link")
            if locator.startswith("//"):
                add_to_cart_link = self.page.locator(f"xpath={locator}").first
            else:
                add_to_cart_link = self.page.locator(locator).first
        
        if add_to_cart_link.count() > 0:
            add_to_cart_link.scroll_into_view_if_needed()
            add_to_cart_link.wait_for(state="visible", timeout=30000)
            add_to_cart_link.click(timeout=30000)
            self.page.wait_for_timeout(2000)
            logger.info("Product added to cart successfully")
        else:
            logger.warning("Add to Cart button not found")

