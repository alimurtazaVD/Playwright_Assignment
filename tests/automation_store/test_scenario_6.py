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
def test_scenario_6_currency_euro_delete_items(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 6: CURRENCY CHANGE TO EURO & DELETE ITEMS")
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
    
    print_flush("\n[STEP 6] Getting initial cart items...")
    initial_items = cart_page.get_cart_items()
    print_flush(f"[RESULT] Initial items in cart: {len(initial_items)}")
    if initial_items:
        print_flush("[RESULT] Initial cart items:")
        for idx, item in enumerate(initial_items, 1):
            print_flush(f"  {idx}. {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")
    
    print_flush("\n[STEP 7] Changing currency to Euro...")
    cart_page.change_currency_to_euro()
    print_flush("[PASS] Currency changed to Euro")
    
    print_flush("\n[STEP 8] Getting subtotal in Euro...")
    subtotal_euro = cart_page.get_subtotal_in_euro()
    print_flush(f"[RESULT] Subtotal in Euro: €{subtotal_euro:.2f}")
    print_flush(f"[RESULT] Subtotal threshold: €250.00")
    
    print_flush("\n[STEP 9] Checking if subtotal > 250 Euro...")
    if subtotal_euro > 250:
        print_flush(f"[RESULT] Subtotal ({subtotal_euro:.2f} Euro) is greater than 250 Euro")
        print_flush("[ACTION] Need to delete highest value items...")
        
        print_flush("\n[STEP 10] Getting cart items with totals...")
        items_with_totals = cart_page.get_cart_items_with_totals()
        print_flush(f"[RESULT] Found {len(items_with_totals)} items with totals:")
        for idx, item in enumerate(items_with_totals, 1):
            print_flush(f"  {idx}. {item['name']}")
            print_flush(f"     Unit Price: {item['unit_price']} | Total: {item['total']} | Value: €{item['total_value']:.2f}")
        
        print_flush("\n[STEP 11] Sorting items by total value (highest first)...")
        sorted_items = sorted(items_with_totals, key=lambda x: x['total_value'], reverse=True)
        print_flush("[RESULT] Items sorted by value (highest to lowest):")
        for idx, item in enumerate(sorted_items, 1):
            print_flush(f"  {idx}. {item['name']} - €{item['total_value']:.2f}")
        
        print_flush("\n[STEP 12] Deleting highest value items until total <= 250 Euro...")
        deleted_count = 0
        current_total = subtotal_euro
        
        while current_total > 250 and len(sorted_items) > 0:
            highest_item = sorted_items[0]
            print_flush(f"\n[ACTION] Current total: €{current_total:.2f}")
            print_flush(f"[ACTION] Deleting item: {highest_item['name']} (€{highest_item['total_value']:.2f})")
            
            deleted = cart_page.delete_item_by_index(highest_item['index'])
            if deleted:
                deleted_count += 1
                current_total -= highest_item['total_value']
                sorted_items.pop(0)
                print_flush(f"[PASS] Item deleted. New total: €{current_total:.2f}")
                
                if current_total <= 250:
                    print_flush(f"[SUCCESS] Total ({current_total:.2f} Euro) is now <= 250 Euro")
                    break
                
                print_flush("[ACTION] Refreshing cart items after deletion...")
                page.wait_for_timeout(2000)
                items_with_totals = cart_page.get_cart_items_with_totals()
                sorted_items = sorted(items_with_totals, key=lambda x: x['total_value'], reverse=True)
            else:
                print_flush(f"[FAILED] Failed to delete item: {highest_item['name']}")
                break
        
        print_flush(f"\n[RESULT] Deleted {deleted_count} item(s)")
    else:
        print_flush(f"[RESULT] Subtotal ({subtotal_euro:.2f} Euro) is already <= 250 Euro")
        print_flush("[INFO] No items need to be deleted")
    
    print_flush("\n[STEP 13] Getting final total amount in Euro...")
    final_total_euro = cart_page.get_total_amount_in_euro()
    if final_total_euro == 0:
        final_total_euro = cart_page.get_subtotal_in_euro()
    print_flush(f"[RESULT] Final total in Euro: €{final_total_euro:.2f}")
    print_flush(f"[RESULT] Target threshold: €250.00")
    print_flush(f"[RESULT] Difference from threshold: €{250 - final_total_euro:.2f}")
    
    print_flush("\n[STEP 14] Getting final cart items...")
    final_items = cart_page.get_cart_items()
    print_flush(f"[RESULT] Final items in cart: {len(final_items)}")
    if final_items:
        print_flush("[RESULT] Final cart items:")
        for idx, item in enumerate(final_items, 1):
            print_flush(f"  {idx}. {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")
    
    print_flush("\n[VERIFICATION] Running assertions...")
    
    print_flush(f"[CHECK] Verifying total amount <= 250 Euro...")
    print_flush(f"  - Current total: €{final_total_euro:.2f}")
    print_flush(f"  - Threshold: €250.00")
    print_flush(f"  - Condition: {final_total_euro:.2f} <= 250.00")
    
    assert final_total_euro <= 250, f"Expected total amount <= 250 Euro, but found: €{final_total_euro:.2f}"
    print_flush(f"[PASS] Total amount (€{final_total_euro:.2f}) is <= 250 Euro")
    print_flush(f"[PASS] Assertion successful!")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Currency: Changed to Euro (EUR)")
    print_flush(f"  Initial items in cart: {len(initial_items)}")
    print_flush(f"  Initial subtotal: €{subtotal_euro:.2f}")
    print_flush(f"  Subtotal > 250 Euro: {'Yes' if subtotal_euro > 250 else 'No'}")
    print_flush(f"  Items deleted: {deleted_count if subtotal_euro > 250 else 0}")
    print_flush(f"  Final items in cart: {len(final_items)}")
    print_flush(f"  Final subtotal: €{cart_page.get_subtotal_in_euro():.2f}")
    print_flush(f"  Final total in Euro: €{final_total_euro:.2f}")
    print_flush(f"  Target threshold: €250.00")
    print_flush(f"  Total <= 250 Euro: {'Yes' if final_total_euro <= 250 else 'No'}")
    print_flush(f"  Test Status: PASSED")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

