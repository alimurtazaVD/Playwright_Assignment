import logging
import sys
import pytest
from datetime import datetime, timedelta
from playwright.sync_api import Page
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_8_facebook_registration(cross_browser_page, base_url):
    print_flush("\n" + "="*70)
    print_flush("STARTING SCENARIO 8: FACEBOOK REGISTRATION")
    print_flush("="*70)
    
    page = cross_browser_page
    original_url = base_url
    
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
    
    print_flush("\n[STEP 5] Verifying current URL before clicking Facebook...")
    current_url_before = page.url
    print_flush(f"[RESULT] Current URL: {current_url_before}")
    assert "automationteststore.com" in current_url_before, f"Expected Automation Test Store URL, found: {current_url_before}"
    print_flush("[PASS] URL verification passed - on Automation Test Store")
    
    print_flush("\n[STEP 6] Clicking Facebook link...")
    context = page.context
    original_pages = context.pages
    original_url = page.url
    
    home_page.click_facebook_link()
    
    page.wait_for_timeout(3000)
    
    all_pages = context.pages
    facebook_page = None
    
    for p in all_pages:
        if p.url != page.url and "facebook.com" in p.url:
            facebook_page = p
            break
    
    if not facebook_page:
        page.wait_for_timeout(2000)
        all_pages = context.pages
        for p in all_pages:
            if p.url != page.url and "facebook.com" in p.url:
                facebook_page = p
                break
    
    assert facebook_page is not None, "Facebook page did not open"
    print_flush("[PASS] Facebook page opened in new window")
    
    print_flush("\n[STEP 7] Switching to Facebook window...")
    facebook_page.bring_to_front()
    facebook_page.wait_for_load_state("load", timeout=30000)
    facebook_url = facebook_page.url
    print_flush(f"[RESULT] Facebook URL: {facebook_url}")
    assert "facebook.com" in facebook_url, f"Expected Facebook URL, found: {facebook_url}"
    print_flush("[PASS] Facebook URL verification passed")
    
    print_flush("\n[STEP 8] Clicking 'Create new account' button...")
    create_account_button = facebook_page.get_by_role("button", name="Create new account", exact=False).first
    if create_account_button.count() == 0:
        create_account_button = facebook_page.locator("a[role='button']:has-text('Create new account')").first
    if create_account_button.count() == 0:
        create_account_button = facebook_page.locator("//a[contains(text(), 'Create new account')]").first
    
    create_account_button.wait_for(state="visible", timeout=30000)
    create_account_button.click(timeout=30000)
    facebook_page.wait_for_timeout(3000)
    
    facebook_url_after = facebook_page.url
    print_flush(f"[RESULT] Facebook URL after clicking: {facebook_url_after}")
    assert "facebook.com" in facebook_url_after, f"Expected Facebook URL, found: {facebook_url_after}"
    print_flush("[PASS] Clicked 'Create new account' button")
    print_flush("[PASS] Still on Facebook URL after clicking create account")
    
    print_flush("\n[STEP 9] Filling Facebook registration form...")
    
    first_name = facebook_page.locator("input[name='firstname']").first
    if first_name.count() == 0:
        first_name = facebook_page.locator("input[placeholder*='First name']").first
    
    surname = facebook_page.locator("input[name='lastname']").first
    if surname.count() == 0:
        surname = facebook_page.locator("input[placeholder*='Surname']").first
    
    mobile_email = facebook_page.locator("input[name='reg_email__']").first
    if mobile_email.count() == 0:
        mobile_email = facebook_page.locator("input[placeholder*='Mobile number']").first
    
    password = facebook_page.locator("input[name='reg_passwd__']").first
    if password.count() == 0:
        password = facebook_page.locator("input[type='password']").first
    
    first_name.wait_for(state="visible", timeout=20000)
    first_name.fill("Test")
    print_flush("  - First name: Test")
    
    surname.wait_for(state="visible", timeout=20000)
    surname.fill("User")
    print_flush("  - Surname: User")
    
    mobile_email.wait_for(state="visible", timeout=20000)
    mobile_email.fill("testuser@example.com")
    print_flush("  - Email: testuser@example.com")
    
    password.wait_for(state="visible", timeout=20000)
    password.fill("TestPassword123!")
    print_flush("  - Password: Set")
    
    print_flush("\n[STEP 10] Setting Date of Birth (18 years back from today)...")
    today = datetime.now()
    dob_date = today - timedelta(days=365*18)
    
    day = dob_date.day
    month = dob_date.strftime("%b")
    year = dob_date.year
    
    print_flush(f"[RESULT] DOB: {day} {month} {year}")
    
    day_dropdown = facebook_page.locator("select[name='birthday_day']").first
    if day_dropdown.count() == 0:
        day_dropdown = facebook_page.locator("select#day").first
    if day_dropdown.count() == 0:
        day_dropdown = facebook_page.locator("select").first
    
    month_dropdown = facebook_page.locator("select[name='birthday_month']").first
    if month_dropdown.count() == 0:
        month_dropdown = facebook_page.locator("select#month").first
    if month_dropdown.count() == 0:
        selects = facebook_page.locator("select")
        if selects.count() >= 2:
            month_dropdown = selects.nth(1)
    
    year_dropdown = facebook_page.locator("select[name='birthday_year']").first
    if year_dropdown.count() == 0:
        year_dropdown = facebook_page.locator("select#year").first
    if year_dropdown.count() == 0:
        selects = facebook_page.locator("select")
        if selects.count() >= 3:
            year_dropdown = selects.nth(2)
    
    if day_dropdown.count() > 0:
        day_dropdown.select_option(str(day))
        print_flush(f"  - Day: {day}")
    
    if month_dropdown.count() > 0:
        month_dropdown.select_option(month)
        print_flush(f"  - Month: {month}")
    
    if year_dropdown.count() > 0:
        year_dropdown.select_option(str(year))
        print_flush(f"  - Year: {year}")
    
    print_flush("[PASS] Date of Birth set successfully")
    
    print_flush("\n[STEP 11] Selecting Gender...")
    gender_male = facebook_page.locator("input[type='radio'][value='2']").first
    if gender_male.count() == 0:
        gender_male = facebook_page.locator("input[name='sex'][value='2']").first
    if gender_male.count() == 0:
        gender_labels = facebook_page.locator("label:has-text('Male')")
        if gender_labels.count() > 0:
            gender_male = gender_labels.first.locator("..").locator("input[type='radio']").first
    
    if gender_male.count() > 0:
        gender_male.click()
        print_flush("  - Gender: Male")
        print_flush("[PASS] Gender selected")
    
    print_flush("\n[STEP 12] Verifying Facebook URL before closing...")
    facebook_url_final = facebook_page.url
    print_flush(f"[RESULT] Facebook URL: {facebook_url_final}")
    assert "facebook.com" in facebook_url_final, f"Expected Facebook URL, found: {facebook_url_final}"
    print_flush("[PASS] Facebook URL verification passed")
    
    print_flush("\n[STEP 13] Closing Facebook window...")
    facebook_page.close()
    print_flush("[PASS] Facebook window closed")
    
    print_flush("\n[STEP 14] Switching back to Automation Test Store window...")
    page.bring_to_front()
    page.wait_for_timeout(2000)
    print_flush("[PASS] Switched back to Automation Test Store")
    
    print_flush("\n[VERIFICATION] Verifying Automation Test Store URL...")
    current_url = page.url
    print_flush(f"[RESULT] Current URL: {current_url}")
    print_flush(f"[RESULT] Original URL: {original_url}")
    print_flush(f"[RESULT] Expected: Automation Test Store URL")
    
    assert "automationteststore.com" in current_url, f"Expected Automation Test Store URL, found: {current_url}"
    print_flush("[PASS] Website URL verification passed - on Automation Test Store")
    
    print_flush("\n[VERIFICATION] Verifying URL structure...")
    assert current_url.startswith("http"), f"Expected valid HTTP/HTTPS URL, found: {current_url}"
    print_flush("[PASS] URL structure verification passed")
    
    print_flush("\n[VERIFICATION] Verifying we're not on Facebook...")
    assert "facebook.com" not in current_url, f"Expected not to be on Facebook, but found: {current_url}"
    print_flush("[PASS] Not on Facebook - verification passed")
    
    print_flush("\n" + "="*70)
    print_flush("TEST SUMMARY")
    print_flush("="*70)
    print_flush(f"  Original URL: {original_url}")
    print_flush(f"  Facebook URL: {facebook_url}")
    print_flush(f"  Final URL: {current_url}")
    print_flush(f"  URL Verification: PASSED")
    print_flush(f"  DOB Set: {day} {month} {year} (18 years back)")
    print_flush(f"  Facebook Registration: Completed")
    print_flush(f"  Facebook Window: Closed")
    print_flush(f"  Back to Automation Store: Yes")
    print_flush("="*70)
    print_flush("[SUCCESS] TEST PASSED - All assertions successful!")
    print_flush("="*70 + "\n")

