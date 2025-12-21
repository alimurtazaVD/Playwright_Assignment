import logging
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.category_page import StoreCategoryPage
from src.pages.automation_store.product_listing_page import StoreProductListingPage
from src.pages.automation_store.product_detail_page import StoreProductDetailPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_scenario_2_apparel_shoes_cart(page, base_url):
    login_page = StoreLoginPage(page)
    login_page.open(base_url)
    login_page.click_login_link()
    
    creds = config_manager.get_test_data()["automation_store"]["login_user"]
    login_page.login(creds["username"], creds["password"])
    
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    
    category_page = StoreCategoryPage(page)
    listing_page = StoreProductListingPage(page)
    detail_page = StoreProductDetailPage(page)
    cart_page = StoreCartPage(page)
    
    category_page.click_category("APPAREL & ACCESSORIES")
    category_page.click_category("T-shirts")
    
    listing_page.sort_by_price_low_to_high()
    products = listing_page.get_products_by_price_order(3, ascending=True)
    
    expected_items = []
    
    for i, product in enumerate(products):
        listing_page.click_product_by_index(i)
        #detail_page.select_size("Medium")
        detail_page.set_quantity(1)
        detail_page.add_to_cart()
        expected_items.append({"name": product["name"], "quantity": 1})
        page.go_back()
        page.wait_for_load_state("networkidle")
        listing_page.sort_by_price_low_to_high()
    
    home_page.navigate_to_home(base_url)
    category_page.click_category("Apparel & accessories")
    category_page.click_category("Shoes")
    
    listing_page.sort_by_price_high_to_low()
    highest_products = listing_page.get_products_by_price_order(1, ascending=False)
    highest_product = highest_products[0] if highest_products else {}
    listing_page.click_product_by_index(0)
    detail_page.set_quantity(2)
    detail_page.add_to_cart()
    expected_items.append({"name": highest_product["name"], "quantity": 2})
    
    cart_page.navigate_to_cart()
    
    item_count = cart_page.get_item_count()
    assert item_count == len(expected_items), f"Expected {len(expected_items)} items, found {item_count}"
    
    all_verified = cart_page.verify_all_items_in_cart(expected_items)
    assert all_verified, "Not all expected items found in cart with correct quantities"
    
    total_items = cart_page.get_total_item_count()
    expected_total = sum(item["quantity"] for item in expected_items)
    assert total_items == expected_total, f"Expected total quantity {expected_total}, found {total_items}"

