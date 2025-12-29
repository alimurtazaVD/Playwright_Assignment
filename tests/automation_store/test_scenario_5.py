import logging
import sys
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.category_page import StoreCategoryPage
from src.pages.automation_store.product_listing_page import StoreProductListingPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_5_fragrance_sale_items_list_view(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 5: FRAGRANCE SALE ITEMS - LIST VIEW")
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
    
    print_flush("\n[STEP 5] Navigating to Fragrance section...")
    category_page = StoreCategoryPage(page)
    category_page.click_fragrance()
    print_flush("[PASS] Navigated to Fragrance category")
    
    listing_page = StoreProductListingPage(page)
    listing_page.wait_for_listing_page_ready()
    
    print_flush("\n[STEP 6] Scrolling to bottom to find sale items...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)
    print_flush("[PASS] Scrolled to bottom and back")
    
    print_flush("\n[STEP 7] Finding sale items in Fragrance section...")
    sale_items_count = listing_page.count_sale_items()
    print_flush(f"[RESULT] Total items on sale: {sale_items_count}")
    
    sale_items = listing_page.get_sale_items()
    if sale_items:
        print_flush(f"[RESULT] Found {len(sale_items)} sale item(s):")
        for idx, item in enumerate(sale_items, 1):
            name_clean = item['name'].split('\t')[0].strip()
            print_flush(f"  {idx}. {name_clean} - {item['price']}")
    
    assert sale_items_count > 0, "No sale items found in Fragrance section"
    print_flush("[PASS] Sale items found")
    
    print_flush("\n[STEP 8] Adding sale item to cart (first time)...")
    listing_url = page.url
    added_count = listing_page.add_sale_items_to_cart()
    print_flush(f"[RESULT] Added {added_count} sale item(s) to cart")
    assert added_count > 0, "Failed to add sale item to cart"
    print_flush("[PASS] Sale item added to cart successfully")
    
    print_flush("\n[STEP 9] Switching to list view...")
    page.goto(listing_url)
    listing_page.wait_for_listing_page_ready()
    listing_page.switch_to_list_view()
    print_flush("[PASS] Switched to list view")
    
    print_flush("\n[STEP 10] Scrolling to last item in list view...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    print_flush("[PASS] Scrolled to bottom")
    
    print_flush("\n[STEP 11] Getting last item information...")
    last_item_info = listing_page.get_last_item_in_list_view()
    print_flush(f"[RESULT] Last item: {last_item_info['name']}")
    print_flush(f"[RESULT] Last item price: {last_item_info['price']}")
    print_flush("[PASS] Last item information retrieved")
    
    print_flush("\n[STEP 12] Adding last item to cart (second time)...")
    added_from_list = listing_page.add_last_item_from_list_view_to_cart()
    assert added_from_list, "Failed to add last item from list view to cart"
    print_flush("[PASS] Last item added to cart from list view")
    
    print_flush("\n[STEP 13] Navigating to cart page...")
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    print_flush("[PASS] Navigated to cart page")
    
    print_flush("\n[VERIFICATION] Verifying cart contents...")
    total_items_in_cart = cart_page.get_item_count()
    total_quantity = cart_page.get_total_item_count()
    total_amount = cart_page.get_total_amount()
    
    print_flush(f"\n[CART SUMMARY]")
    print_flush("-" * 70)
    print_flush(f"  Total items in cart: {total_items_in_cart}")
    print_flush(f"  Total quantity: {total_quantity}")
    print_flush(f"  Total amount: {total_amount}")
    print_flush("-" * 70)
    
    cart_items = cart_page.get_cart_items()
    if cart_items:
        print_flush(f"\n[CART ITEMS DETAILS] ({len(cart_items)} items):")
        print_flush("-" * 70)
        for idx, item in enumerate(cart_items, 1):
            print_flush(f"  {idx}. {item['name']}")
            print_flush(f"     Quantity: {item['quantity']} | Price: {item['price']}")
        print_flush("-" * 70)
    
    print_flush("\n[VERIFICATION] Running assertions...")
    
    expected_min_items = 1
    assert total_items_in_cart >= expected_min_items, f"Expected at least {expected_min_items} item(s) in cart, found {total_items_in_cart}"
    print_flush(f"[PASS] Cart contains at least {expected_min_items} item(s)")
    
    expected_min_quantity = 2
    assert total_quantity >= expected_min_quantity, f"Expected total quantity at least {expected_min_quantity}, found {total_quantity}"
    print_flush(f"[PASS] Total quantity is at least {expected_min_quantity}")
    
    assert total_amount, f"Expected total amount to be present, but found: {total_amount}"
    print_flush(f"[PASS] Total amount is present: {total_amount}")
    
    sale_item_name = sale_items[0]['name'].split('\t')[0].strip() if sale_items else ""
    sale_item_quantity = 0
    if sale_item_name:
        found_sale_item = False
        for cart_item in cart_items:
            if sale_item_name.lower() in cart_item['name'].lower():
                found_sale_item = True
                sale_item_quantity = cart_item['quantity']
                print_flush(f"[PASS] Sale item '{sale_item_name}' found in cart")
                print_flush(f"[RESULT] Sale item quantity in cart: {sale_item_quantity}")
                break
        assert found_sale_item, f"Expected sale item '{sale_item_name}' in cart"
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Sale items found: {sale_items_count}")
    print_flush(f"  Sale item name: {sale_item_name}")
    print_flush(f"  Items added (first time): {added_count}")
    print_flush(f"  Last item added (second time): {added_from_list}")
    print_flush(f"  Sale item quantity in cart: {sale_item_quantity}")
    print_flush(f"  Total items in cart: {total_items_in_cart}")
    print_flush(f"  Total quantity: {total_quantity}")
    print_flush(f"  Total amount: {total_amount}")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

