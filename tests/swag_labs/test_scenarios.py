"""
Swag Labs Scenarios
"""

import logging
import pytest
from src.pages.swag_labs.login_page import SwagLoginPage
from src.pages.swag_labs.inventory_page import SwagInventoryPage
from src.pages.swag_labs.cart_page import SwagCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_scenario_1_invalid_password(page, base_url):
    # 1 Go to url, 2 valid username, 3 invalid password, 4 click sign in, assert error
    login = SwagLoginPage(page)
    login.open(base_url)
    creds = config_manager.get_test_data()["users"]
    login.login(creds["standard_user"]["username"], "wrong_password")
    error_visible = login.is_error_visible()
    logger.info(f"[Scenario 1] Error visible → Expected: True | Actual: {error_visible}")
    assert error_visible, f"Expected error to be visible: True, Actual: {error_visible}"
    expected_msg = config_manager.get_test_data()["login_messages"]["invalid_credentials"]
    actual_msg = (login.get_error_text() or "").strip()
    logger.info(f"[Scenario 1] Error message → Expected: {expected_msg} | Actual: {actual_msg}")
    assert actual_msg == expected_msg, (
        f"Invalid-credentials message mismatch.\nExpected: {expected_msg}\nActual:   {actual_msg}"
    )


@pytest.mark.smoke
def test_scenario_2_valid_login(page, base_url):
    login = SwagLoginPage(page)
    login.open(base_url)
    creds = config_manager.get_test_data()["users"]
    login.login(creds["standard_user"]["username"], creds["standard_user"]["password"])
    page.wait_for_url("**/inventory.html")
    expected_fragment = "inventory.html"
    actual_url = page.url
    logger.info(f"[Scenario 2] URL → Expected contains: {expected_fragment} | Actual: {actual_url}")
    assert expected_fragment in actual_url, (
        f"Expected URL to contain: {expected_fragment}, Actual URL: {actual_url}"
    )
    inv = SwagInventoryPage(page)
    expected_title = "products"
    actual_title = (inv.get_title_text() or "").strip().lower()
    logger.info(f"[Scenario 2] Title → Expected: {expected_title} | Actual: {actual_title}")
    assert actual_title == expected_title, (
        f"Inventory page title mismatch. Expected: {expected_title}, Actual: {actual_title}"
    )


@pytest.mark.regression
def test_scenario_3_sort_and_cart(page, base_url):
    # Login
    login = SwagLoginPage(page)
    login.open(base_url)
    creds = config_manager.get_test_data()["users"]
    login.login(creds["standard_user"]["username"], creds["standard_user"]["password"]) 
    page.wait_for_url("**/inventory.html")
    inv = SwagInventoryPage(page)

    # Sort low to high and assert
    inv.sort_low_to_high()
    prices = inv.get_all_prices()
    expected_sorted = sorted(prices)
    logger.info(f"[Scenario 3] Prices sorted check → Expected: {expected_sorted} | Actual: {prices}")
    assert prices == expected_sorted, (
        f"Prices should be sorted low→high.\nExpected: {expected_sorted}\nActual:   {prices}"
    )

    # Add two lowest items
    lowest_selected = inv.add_lowest_n_items(2)
    logger.info(f"[Scenario 3] Lowest two selected → {lowest_selected}")

    # Go to cart
    inv.open_cart()
    cart = SwagCartPage(page)

    # Assert quantities and totals
    item_count = cart.get_item_count()
    logger.info(f"[Scenario 3] Cart item count → Expected: 2 | Actual: {item_count}")
    assert item_count == 2, f"Cart item count mismatch. Expected: 2, Actual: {item_count}"
    quantities = cart.get_quantities()
    all_one = all(q == 1 for q in quantities)
    logger.info(f"[Scenario 3] Cart quantities → Expected: all 1 | Actual: {quantities}")
    assert all_one, f"Each cart quantity should be 1. Actual quantities: {quantities}"
    cart_prices = cart.get_item_prices()
    expected_prices = sorted(lowest_selected)
    actual_selected = sorted(cart_prices)[:2]
    logger.info(
        f"[Scenario 3] Cart prices → Expected (two lowest): {expected_prices} | Actual (first two): {actual_selected}"
    )
    assert actual_selected == expected_prices, (
        f"Cart prices mismatch.\nExpected (two lowest added): {expected_prices}\nActual (first two in cart): {actual_selected}"
    )


@pytest.mark.regression
def test_scenario_4_multiple_flow(page, base_url):
    """Scenario 4: Multiple Test
    1. Go to dashboard
    2. Open menu option (from the left side)
    3. Select About Option
    4. Assert the text on the page "Build apps users love with AI-driven quality"
    """

    # 1. Login and reach inventory
    login = SwagLoginPage(page)
    login.open(base_url)

    creds = config_manager.get_test_data()["users"]
    login.login(
        creds["standard_user"]["username"],
        creds["standard_user"]["password"]
    )

    page.wait_for_url("**/inventory.html")

    # 2. Open menu
    inv = SwagInventoryPage(page)
    inv.open_menu()

    # 3. Click About
    inv.click_about()

    # 4. Validate About page content (CI-safe)
    expected_text = "Build apps users love with AI-driven quality"

    # Ensure navigation happened
    page.wait_for_url("**saucelabs.com**", timeout=30000)

    # Wait for meaningful content instead of networkidle
    about_text = page.locator(f"text={expected_text}")

    about_text.wait_for(state="visible", timeout=30000)

    assert about_text.is_visible(), (
        f"[Scenario 4] Expected text not visible: '{expected_text}'"
    )

    actual_text = about_text.text_content()
    logger.info(
        f"[Scenario 4] Assertion passed → Expected: '{expected_text}' | Actual: '{actual_text}'"
    )

    logger.info("[Scenario 4] Successfully completed multiple flow test")


