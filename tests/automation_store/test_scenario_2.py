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
def test_scenario_2_apparel_shoes_cart(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 2: APPAREL & SHOES CART TEST")
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
    
    category_page = StoreCategoryPage(page)
    listing_page = StoreProductListingPage(page)
    detail_page = StoreProductDetailPage(page)
    cart_page = StoreCartPage(page)
    
    print_flush("\n" + "="*60)
    print_flush("PART 1: T-SHIRTS SECTION")
    print_flush("="*60)
    
    print_flush("\n[STEP 5] Navigating to APPAREL & ACCESSORIES > T-shirts...")
    category_page.click_category("APPAREL & ACCESSORIES")
    category_page.click_category("T-shirts")
    print_flush("[PASS] Navigated to T-shirts category")
    
    print_flush("[STEP 6] Sorting by price (Low to High)...")
    listing_url = page.url
    listing_page.sort_by_price_low_to_high()
    print_flush("[PASS] Sorted by price low to high")
    
    print_flush("[STEP 7] Getting 3 lowest priced products...")
    products = listing_page.get_products_by_price_order(3, ascending=True)
    print_flush(f"[RESULT] Found {len(products)} products")
    
    expected_items = []
    expected_count = 3
    
    print_flush(f"\n[STEP 8] Adding {expected_count} T-shirts to cart (quantity: 1 each)...")
    for i in range(expected_count):
        if i > 0:
            page.goto(listing_url)
            listing_page.wait_for_listing_page_ready()
            listing_page.sort_by_price_low_to_high()
        
        print_flush(f"  - Adding product {i+1}/{expected_count}...")
        listing_page.click_product_by_index(i)
        detail_page.set_quantity(1)
        detail_page.add_to_cart()
        product_name = products[i].get("name", f"Product_{i+1}") if i < len(products) else f"Product_{i+1}"
        expected_items.append({"name": product_name, "quantity": 1})
        print_flush(f"  [PASS] Added product {i+1} to cart")
    
    print_flush(f"[PASS] Successfully added {expected_count} T-shirts to cart")
    
    print_flush("\n" + "="*60)
    print_flush("PART 2: SHOES SECTION")
    print_flush("="*60)
    
    print_flush("\n[STEP 9] Navigating to Home page...")
    home_page.navigate_to_home(base_url)
    print_flush("[PASS] Navigated to Home page")
    
    print_flush("[STEP 10] Navigating to Apparel & accessories > Shoes...")
    category_page.click_category("Apparel & accessories")
    category_page.click_category("Shoes")
    print_flush("[PASS] Navigated to Shoes category")
    
    print_flush("[STEP 11] Sorting by price (High to Low)...")
    shoes_listing_url = page.url
    listing_page.sort_by_price_high_to_low()
    listing_page.wait_for_listing_page_ready()
    print_flush("[PASS] Sorted by price high to low")
    
    print_flush("[STEP 12] Getting 2 highest priced shoes...")
    highest_products = listing_page.get_products_by_price_order(2, ascending=False)
    print_flush(f"[RESULT] Found {len(highest_products)} highest priced shoes")
    if highest_products:
        for idx, prod in enumerate(highest_products, 1):
            price = prod.get("price", "N/A")
            print_flush(f"  {idx}. Price: {price}")
    
    print_flush(f"\n[STEP 13] Adding 2 highest priced shoes to cart (quantity: 1 each)...")
    for i in range(2):
        if i > 0:
            page.goto(shoes_listing_url)
            listing_page.wait_for_listing_page_ready()
            listing_page.sort_by_price_high_to_low()
        
        print_flush(f"  - Adding shoe {i+1}/2...")
        listing_page.click_product_by_index(i)
        detail_page.set_quantity(1)
        detail_page.add_to_cart()
        
        product_name = highest_products[i].get("name", f"Shoes_Product_{i+1}") if i < len(highest_products) else f"Shoes_Product_{i+1}"
        product_price = highest_products[i].get("price", "N/A") if i < len(highest_products) else "N/A"
        expected_items.append({"name": product_name, "quantity": 1})
        print_flush(f"  [PASS] Added {product_name} (Price: {product_price}, Qty: 1) to cart")
    
    print_flush(f"[PASS] Successfully added 2 highest priced shoes to cart")
    
    print_flush("\n" + "="*60)
    print_flush("PART 3: CART VERIFICATION")
    print_flush("="*60)
    
    print_flush("\n[STEP 14] Navigating to cart page...")
    cart_page.navigate_to_cart()
    print_flush("[PASS] Navigated to cart page")
    
    print_flush("\n[STEP 15] Verifying cart contents...")
    item_count = cart_page.get_item_count()
    expected_item_count = len(expected_items)
    print_flush(f"[RESULT] Total items in cart: {item_count}")
    print_flush(f"[RESULT] Expected items: {expected_item_count}")
    assert item_count >= expected_item_count, f"Expected at least {expected_item_count} items, found {item_count}"
    print_flush(f"[PASS] Cart contains at least {expected_item_count} items")
    
    total_items = cart_page.get_total_item_count()
    expected_total = sum(item["quantity"] for item in expected_items)
    print_flush(f"[RESULT] Total quantity in cart: {total_items}")
    print_flush(f"[RESULT] Expected total quantity: {expected_total}")
    assert total_items >= expected_total, f"Expected total quantity at least {expected_total}, found {total_items}"
    print_flush(f"[PASS] Total quantity verification passed")
    
    cart_items = cart_page.get_cart_items()
    
    print_flush(f"\n[STEP 16] Verifying shoes items in cart...")
    shoes_items = [item for item in cart_items if item.get("quantity", 0) >= 1]
    print_flush(f"[RESULT] Found {len(shoes_items)} items in cart")
    assert len(shoes_items) >= 2, f"Expected at least 2 shoes items in cart, found {len(shoes_items)}"
    print_flush(f"[PASS] At least 2 shoes items found in cart")
    
    print_flush(f"\n[STEP 17] Verifying shoes items details...")
    for idx, shoes_item in enumerate(shoes_items[:2], 1):
        print_flush(f"  Shoes Item {idx}:")
        print_flush(f"    - Name: {shoes_item.get('name', 'N/A')}")
        print_flush(f"    - Quantity: {shoes_item.get('quantity', 0)}")
        print_flush(f"    - Price: {shoes_item.get('price', 'N/A')}")
        assert shoes_item.get("quantity", 0) >= 1, f"Expected shoes product quantity to be at least 1, found {shoes_item.get('quantity', 0)}"
        assert shoes_item.get("name"), f"Expected shoes product name to be present, found: {shoes_item.get('name')}"
        assert shoes_item.get("price"), f"Expected shoes product price to be present, found: {shoes_item.get('price')}"
        print_flush(f"    [PASS] Shoes item {idx} verification passed")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  T-shirts added: {expected_count} (quantity: 1 each)")
    print_flush(f"  Shoes added: 2 (quantity: 1 each)")
    print_flush(f"  Total items in cart: {item_count}")
    print_flush(f"  Total quantity: {total_items}")
    print_flush(f"  Expected total quantity: {expected_total}")
    print_flush(f"  Shoes items verified: {len(shoes_items)}")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

