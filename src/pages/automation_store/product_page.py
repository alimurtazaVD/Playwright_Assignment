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
        self.page.wait_for_timeout(2000)
        
        product_containers = self.page.locator("div.thumbnail")
        if product_containers.count() == 0:
            product_containers = self.page.locator(f"xpath={self.get_locator('product_items')}")
        
        product_container = product_containers.first
        product_container.wait_for(state="visible", timeout=20000)
        
        name_element = product_container.locator("h4 a").first
        if name_element.count() == 0:
            name_element = product_container.locator("xpath=.//a[@title]").first
        if name_element.count() == 0:
            name_xpath = self.get_locator("product_name")
            name_element = product_container.locator(f"xpath={name_xpath}")
        
        product_name = ""
        if name_element.count() > 0:
            product_name = name_element.get_attribute("title") or ""
            if not product_name or product_name == "Add to Cart":
                product_name = name_element.text_content().strip()
                if product_name == "Add to Cart":
                    all_links = product_container.locator("a")
                    for i in range(all_links.count()):
                        link = all_links.nth(i)
                        link_text = link.text_content().strip()
                        link_title = link.get_attribute("title") or ""
                        if link_title and link_title != "Add to Cart":
                            product_name = link_title
                            break
                        elif link_text and link_text != "Add to Cart" and len(link_text) > 5:
                            product_name = link_text
                            break
        
        price_element = product_container.locator(".pricetag .oneprice").first
        if price_element.count() == 0:
            price_xpath = self.get_locator("product_price")
            price_element = product_container.locator(f"xpath={price_xpath}")
        
        product_price = price_element.text_content().strip() if price_element.count() > 0 else ""
        
        return {"name": product_name, "price": product_price}

    def click_newest_product(self) -> None:
        self.sort_by_newest()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        product_containers = self.page.locator("div.thumbnail")
        if product_containers.count() == 0:
            product_containers = self.page.locator(f"xpath={self.get_locator('product_items')}")
        
        product_count = product_containers.count()
        if product_count == 0:
            raise Exception("No products found on page")
        
        product_container = product_containers.first
        product_container.wait_for(state="visible", timeout=20000)
        
        product_link = product_container.locator("xpath=.//a[@title]").first
        if product_link.count() == 0:
            product_link = product_container.locator("h4 a").first
        if product_link.count() == 0:
            name_xpath = self.get_locator("product_name")
            product_link = product_container.locator(f"xpath={name_xpath}")
        
        if product_link.count() == 0:
            raise Exception("Product link not found")
        
        product_link.scroll_into_view_if_needed()
        product_link.click(timeout=30000)
        self.wait_for_load_state("load", timeout=20000)
        self.page.wait_for_timeout(1000)

    def add_to_cart(self) -> None:
        self.wait_for_load_state("networkidle")
        add_to_cart = self.page.locator(f"xpath={self.get_locator('add_to_cart_button')}").first
        add_to_cart.click()
        self.wait_for_load_state("networkidle")


