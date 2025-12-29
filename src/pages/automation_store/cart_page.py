import logging
from playwright.sync_api import Page
from ..base_page import BasePage

logger = logging.getLogger(__name__)


class StoreCartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "cart", task_name="automation_store")

    def navigate_to_cart(self) -> None:
        try:
            cart_link = self.page.get_by_role("link", name="Cart", exact=False).first
            if cart_link.count() > 0:
                cart_link.click(timeout=30000)
            else:
                base_url = self.page.url.split('/index.php')[0] if '/index.php' in self.page.url else self.page.url.rstrip('/')
                cart_url = f"{base_url}/index.php?rt=checkout/cart"
                self.page.goto(cart_url)
        except:
            try:
                self.page.locator("#cart_checkout1").click(timeout=30000)
            except:
                base_url = self.page.url.split('/index.php')[0] if '/index.php' in self.page.url else self.page.url.rstrip('/')
                cart_url = f"{base_url}/index.php?rt=checkout/cart"
                self.page.goto(cart_url)
        
        self.wait_for_load_state("networkidle", timeout=30000)

    def get_cart_items(self) -> list:
        items = []
        self.page.wait_for_timeout(2000)
        cart_items_xpath = self.get_locator("cart_items")
        cart_items = self.page.locator(f"xpath={cart_items_xpath}")
        cart_items.first.wait_for(state="visible", timeout=30000)
        count = cart_items.count()
        
        for i in range(count):
            try:
                item = cart_items.nth(i)
                name_xpath = self.get_locator("item_name")
                name_element = item.locator(f"xpath={name_xpath}")
                name = name_element.text_content().strip() if name_element.count() > 0 else ""
                
                quantity_xpath = self.get_locator("item_quantity")
                quantity_element = item.locator(f"xpath={quantity_xpath}")
                quantity = "1"
                if quantity_element.count() > 0:
                    try:
                        quantity = quantity_element.get_attribute("value") or quantity_element.input_value() or "1"
                        if not quantity or quantity == "":
                            quantity = "1"
                    except:
                        try:
                            quantity = quantity_element.input_value() or "1"
                        except:
                            quantity = "1"
                
                price_xpath = self.get_locator("item_price")
                price_element = item.locator(f"xpath={price_xpath}").first
                price = price_element.text_content().strip() if price_element.count() > 0 else ""
                
                if name:
                    items.append({
                        "name": name,
                        "quantity": int(quantity) if quantity.isdigit() else 1,
                        "price": price
                    })
            except Exception as e:
                logger.warning(f"Error getting cart item {i}: {e}")
                continue
        
        return items

    def get_item_count(self) -> int:
        cart_items_xpath = self.get_locator("cart_items")
        all_rows = self.page.locator(f"xpath={cart_items_xpath}")
        count = 0
        
        for i in range(all_rows.count()):
            row = all_rows.nth(i)
            name_element = row.locator(f"xpath={self.get_locator('item_name')}")
            if name_element.count() > 0:
                count += 1
        
        return count

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

    def get_total_amount(self) -> str:
        total_price_xpath = self.get_locator("total_price")
        total_element = self.page.locator(f"xpath={total_price_xpath}")
        if total_element.count() > 0:
            return total_element.text_content().strip()
        return ""

    def get_cart_count_from_header(self) -> dict:
        cart_link_xpath = self.get_locator("cart_link_header")
        cart_link = self.page.locator(f"xpath={cart_link_xpath}")
        if cart_link.count() > 0:
            text = cart_link.text_content().strip()
            import re
            items_match = re.search(r'(\d+)\s+Items', text)
            amount_match = re.search(r'\$([\d.]+)', text)
            return {
                "count": int(items_match.group(1)) if items_match else 0,
                "amount": f"${amount_match.group(1)}" if amount_match else ""
            }
        return {"count": 0, "amount": ""}

    def checkout(self) -> None:
        checkout_locator = self.get_locator("cart_checkout_button")
        checkout_button = self.page.locator(f"xpath={checkout_locator}")
        if checkout_button.count() == 0:
            checkout_button = self.page.locator("xpath=//a[@id='cart_checkout2']")
        if checkout_button.count() == 0:
            checkout_button = self.page.locator("xpath=//a[contains(@href, 'checkout')]")
        if checkout_button.count() == 0:
            checkout_button = self.page.get_by_role("link", name="Checkout", exact=False)
        
        if checkout_button.count() > 0:
            checkout_button.click(timeout=30000)
            self.page.wait_for_timeout(2000)
            self.wait_for_load_state("networkidle", timeout=30000)
            logger.info("Checkout button clicked successfully")
        else:
            logger.warning("Checkout button not found")

    def change_currency_to_euro(self) -> None:
        currency_dropdown = self.page.locator("xpath=//li[contains(@class, 'dropdown')]//a[contains(@class, 'dropdown-toggle') and contains(text(), 'Dollar')]").first
        if currency_dropdown.count() == 0:
            currency_dropdown = self.page.locator("xpath=//a[contains(@class, 'dropdown-toggle') and contains(text(), 'Dollar')]").first
        if currency_dropdown.count() == 0:
            currency_dropdown = self.page.locator("xpath=//li[contains(@class, 'dropdown')]//a[@class='dropdown-toggle']").first
        
        if currency_dropdown.count() > 0:
            currency_dropdown.click(timeout=30000)
            self.page.wait_for_timeout(1000)
            
            euro_option = self.page.locator("xpath=//a[contains(@href, 'currency=EUR')]").first
            if euro_option.count() == 0:
                euro_option = self.page.locator("xpath=//a[contains(text(), 'Euro')]").first
            if euro_option.count() == 0:
                euro_option = self.page.locator("xpath=//a[contains(text(), 'EUR')]").first
            if euro_option.count() == 0:
                euro_option = self.page.locator("xpath=//ul[contains(@class, 'dropdown-menu')]//a[contains(@href, 'EUR')]").first
            
            if euro_option.count() > 0:
                euro_option.click(timeout=30000)
                self.page.wait_for_timeout(3000)
                self.wait_for_load_state("networkidle", timeout=20000)
                logger.info("Currency changed to Euro")
            else:
                logger.warning("Euro option not found in currency dropdown")
        else:
            logger.warning("Currency dropdown not found")

    def get_subtotal_in_euro(self) -> float:
        self.page.wait_for_timeout(2000)
        subtotal_locator = self.get_locator("subtotal")
        subtotal_element = self.page.locator(f"xpath={subtotal_locator}")
        
        if subtotal_element.count() == 0:
            subtotal_element = self.page.locator("xpath=//table//tr[contains(., 'Sub-Total')]//td[2]//span")
        if subtotal_element.count() == 0:
            subtotal_element = self.page.locator("xpath=//table//tr[contains(., 'Sub-Total')]//td[last()]")
        if subtotal_element.count() == 0:
            subtotal_element = self.page.locator("xpath=//table//tr[contains(., 'Sub-Total')]//td[contains(@class, 'align_right')]")
        
        if subtotal_element.count() > 0:
            subtotal_text = subtotal_element.text_content().strip()
            import re
            subtotal_text_clean = subtotal_text.replace(',', '').replace('€', '').replace('EUR', '').replace('Euro', '').strip()
            amount_match = re.search(r'([\d]+\.?\d*)', subtotal_text_clean)
            if amount_match:
                return float(amount_match.group(1))
        
        return 0.0

    def get_cart_items_with_totals(self) -> list:
        items = []
        self.page.wait_for_timeout(2000)
        cart_items_xpath = self.get_locator("cart_items")
        cart_items = self.page.locator(f"xpath={cart_items_xpath}")
        cart_items.first.wait_for(state="visible", timeout=30000)
        count = cart_items.count()
        
        for i in range(count):
            try:
                item = cart_items.nth(i)
                name_xpath = self.get_locator("item_name")
                name_element = item.locator(f"xpath={name_xpath}")
                name = name_element.text_content().strip() if name_element.count() > 0 else ""
                
                quantity_xpath = self.get_locator("item_quantity")
                quantity_element = item.locator(f"xpath={quantity_xpath}")
                quantity = "1"
                if quantity_element.count() > 0:
                    try:
                        quantity = quantity_element.get_attribute("value") or quantity_element.input_value() or "1"
                        if not quantity or quantity == "":
                            quantity = "1"
                    except:
                        try:
                            quantity = quantity_element.input_value() or "1"
                        except:
                            quantity = "1"
                
                price_xpath = self.get_locator("item_price")
                price_element = item.locator(f"xpath={price_xpath}").first
                unit_price = price_element.text_content().strip() if price_element.count() > 0 else ""
                
                total_xpath = self.get_locator("item_total")
                total_elements = item.locator(f"xpath={total_xpath}")
                item_total = ""
                if total_elements.count() >= 2:
                    item_total = total_elements.nth(1).text_content().strip()
                elif total_elements.count() == 1:
                    item_total = total_elements.first.text_content().strip()
                
                if name:
                    import re
                    unit_price_value = 0.0
                    total_value = 0.0
                    
                    if unit_price:
                        price_match = re.search(r'([\d,]+\.?\d*)', unit_price.replace(',', ''))
                        if price_match:
                            unit_price_value = float(price_match.group(1))
                    
                    if item_total:
                        item_total_clean = item_total.replace(',', '').replace('€', '').replace('EUR', '').replace('Euro', '').replace('$', '').strip()
                        total_match = re.search(r'([\d]+\.?\d*)', item_total_clean)
                        if total_match:
                            total_value = float(total_match.group(1))
                    
                    items.append({
                        "name": name,
                        "quantity": int(quantity) if quantity.isdigit() else 1,
                        "unit_price": unit_price,
                        "unit_price_value": unit_price_value,
                        "total": item_total,
                        "total_value": total_value,
                        "index": i
                    })
            except Exception as e:
                logger.warning(f"Error getting cart item {i}: {e}")
                continue
        
        return items

    def delete_item_by_index(self, index: int) -> bool:
        try:
            cart_items_xpath = self.get_locator("cart_items")
            cart_items = self.page.locator(f"xpath={cart_items_xpath}")
            
            if index >= cart_items.count():
                logger.warning(f"Item index {index} out of range")
                return False
            
            item = cart_items.nth(index)
            remove_button = item.locator(f"xpath={self.get_locator('item_remove')}")
            
            if remove_button.count() == 0:
                remove_button = item.locator("xpath=.//a[contains(@title, 'Remove')]")
            if remove_button.count() == 0:
                remove_button = item.locator("xpath=.//a[contains(@href, 'remove')]")
            if remove_button.count() == 0:
                remove_button = item.locator("xpath=.//td[last()]//a")
            
            if remove_button.count() > 0:
                remove_button.click(timeout=30000)
                self.page.wait_for_timeout(2000)
                self.wait_for_load_state("networkidle", timeout=20000)
                logger.info(f"Deleted item at index {index}")
                return True
            else:
                logger.warning(f"Remove button not found for item at index {index}")
                return False
        except Exception as e:
            logger.warning(f"Error deleting item at index {index}: {e}")
            return False

    def get_total_amount_in_euro(self) -> float:
        total_price_xpath = self.get_locator("total_price")
        total_element = self.page.locator(f"xpath={total_price_xpath}")
        
        if total_element.count() == 0:
            total_element = self.page.locator("xpath=//table//tr[contains(., 'Total')]//td[2]//span")
        if total_element.count() == 0:
            total_element = self.page.locator("xpath=//table//tr[last()]//td[last()]//span")
        if total_element.count() == 0:
            total_element = self.page.locator("xpath=//table//tr[contains(., 'Total')]//td[contains(@class, 'align_right')]")
        
        if total_element.count() > 0:
            total_text = total_element.text_content().strip()
            import re
            total_text_clean = total_text.replace(',', '').replace('€', '').replace('EUR', '').replace('Euro', '').strip()
            amount_match = re.search(r'([\d]+\.?\d*)', total_text_clean)
            if amount_match:
                return float(amount_match.group(1))
        
        return 0.0

    def apply_coupon(self, coupon_code: str) -> bool:
        try:
            coupon_input = self.page.locator(f"xpath={self.get_locator('coupon_input')}")
            if coupon_input.count() == 0:
                coupon_input = self.page.locator("input[name='coupon']")
            if coupon_input.count() == 0:
                coupon_input = self.page.locator("input#coupon")
            
            if coupon_input.count() > 0:
                coupon_input.fill(coupon_code)
                self.page.wait_for_timeout(500)
                
                apply_button = self.page.locator(f"xpath={self.get_locator('apply_coupon_button')}")
                if apply_button.count() == 0:
                    apply_button = self.page.locator("button:has-text('Apply Coupon')")
                if apply_button.count() == 0:
                    apply_button = self.page.locator("xpath=//button[contains(text(), 'Apply')]")
                if apply_button.count() == 0:
                    apply_button = self.page.locator("xpath=//input[@type='submit' and contains(@value, 'Apply')]")
                
                if apply_button.count() > 0:
                    apply_button.click(timeout=30000)
                    self.page.wait_for_timeout(2000)
                    self.wait_for_load_state("networkidle", timeout=20000)
                    logger.info(f"Applied coupon code: {coupon_code}")
                    return True
                else:
                    logger.warning("Apply coupon button not found")
                    return False
            else:
                logger.warning("Coupon input field not found")
                return False
        except Exception as e:
            logger.warning(f"Error applying coupon: {e}")
            return False

    def remove_coupon(self) -> bool:
        try:
            remove_button = self.page.locator(f"xpath={self.get_locator('remove_coupon_button')}")
            if remove_button.count() == 0:
                remove_button = self.page.locator("xpath=//a[contains(@href, 'remove')]")
            if remove_button.count() == 0:
                remove_button = self.page.locator("xpath=//a[contains(text(), 'Remove')]")
            if remove_button.count() == 0:
                remove_button = self.page.locator("xpath=//span[contains(@class, 'remove')]//a")
            
            if remove_button.count() > 0:
                remove_button.click(timeout=30000)
                self.page.wait_for_timeout(2000)
                self.wait_for_load_state("networkidle", timeout=20000)
                logger.info("Removed coupon")
                return True
            else:
                logger.warning("Remove coupon button not found")
                return False
        except Exception as e:
            logger.warning(f"Error removing coupon: {e}")
            return False

    def complete_checkout_steps(self) -> str:
        try:
            self.page.wait_for_timeout(2000)
            
            step = 1
            max_steps = 5
            
            while step <= max_steps:
                current_url = self.page.url
                logger.info(f"Checkout step {step}, URL: {current_url}")
                
                if "success" in current_url.lower() or "confirm" in current_url.lower():
                    confirmation_message = self.get_order_confirmation_message()
                    return confirmation_message
                
                continue_button = self.page.locator("xpath=//button[contains(text(), 'Continue')]")
                if continue_button.count() == 0:
                    continue_button = self.page.locator("xpath=//input[@type='submit' and contains(@value, 'Continue')]")
                if continue_button.count() == 0:
                    continue_button = self.page.locator("xpath=//button[@id='checkout_btn']")
                if continue_button.count() == 0:
                    continue_button = self.page.locator("xpath=//a[contains(@href, 'checkout') and contains(text(), 'Continue')]")
                
                confirm_button = self.page.locator("xpath=//button[contains(text(), 'Confirm')]")
                if confirm_button.count() == 0:
                    confirm_button = self.page.locator("xpath=//input[@type='submit' and contains(@value, 'Confirm')]")
                if confirm_button.count() == 0:
                    confirm_button = self.page.locator("xpath=//button[@id='checkout_btn']")
                
                if confirm_button.count() > 0:
                    confirm_button.click(timeout=30000)
                    self.page.wait_for_timeout(3000)
                    self.wait_for_load_state("networkidle", timeout=30000)
                    logger.info("Order confirmed")
                    confirmation_message = self.get_order_confirmation_message()
                    return confirmation_message
                elif continue_button.count() > 0:
                    continue_button.click(timeout=30000)
                    self.page.wait_for_timeout(2000)
                    self.wait_for_load_state("networkidle", timeout=20000)
                    step += 1
                else:
                    logger.warning(f"No continue or confirm button found at step {step}")
                    break
            
            confirmation_message = self.get_order_confirmation_message()
            return confirmation_message
        except Exception as e:
            logger.warning(f"Error completing checkout steps: {e}")
            return ""

    def confirm_order(self) -> str:
        return self.complete_checkout_steps()

    def get_order_confirmation_message(self) -> str:
        try:
            self.page.wait_for_timeout(2000)
            
            confirmation = self.page.locator(f"xpath={self.get_locator('order_confirmation_message')}")
            if confirmation.count() == 0:
                confirmation = self.page.locator("xpath=//div[contains(@class, 'success')]")
            if confirmation.count() == 0:
                confirmation = self.page.locator("xpath=//div[contains(@class, 'alert-success')]")
            if confirmation.count() == 0:
                confirmation = self.page.locator("xpath=//h1[contains(text(), 'order') or contains(text(), 'confirm')]")
            if confirmation.count() == 0:
                confirmation = self.page.locator("xpath=//div[contains(text(), 'order') and contains(text(), 'confirm')]")
            
            if confirmation.count() > 0:
                message = confirmation.text_content().strip()
                logger.info(f"Order confirmation message: {message}")
                return message
            else:
                page_text = self.page.locator("body").text_content()
                if "order" in page_text.lower() and ("confirm" in page_text.lower() or "success" in page_text.lower()):
                    logger.info("Order confirmation found in page text")
                    return "Order confirmed successfully"
                return ""
        except Exception as e:
            logger.warning(f"Error getting order confirmation message: {e}")
            return ""

