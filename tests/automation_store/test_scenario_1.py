import logging
import sys
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.product_page import StoreProductPage
from src.pages.automation_store.product_detail_page import StoreProductDetailPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_1_dove_brand_newest_item_cart(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 1: DOVE BRAND NEWEST ITEM TO CART")
    print_flush("="*70)
    
    page = cross_browser_page
    print_flush("\n[STEP 1] Opening Automation Test Store...")
    login_page = StoreLoginPage(page)
    login_page.open(base_url)
    
    print_flush("[STEP 2] Clicking Login link...")
    login_page.click_login_link()
    
    print_flush("[STEP 3] Logging in...")
    creds = config_manager.get_test_data()["automation_store"]["login_user"]
    login_page.login(creds["username"], creds["password"])
    print_flush(f"[PASS] Logged in as: {creds['username']}")
    
    print_flush("[STEP 4] Navigating to Home page...")
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    print_flush("[PASS] Navigated to Home page")
    
    print_flush("[STEP 5] Clicking DOVE brand...")
    home_page.click_dove_brand()
    print_flush("[PASS] Navigated to DOVE brand products")
    
    print_flush("\n[STEP 6] Finding newest product...")
    product_page = StoreProductPage(page)
    newest_product = product_page.get_newest_product()
    product_name = newest_product["name"]
    product_price = newest_product["price"]
    print_flush(f"[RESULT] Newest product found:")
    print_flush(f"  - Name: {product_name}")
    print_flush(f"  - Price: {product_price}")
    
    print_flush("\n[STEP 7] Clicking newest product...")
    product_page.click_newest_product()
    print_flush("[PASS] Navigated to product detail page")
    
    print_flush("[STEP 8] Adding product to cart...")
    detail_page = StoreProductDetailPage(page)
    detail_page.add_to_cart()
    print_flush("[PASS] Product added to cart successfully")
    
    print_flush("\n[STEP 9] Navigating to cart page...")
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    print_flush("[PASS] Navigated to cart page")
    
    print_flush("\n[VERIFICATION] Verifying cart contents...")
    item_count = cart_page.get_item_count()
    print_flush(f"[RESULT] Total items in cart: {item_count}")
    assert item_count >= 1, f"Expected at least 1 item in cart, but found {item_count}"
    print_flush("[PASS] Cart contains at least 1 item")
    
    cart_item = cart_page.verify_item_in_cart(product_name)
    assert cart_item, f"Expected item '{product_name}' not found in cart"
    print_flush(f"[PASS] Product '{product_name}' found in cart")
    
    actual_quantity = cart_item.get("quantity", 0)
    print_flush(f"[RESULT] Product quantity: {actual_quantity}")
    assert actual_quantity >= 1, f"Expected quantity at least 1, Actual: {actual_quantity}"
    print_flush("[PASS] Quantity verification passed")
    
    actual_price = cart_item.get("price", "")
    print_flush(f"[RESULT] Product price: {actual_price}")
    assert actual_price, f"Expected price to be present, but found: {actual_price}"
    print_flush("[PASS] Price verification passed")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Product Name: {product_name}")
    print_flush(f"  Product Price: {product_price}")
    print_flush(f"  Items in Cart: {item_count}")
    print_flush(f"  Cart Quantity: {actual_quantity}")
    print_flush(f"  Cart Price: {actual_price}")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

