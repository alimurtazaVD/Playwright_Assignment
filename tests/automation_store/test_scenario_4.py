import logging
import sys
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.category_page import StoreCategoryPage
from src.pages.automation_store.product_listing_page import StoreProductListingPage
from src.pages.automation_store.product_detail_page import StoreProductDetailPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_4_men_product_starts_with_m(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 4: MEN SECTION - PRODUCT NAME STARTS WITH 'M'")
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
    
    print_flush("\n[STEP 5] Navigating to Men section...")
    category_page = StoreCategoryPage(page)
    category_page.click_men()
    print_flush("[PASS] Navigated to Men section")
    
    print_flush("\n[STEP 6] Scrolling down to load all products...")
    listing_page = StoreProductListingPage(page)
    listing_page.wait_for_listing_page_ready()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)
    print_flush("[PASS] Scrolled down and back up to load products")
    
    print_flush("\n[STEP 7] Finding products whose name starts with 'M'...")
    product_1_locator = "//a[@title='Men+Care Clean Comfort Deodorant']"
    product_2_locator = "//a[@title='Men+Care Active Clean Shower Tool']"
    
    product_1 = page.locator(f"xpath={product_1_locator}").first
    product_2 = page.locator(f"xpath={product_2_locator}").first
    
    if product_1.count() == 0 or product_2.count() == 0:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        product_1 = page.locator(f"xpath={product_1_locator}").first
        product_2 = page.locator(f"xpath={product_2_locator}").first
    
    assert product_1.count() > 0, "Product 'Men+Care Clean Comfort Deodorant' not found"
    assert product_2.count() > 0, "Product 'Men+Care Active Clean Shower Tool' not found"
    
    product_1_name = product_1.get_attribute("title") or "Men+Care Clean Comfort Deodorant"
    product_2_name = product_2.get_attribute("title") or "Men+Care Active Clean Shower Tool"
    
    print_flush(f"[RESULT] Found 2 products starting with 'M':")
    print_flush(f"  1. {product_1_name}")
    print_flush(f"  2. {product_2_name}")
    
    men_listing_url = page.url
    expected_items = []
    
    print_flush(f"\n[STEP 8] Adding first product '{product_1_name}' to cart...")
    product_1.scroll_into_view_if_needed()
    product_1.click(timeout=30000)
    page.wait_for_timeout(2000)
    print_flush("[PASS] Navigated to product detail page")
    
    detail_page = StoreProductDetailPage(page)
    detail_page.set_quantity(1)
    detail_page.add_to_cart()
    expected_items.append({"name": product_1_name, "quantity": 1})
    print_flush(f"[PASS] Added '{product_1_name}' to cart")
    
    print_flush(f"\n[STEP 9] Adding second product '{product_2_name}' to cart...")
    page.goto(men_listing_url)
    listing_page.wait_for_listing_page_ready()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    
    product_2 = page.locator(f"xpath={product_2_locator}").first
    product_2.scroll_into_view_if_needed()
    product_2.click(timeout=30000)
    page.wait_for_timeout(2000)
    print_flush("[PASS] Navigated to product detail page")
    
    detail_page.set_quantity(1)
    detail_page.add_to_cart()
    expected_items.append({"name": product_2_name, "quantity": 1})
    print_flush(f"[PASS] Added '{product_2_name}' to cart")
    
    print_flush("\n[STEP 10] Navigating to cart page...")
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    print_flush("[PASS] Navigated to cart page")
    
    print_flush("\n[VERIFICATION] Verifying cart contents...")
    item_count = cart_page.get_item_count()
    print_flush(f"[RESULT] Total items in cart: {item_count}")
    assert item_count >= 2, f"Expected at least 2 items in cart, but found {item_count}"
    print_flush("[PASS] Cart contains at least 2 items")
    
    cart_items = cart_page.get_cart_items()
    print_flush(f"\n[STEP 11] Verifying products starting with 'M' are in cart...")
    
    products_with_m = []
    for item in cart_items:
        item_name = item.get("name", "").strip()
        if item_name.upper().startswith("M"):
            products_with_m.append(item)
            print_flush(f"[RESULT] Found product: {item_name}")
            print_flush(f"  - Quantity: {item.get('quantity', 0)}")
            print_flush(f"  - Price: {item.get('price', 'N/A')}")
    
    assert len(products_with_m) >= 2, f"Expected at least 2 products starting with 'M' in cart, found {len(products_with_m)}"
    print_flush(f"[PASS] Found {len(products_with_m)} product(s) starting with 'M'")
    
    for idx, item in enumerate(products_with_m[:2], 1):
        item_name = item.get("name", "").strip()
        assert item_name.upper().startswith("M"), f"Expected product name to start with 'M', found: {item_name}"
        print_flush(f"[PASS] Product {idx} '{item_name}' starts with 'M'")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Product 1: {product_1_name}")
    print_flush(f"  Product 2: {product_2_name}")
    print_flush(f"  Items in Cart: {item_count}")
    print_flush(f"  Products Starting with 'M': {len(products_with_m)}")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

