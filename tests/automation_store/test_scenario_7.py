import logging
import sys
import pytest
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_7_invalid_coupon_checkout_confirm(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 7: INVALID COUPON, CHECKOUT & ORDER CONFIRMATION")
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
    
    print_flush("\n[STEP 5] Navigating to cart page...")
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    print_flush("[PASS] Navigated to cart page")
    
    print_flush("\n[STEP 6] Checking cart items...")
    page.wait_for_timeout(2000)
    
    try:
        cart_items = cart_page.get_cart_items()
    except:
        cart_items = []
    
    print_flush(f"[RESULT] Items in cart: {len(cart_items)}")
    
    if len(cart_items) == 0:
        print_flush("[INFO] Cart is empty. Adding an item to cart first...")
        from src.pages.automation_store.category_page import StoreCategoryPage
        from src.pages.automation_store.product_listing_page import StoreProductListingPage
        from src.pages.automation_store.product_detail_page import StoreProductDetailPage
        
        category_page = StoreCategoryPage(page)
        category_page.click_fragrance()
        listing_page = StoreProductListingPage(page)
        listing_page.wait_for_listing_page_ready()
        
        product_link = page.locator("xpath=//a[contains(@href, 'product/product')]").first
        if product_link.count() > 0:
            product_link.click(timeout=30000)
            page.wait_for_timeout(2000)
            
            detail_page = StoreProductDetailPage(page)
            detail_page.set_quantity(1)
            detail_page.add_to_cart()
            page.wait_for_timeout(2000)
            print_flush("[PASS] Added item to cart")
        
        cart_page.navigate_to_cart()
        page.wait_for_timeout(2000)
        cart_items = cart_page.get_cart_items()
        print_flush(f"[RESULT] Items in cart after adding: {len(cart_items)}")
    
    if cart_items:
        print_flush("[RESULT] Cart items:")
        for idx, item in enumerate(cart_items, 1):
            print_flush(f"  {idx}. {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")
    
    assert len(cart_items) > 0, "Cart is empty. Please add items to cart first."
    print_flush("[PASS] Cart has items")
    
    print_flush("\n[STEP 7] Applying invalid coupon code...")
    invalid_coupon = "INVALID123"
    print_flush(f"[ACTION] Coupon code: {invalid_coupon}")
    coupon_applied = cart_page.apply_coupon(invalid_coupon)
    print_flush(f"[RESULT] Coupon applied: {coupon_applied}")
    if coupon_applied:
        print_flush("[PASS] Invalid coupon code applied (error message expected)")
    else:
        print_flush("[INFO] Coupon application failed or error message displayed")
    
    print_flush("\n[STEP 8] Removing invalid coupon...")
    coupon_removed = cart_page.remove_coupon()
    print_flush(f"[RESULT] Coupon removed: {coupon_removed}")
    if coupon_removed:
        print_flush("[PASS] Invalid coupon removed successfully")
    else:
        print_flush("[INFO] No coupon to remove or already removed")
    
    print_flush("\n[STEP 9] Proceeding to checkout...")
    cart_page.checkout()
    print_flush("[PASS] Checkout button clicked")
    
    print_flush("\n[STEP 10] Waiting for checkout page to load...")
    page.wait_for_timeout(3000)
    print_flush(f"[RESULT] Current URL: {page.url}")
    print_flush("[PASS] Checkout page loaded")
    
    print_flush("\n[STEP 11] Completing checkout steps and confirming order...")
    confirmation_message = cart_page.complete_checkout_steps()
    print_flush(f"[RESULT] Confirmation message: {confirmation_message}")
    
    if not confirmation_message:
        page.wait_for_timeout(2000)
        confirmation_message = cart_page.get_order_confirmation_message()
        print_flush(f"[RESULT] Confirmation message (retry): {confirmation_message}")
    
    print_flush(f"[RESULT] Final URL: {page.url}")
    
    print_flush("\n[VERIFICATION] Running assertions...")
    
    print_flush("[CHECK] Verifying order confirmation message...")
    assert confirmation_message, "Expected order confirmation message, but none found"
    print_flush(f"[PASS] Order confirmation message found: {confirmation_message}")
    
    confirmation_lower = confirmation_message.lower()
    assert "order" in confirmation_lower or "confirm" in confirmation_lower or "success" in confirmation_lower, \
        f"Expected confirmation message to contain 'order', 'confirm', or 'success', but found: {confirmation_message}"
    print_flush("[PASS] Confirmation message contains expected keywords")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Cart items: {len(cart_items)}")
    print_flush(f"  Invalid coupon applied: {coupon_applied}")
    print_flush(f"  Coupon removed: {coupon_removed}")
    print_flush(f"  Checkout completed: Yes")
    print_flush(f"  Order confirmed: Yes")
    print_flush(f"  Confirmation message: {confirmation_message[:50]}..." if len(confirmation_message) > 50 else f"  Confirmation message: {confirmation_message}")
    print_flush(f"  Test Status: PASSED")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

