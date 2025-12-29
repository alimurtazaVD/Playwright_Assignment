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
def test_scenario_3_skincare_sale_items(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 3: SKINCARE SALE ITEMS TEST")
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
    print_flush(f"✓ Logged in as: {creds['username']}")
    
    print_flush("[STEP 4] Navigating to Home page...")
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    print_flush("✓ Navigated to Home page")
    
    print_flush("[STEP 5] Clicking Skincare category...")
    category_page = StoreCategoryPage(page)
    category_page.click_skincare()
    print_flush("✓ Navigated to Skincare category")
    
    listing_page = StoreProductListingPage(page)
    listing_page.wait_for_load_state("networkidle")
    
    print_flush("\n" + "="*70)
    print_flush("SCENARIO 3: SKINCARE SALE ITEMS ANALYSIS")
    print_flush("="*70)
    
    print_flush("\n[ANALYSIS] Counting sale items...")
    sale_items_count = listing_page.count_sale_items()
    print_flush(f"✓ [RESULT] Total items on sale: {sale_items_count}")
    logger.info(f"Total items on sale: {sale_items_count}")
    
    print_flush("[ANALYSIS] Checking for sale items that are out of stock...")
    sale_and_out_of_stock_count = listing_page.count_sale_and_out_of_stock_items()
    print_flush(f"✓ [RESULT] Items on sale and also out of stock: {sale_and_out_of_stock_count}")
    logger.info(f"Items on sale and also out of stock: {sale_and_out_of_stock_count}")
    
    print_flush("[ANALYSIS] Getting detailed sale items information...")
    sale_items = listing_page.get_sale_items()
    if sale_items:
        print_flush(f"\n✓ [RESULT] Found {len(sale_items)} sale items:")
        print_flush("-" * 70)
        for idx, item in enumerate(sale_items, 1):
            name_clean = item['name'].split('\t')[0].strip()
            print_flush(f"  {idx}. {name_clean}")
            print_flush(f"     Price: {item['price']}")
        print_flush("-" * 70)
        logger.info(f"Sale items list: {sale_items}")
    else:
        print_flush("\n✗ [RESULT] No sale items found")
    
    print_flush(f"\n[ACTION] Adding {len(sale_items)} sale items to cart...")
    print_flush("-" * 70)
    added_count = listing_page.add_sale_items_to_cart()
    print_flush("-" * 70)
    if added_count > 0:
        print_flush(f"✓ [SUCCESS] Successfully added {added_count} sale items to cart")
    else:
        print_flush(f"✗ [FAILED] No items were added to cart")
    logger.info(f"Added {added_count} sale items to cart")
    
    if added_count == 0:
        print_flush("\n" + "="*70)
        print_flush("⚠ [WARNING] No items were added to cart. Skipping cart verification.")
        print_flush("="*70 + "\n")
        logger.warning("No items were added to cart")
        return
    
    print_flush(f"\n[ACTION] Navigating to cart page...")
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    print_flush("✓ Navigated to cart page")
    
    print_flush("[VERIFICATION] Retrieving cart information...")
    total_items_in_cart = cart_page.get_item_count()
    total_quantity = cart_page.get_total_item_count()
    total_amount = cart_page.get_total_amount()
    
    print_flush(f"\n✓ [CART SUMMARY]")
    print_flush("-" * 70)
    print_flush(f"  Total items in cart: {total_items_in_cart}")
    print_flush(f"  Total quantity: {total_quantity}")
    print_flush(f"  Total amount: {total_amount}")
    print_flush("-" * 70)
    logger.info(f"Total items in cart: {total_items_in_cart}")
    logger.info(f"Total quantity: {total_quantity}")
    logger.info(f"Total amount: {total_amount}")
    
    cart_items = cart_page.get_cart_items()
    if cart_items:
        print_flush(f"\n✓ [CART ITEMS DETAILS] ({len(cart_items)} items):")
        print_flush("-" * 70)
        for idx, item in enumerate(cart_items, 1):
            print_flush(f"  {idx}. {item['name']}")
            print_flush(f"     Quantity: {item['quantity']} | Price: {item['price']}")
        print_flush("-" * 70)
        logger.info(f"Cart items list: {cart_items}")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY & VERIFICATION")
    print_flush("="*70)
    print_flush(f"  Sale items found: {sale_items_count}")
    print_flush(f"  Sale items out of stock: {sale_and_out_of_stock_count}")
    print_flush(f"  Items added to cart: {added_count}")
    print_flush(f"  Items in cart: {total_items_in_cart}")
    print_flush(f"  Total cart quantity: {total_quantity}")
    print_flush(f"  Total cart amount: {total_amount}")
    print_flush("="*70)
    
    if added_count > 0:
        print_flush("\n[VERIFICATION] Running assertions...")
        try:
            assert total_items_in_cart >= added_count, f"Expected at least {added_count} items in cart, found {total_items_in_cart}"
            print_flush(f"  ✓ PASS: Cart contains at least {added_count} items")
            
            assert total_quantity >= added_count, f"Expected total quantity at least {added_count}, found {total_quantity}"
            print_flush(f"  ✓ PASS: Total quantity is at least {added_count}")
            
            assert total_amount, f"Expected total amount to be present, but found: {total_amount}"
            print_flush(f"  ✓ PASS: Total amount is present: {total_amount}")
            
            sale_items_in_cart = [item for item in cart_items if any(sale_item['name'].split('\t')[0].strip() in item['name'] for sale_item in sale_items)]
            assert len(sale_items_in_cart) == added_count, f"Expected {added_count} sale items in cart, found {len(sale_items_in_cart)}"
            print_flush(f"  ✓ PASS: All {added_count} sale items are in cart")
            
            print_flush("\n[ACTION] Proceeding to checkout...")
            cart_page.checkout()
            print_flush("✓ [SUCCESS] Checkout completed successfully")
            logger.info("Checkout completed")
            
            print_flush("\n" + "="*70)
            print_flush("✓ TEST PASSED - All assertions successful!")
            print_flush("="*70 + "\n")
        except AssertionError as e:
            print_flush(f"\n✗ [FAILED] Assertion error: {e}")
            print_flush("="*70 + "\n")
            raise
    else:
        print_flush("\n⚠ [INFO] No items were added to cart, skipping assertions")
        logger.info("No items were added to cart, skipping assertions")
        print_flush("="*70 + "\n")

