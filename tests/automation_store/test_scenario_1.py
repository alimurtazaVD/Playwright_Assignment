import logging
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.product_page import StoreProductPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_scenario_1_dove_brand_newest_item_cart(page, base_url):
    login_page = StoreLoginPage(page)
    login_page.open(base_url)
    login_page.click_login_link()
    
    creds = config_manager.get_test_data()["automation_store"]["login_user"]
    login_page.login(creds["username"], creds["password"])
    
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    
    home_page.click_dove_brand()
    
    product_page = StoreProductPage(page)
    newest_product = product_page.get_newest_product()
    product_name = newest_product["name"]
    product_price = newest_product["price"]
    
    product_page.click_newest_product()
    product_page.add_to_cart()
    
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    
    item_count = cart_page.get_item_count()
    assert item_count >= 1, f"Expected at least 1 item in cart, but found {item_count}"
    
    cart_item = cart_page.verify_item_in_cart(product_name)
    assert cart_item, f"Expected item '{product_name}' not found in cart"
    
    actual_quantity = cart_item.get("quantity", 0)
    assert actual_quantity == 1, f"Expected quantity: 1, Actual: {actual_quantity}"
    
    actual_price = cart_item.get("price", "")
    assert actual_price, f"Expected price to be present, but found: {actual_price}"

