import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreProductListingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "product_listing", task_name="automation_store")

    def sort_by_price_low_to_high(self) -> None:
        sort_dropdown = self.page.locator(self.get_locator("sort_dropdown"))
        sort_dropdown.wait_for(state="visible", timeout=30000)
        sort_dropdown.select_option("p.price-ASC")
        self.wait_for_load_state("load", timeout=20000)
        self.page.wait_for_timeout(2000)

    def sort_by_price_high_to_low(self) -> None:
        sort_dropdown = self.page.locator(self.get_locator("sort_dropdown"))
        sort_dropdown.wait_for(state="visible", timeout=30000)
        sort_dropdown.select_option("p.price-DESC")
        self.wait_for_load_state("load", timeout=20000)
        self.page.wait_for_timeout(2000)

    def get_products_by_name_starting_with(self, starting_letter: str) -> list:
        self.wait_for_load_state("load")
        self.page.wait_for_timeout(2000)
        
        products = []
        product_items = self.page.locator("div.thumbnail")
        if product_items.count() == 0:
            product_items = self.page.locator(self.get_locator("product_items"))
        
        item_count = product_items.count()
        
        for i in range(item_count):
            try:
                product = product_items.nth(i)
                try:
                    product.wait_for(state="visible", timeout=5000)
                except:
                    self.page.wait_for_timeout(1000)
                    continue
                
                name = ""
                name_element = product.locator("h4 a").first
                if name_element.count() > 0:
                    name = name_element.get_attribute("title") or name_element.text_content().strip()
                
                if not name or name in ["Add to Cart", "Write Review", ""]:
                    product_link = product.locator("xpath=.//a[contains(@href, 'product/product')]").first
                    if product_link.count() > 0:
                        name = product_link.get_attribute("title") or product_link.text_content().strip()
                
                if not name or name in ["Add to Cart", "Write Review", ""]:
                    all_links = product.locator("a")
                    for j in range(all_links.count()):
                        link = all_links.nth(j)
                        href = link.get_attribute("href") or ""
                        if "product/product" in href:
                            link_title = link.get_attribute("title") or ""
                            link_text = link.text_content().strip()
                            if link_title and link_title not in ["Add to Cart", "Write Review"] and len(link_title) > 5:
                                name = link_title
                                break
                            elif link_text and link_text not in ["Add to Cart", "Write Review"] and len(link_text) > 5:
                                name = link_text
                                break
                
                if not name or name in ["Add to Cart", "Write Review", ""]:
                    product_text = product.text_content() or ""
                    import re
                    lines = product_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 5 and line not in ["Add to Cart", "Write Review", "View"] and not line.startswith('$') and not re.match(r'^\d+$', line) and not line.startswith('View'):
                            if any(char.isalpha() for char in line):
                                name = line
                                break
                
                if name and name.strip().upper().startswith(starting_letter.upper()):
                    price_element = product.locator(".oneprice").first
                    if price_element.count() == 0:
                        price_element = product.locator(self.get_locator("product_price")).first
                    
                    price_text = price_element.text_content().strip() if price_element.count() > 0 else ""
                    
                    products.append({
                        "name": name,
                        "price": price_text,
                        "index": i
                    })
            except Exception as e:
                logger.warning(f"Error processing product {i}: {e}")
                continue
        
        return products

    def get_products_by_price_order(self, count: int, ascending: bool = True) -> list:
        self.wait_for_load_state("load")
        self.page.wait_for_timeout(2000)
        
        products = []
        product_items = self.page.locator("div.thumbnail")
        if product_items.count() == 0:
            product_items = self.page.locator(self.get_locator("product_items"))
        
        item_count = product_items.count()
        
        for i in range(min(count, item_count)):
            product = product_items.nth(i)
            product.wait_for(state="visible", timeout=10000)
            
            name = ""
            product_link = product.locator("xpath=.//a[contains(@href, 'product/product')]").first
            if product_link.count() > 0:
                name = product_link.get_attribute("title") or product_link.text_content().strip()
            
            if not name or name in ["Add to Cart", "Write Review"]:
                name_element = product.locator("h4 a").first
                if name_element.count() > 0:
                    href = name_element.get_attribute("href") or ""
                    if "product/product" in href:
                        name = name_element.get_attribute("title") or name_element.text_content().strip()
            
            if not name or name in ["Add to Cart", "Write Review"]:
                all_links = product.locator("a")
                for j in range(all_links.count()):
                    link = all_links.nth(j)
                    href = link.get_attribute("href") or ""
                    if "product/product" in href:
                        link_title = link.get_attribute("title") or ""
                        link_text = link.text_content().strip()
                        if link_title and link_title not in ["Add to Cart", "Write Review"] and len(link_title) > 5:
                            name = link_title
                            break
                        elif link_text and link_text not in ["Add to Cart", "Write Review"] and len(link_text) > 5:
                            name = link_text
                            break
            
            if not name or name in ["Add to Cart", "Write Review"]:
                product_text = product.text_content() or ""
                import re
                lines = product_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 5 and line not in ["Add to Cart", "Write Review", "Out of Stock"] and not line.startswith('$') and not re.match(r'^\d+$', line):
                        name = line
                        break
            
            price_element = product.locator(".oneprice").first
            if price_element.count() == 0:
                price_element = product.locator(self.get_locator("product_price")).first
            
            price_text = price_element.text_content().strip() if price_element.count() > 0 else ""
            
            if name and name not in ["Add to Cart", "Write Review", "Out of Stock"]:
                products.append({
                    "name": name,
                    "price": price_text,
                    "index": i
                })
            else:
                logger.warning(f"Could not extract valid product name for product at index {i}. Name found: '{name}'")
        
        return products

    def wait_for_listing_page_ready(self) -> None:
        self.wait_for_load_state("load", timeout=20000)
        self.page.wait_for_timeout(2000)
        
        product_items = self.page.locator("div.thumbnail")
        if product_items.count() == 0:
            product_items = self.page.locator(self.get_locator("product_items"))
        
        if product_items.count() > 0:
            product_items.first.wait_for(state="visible", timeout=30000)
            self.page.wait_for_timeout(1000)
        else:
            sort_dropdown = self.page.locator(self.get_locator("sort_dropdown"))
            try:
                sort_dropdown.wait_for(state="visible", timeout=10000)
            except:
                pass
            self.page.wait_for_timeout(2000)
            product_items = self.page.locator("div.thumbnail")
            if product_items.count() == 0:
                product_items = self.page.locator(self.get_locator("product_items"))
            if product_items.count() > 0:
                product_items.first.wait_for(state="visible", timeout=20000)

    def click_product_by_index(self, index: int) -> None:
        self.wait_for_listing_page_ready()
        
        product_items = self.page.locator("div.thumbnail")
        if product_items.count() == 0:
            product_items = self.page.locator(self.get_locator("product_items"))
        
        item_count = product_items.count()
        if item_count == 0:
            raise Exception(f"No products found on page")
        if index >= item_count:
            raise Exception(f"Product index {index} out of range (total: {item_count})")
        
        product = product_items.nth(index)
        
        try:
            product.wait_for(state="visible", timeout=20000)
        except:
            self.page.wait_for_timeout(2000)
            product.wait_for(state="visible", timeout=20000)
        
        product_link = product.locator("xpath=.//a[@title]").first
        if product_link.count() == 0:
            product_link = product.locator("h4 a").first
        if product_link.count() == 0:
            product_link = product.locator("a.prdocutname").first
        if product_link.count() == 0:
            product_link = product.locator("xpath=.//a[contains(@href, 'product/product')]").first
        if product_link.count() == 0:
            locator = self.get_locator("product_link")
            if locator.startswith("//") or locator.startswith(".//"):
                product_link = product.locator(f"xpath={locator}").first
            else:
                product_link = product.locator(locator).first
        
        if product_link.count() == 0:
            raise Exception(f"Product link not found at index {index}")
        
        product_link.scroll_into_view_if_needed()
        product_link.click(timeout=30000)
        self.page.wait_for_timeout(2000)
        
        try:
            self.page.wait_for_url("**/product/product**", timeout=15000)
        except:
            pass

    def count_sale_items(self) -> int:
        self.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        
        sale_items = self.page.locator("div.thumbnail:has(span.sale)")
        sale_count = sale_items.count()
        logger.info(f"Found {sale_count} sale items using span.sale class")
        
        if sale_count == 0:
            sale_badges = self.page.locator("span.sale")
            sale_count = sale_badges.count()
            logger.info(f"Found {sale_count} sale badges using span.sale")
        
        logger.info(f"Total sale items found: {sale_count}")
        return sale_count

    def count_sale_and_out_of_stock_items(self) -> int:
        self.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        all_products = self.page.locator("div.thumbnail")
        total_count = all_products.count()
        sale_out_of_stock_count = 0
        
        for i in range(total_count):
            product = all_products.nth(i)
            
            try:
                sale_badge = product.locator("span.sale")
                out_of_stock = product.locator("xpath=.//span[contains(text(), 'Out of Stock')]")
                
                if sale_badge.count() > 0 and out_of_stock.count() > 0:
                    sale_out_of_stock_count += 1
            except Exception as e:
                logger.warning(f"Error checking product {i} for sale and out of stock: {e}")
                continue
        
        return sale_out_of_stock_count

    def get_sale_items(self) -> list:
        self.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        
        sale_items = []
        sale_product_containers = self.page.locator("div.thumbnail:has(span.sale)")
        total_count = sale_product_containers.count()
        
        if total_count == 0:
            all_products = self.page.locator("div.thumbnail")
            total_products = all_products.count()
            
            for i in range(total_products):
                product = all_products.nth(i)
                sale_badge = product.locator("span.sale")
                if sale_badge.count() > 0:
                    sale_product_containers = all_products
                    total_count = total_products
                    break
        
        all_products = self.page.locator("div.thumbnail")
        sale_index = 0
        
        for i in range(all_products.count()):
            try:
                product = all_products.nth(i)
                sale_badge = product.locator("span.sale")
                
                if sale_badge.count() > 0:
                    name_element = product.locator("h4 a").first
                    if name_element.count() == 0:
                        name_element = product.locator("a.prdocutname").first
                    if name_element.count() == 0:
                        name_element = product.locator("xpath=.//a[contains(@href, 'product/product')]").first
                    
                    name = ""
                    if name_element.count() > 0:
                        name = name_element.get_attribute("title") or name_element.text_content().strip()
                        if name == "Add to Cart" or not name:
                            product_text = product.text_content() or ""
                            import re
                            name_match = re.search(r'([A-Z][A-Z\s]+?)(?:\s*\([^)]+\))?\s*(?:\$|\n)', product_text)
                            if name_match:
                                name = name_match.group(1).strip()
                    
                    product_text = product.text_content() or ""
                    import re
                    price_values = re.findall(r'\$\d+\.?\d*', product_text)
                    price = price_values[0] if price_values else ""
                    
                    if name and name != "Add to Cart":
                        sale_items.append({
                            "name": name,
                            "price": price,
                            "original_index": i,
                            "index": sale_index
                        })
                        sale_index += 1
            except Exception as e:
                logger.warning(f"Error getting sale item {i}: {e}")
                continue
        
        return sale_items

    def add_sale_items_to_cart(self) -> int:
        from src.pages.automation_store.product_detail_page import StoreProductDetailPage
        
        sale_items = self.get_sale_items()
        added_count = 0
        listing_url = self.page.url
        
        logger.info(f"Found {len(sale_items)} sale items to add to cart")
        
        for sale_item in sale_items:
            try:
                self.page.goto(listing_url)
                self.wait_for_load_state("networkidle", timeout=20000)
                self.page.wait_for_timeout(3000)
                
                all_products = self.page.locator("div.thumbnail")
                all_products.first.wait_for(state="visible", timeout=20000)
                
                sale_products = self.page.locator("div.thumbnail:has(span.sale)")
                total_sale_products = sale_products.count()
                
                sale_index = sale_item["index"]
                
                if total_sale_products <= sale_index:
                    logger.warning(f"Sale product index {sale_index} not found (total: {total_sale_products})")
                    continue
                
                product = sale_products.nth(sale_index)
                product.wait_for(state="visible", timeout=20000)
                
                product_link = product.locator("h4 a").first
                if product_link.count() == 0:
                    product_link = product.locator("a.prdocutname").first
                if product_link.count() == 0:
                    product_link = product.locator("xpath=.//a[contains(@href, 'product/product')]").first
                
                if product_link.count() == 0:
                    logger.warning(f"Product link not found for sale item: {sale_item['name']}")
                    continue
                
                product_link.scroll_into_view_if_needed(timeout=15000)
                self.page.wait_for_timeout(500)
                product_link.click(timeout=15000)
                self.wait_for_load_state("networkidle", timeout=20000)
                
                if "product/product" in self.page.url:
                    detail_page = StoreProductDetailPage(self.page)
                    detail_page.add_to_cart()
                    self.page.wait_for_timeout(2000)
                    added_count += 1
                    logger.info(f"Added {sale_item['name']} to cart")
                else:
                    logger.warning(f"Did not navigate to product detail page for {sale_item['name']}")
            except Exception as e:
                logger.warning(f"Error adding {sale_item.get('name', 'item')} to cart: {e}")
                if "product/product" in self.page.url:
                    try:
                        self.page.go_back()
                        self.wait_for_load_state("networkidle", timeout=15000)
                        self.page.wait_for_timeout(2000)
                    except:
                        self.page.goto(listing_url)
                        self.wait_for_load_state("networkidle", timeout=15000)
                continue
        
        return added_count

    def switch_to_list_view(self) -> None:
        self.page.wait_for_timeout(2000)
        
        list_view_button = self.page.locator(f"xpath={self.get_locator('list_view_button')}")
        if list_view_button.count() == 0:
            list_view_button = self.page.locator("xpath=//button[@id='list']")
        
        if list_view_button.count() > 0:
            list_view_button.scroll_into_view_if_needed(timeout=10000)
            self.page.wait_for_timeout(500)
            list_view_button.click(timeout=30000)
            self.page.wait_for_timeout(3000)
            self.wait_for_load_state("networkidle", timeout=20000)
            logger.info("Switched to list view")
        else:
            logger.warning("List view button not found")

    def get_last_item_in_list_view(self) -> dict:
        self.wait_for_load_state("networkidle", timeout=20000)
        self.page.wait_for_timeout(2000)
        
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(2000)
        
        last_product_link = self.page.locator("xpath=//body/div[@class='container-fixed']/div[@id='maincontainer']/div[@class='container-fluid']/div[@class='col-md-12 col-xs-12 mt20']/div/div[@class='contentpanel']/div[@class='thumbnails list row']/div[9]/div[1]/div[1]/div[2]/a[1]")
        
        if last_product_link.count() == 0:
            product_links = self.page.locator("xpath=//div[@class='thumbnails list row']//a[contains(@href, 'product/product')]")
            total_count = product_links.count()
            if total_count > 0:
                last_product_link = product_links.nth(total_count - 1)
            else:
                raise Exception("No products found in list view")
        
        last_product_link.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        
        name = last_product_link.get_attribute("title") or last_product_link.text_content().strip()
        if not name or name in ["Add to Cart", "Write Review", "View"]:
            parent_container = last_product_link.locator("xpath=ancestor::div[contains(@class, 'product-thumb')]")
            if parent_container.count() > 0:
                product_text = parent_container.text_content() or ""
                import re
                lines = product_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 5 and line not in ["Add to Cart", "Write Review", "View"] and not line.startswith('$'):
                        if any(char.isalpha() for char in line):
                            name = line
                            break
        
        price_element = last_product_link.locator("xpath=ancestor::div[contains(@class, 'product-thumb')]//span[contains(@class, 'oneprice')]").first
        if price_element.count() == 0:
            price_element = last_product_link.locator("xpath=ancestor::div[contains(@class, 'product-thumb')]//div[contains(@class, 'price')]").first
        
        price_text = price_element.text_content().strip() if price_element.count() > 0 else ""
        
        return {
            "name": name,
            "price": price_text,
            "index": 8,
            "element": last_product_link
        }

    def add_last_item_from_list_view_to_cart(self) -> bool:
        from src.pages.automation_store.product_detail_page import StoreProductDetailPage
        
        try:
            last_item_info = self.get_last_item_in_list_view()
            product_link = last_item_info["element"]
            
            if product_link.count() == 0:
                logger.warning(f"Product link not found for last item: {last_item_info['name']}")
                return False
            
            product_link.scroll_into_view_if_needed(timeout=15000)
            self.page.wait_for_timeout(500)
            product_link.click(timeout=30000)
            self.page.wait_for_timeout(2000)
            self.wait_for_load_state("networkidle", timeout=20000)
            
            if "product/product" in self.page.url:
                detail_page = StoreProductDetailPage(self.page)
                detail_page.add_to_cart()
                self.page.wait_for_timeout(2000)
                logger.info(f"Added {last_item_info['name']} to cart from list view")
                return True
            else:
                logger.warning(f"Did not navigate to product detail page for {last_item_info['name']}. Current URL: {self.page.url}")
                return False
        except Exception as e:
            logger.warning(f"Error adding last item from list view to cart: {e}")
            return False

