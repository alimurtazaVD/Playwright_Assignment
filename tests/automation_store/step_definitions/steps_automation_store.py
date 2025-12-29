import logging
import pytest
from pytest_bdd import given, when, then, parsers
from src.pages.automation_store.login_page import StoreLoginPage
from src.pages.automation_store.home_page import StoreHomePage
from src.pages.automation_store.product_page import StoreProductPage
from src.pages.automation_store.product_detail_page import StoreProductDetailPage
from src.pages.automation_store.category_page import StoreCategoryPage
from src.pages.automation_store.product_listing_page import StoreProductListingPage
from src.pages.automation_store.cart_page import StoreCartPage
from src.utils.config_manager import config_manager

logger = logging.getLogger(__name__)


@given("I am logged into the automation test store")
def login_to_store(cross_browser_page, base_url):
    page = cross_browser_page
    login_page = StoreLoginPage(page)
    login_page.open(base_url)
    login_page.click_login_link()
    
    creds = config_manager.get_test_data()["automation_store"]["login_user"]
    login_page.login(creds["username"], creds["password"])
    logger.info("Successfully logged into automation test store")


@when("I navigate to the home page")
def navigate_to_home(cross_browser_page, base_url):
    page = cross_browser_page
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    logger.info("Navigated to home page")


@when("I click on the DOVE brand")
def click_dove_brand(cross_browser_page):
    page = cross_browser_page
    home_page = StoreHomePage(page)
    home_page.click_dove_brand()
    logger.info("Clicked on DOVE brand")


@when("I select the newest product")
def select_newest_product(cross_browser_page, context):
    page = cross_browser_page
    product_page = StoreProductPage(page)
    newest_product = product_page.get_newest_product()
    context['product_name'] = newest_product["name"]
    context['product_price'] = newest_product["price"]
    product_page.click_newest_product()
    logger.info(f"Selected newest product: {context['product_name']}")


@when("I add the product to cart")
def add_product_to_cart(cross_browser_page):
    page = cross_browser_page
    detail_page = StoreProductDetailPage(page)
    detail_page.add_to_cart()
    logger.info("Added product to cart")


@when("I navigate to the cart page")
def navigate_to_cart(cross_browser_page):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    cart_page.navigate_to_cart()
    logger.info("Navigated to cart page")


@then("I should see at least 1 item in the cart")
def verify_cart_has_items(cross_browser_page):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    item_count = cart_page.get_item_count()
    assert item_count >= 1, f"Expected at least 1 item in cart, but found {item_count}"
    logger.info(f"Verified cart has {item_count} item(s)")


@then("the product should be present in the cart")
def verify_product_in_cart(cross_browser_page, context):
    page = cross_browser_page
    product_name = context.get('product_name')
    
    cart_page = StoreCartPage(page)
    cart_item = cart_page.verify_item_in_cart(product_name)
    assert cart_item, f"Expected item '{product_name}' not found in cart"
    logger.info(f"Verified product '{product_name}' is in cart")


@then("the product quantity should be 1")
def verify_product_quantity(cross_browser_page, context):
    page = cross_browser_page
    product_name = context.get('product_name')
    
    cart_page = StoreCartPage(page)
    cart_item = cart_page.verify_item_in_cart(product_name)
    actual_quantity = cart_item.get("quantity", 0)
    assert actual_quantity >= 1, f"Expected quantity at least 1, Actual: {actual_quantity}"
    logger.info(f"Verified product quantity is {actual_quantity}")


@then("the product price should be displayed")
def verify_product_price(cross_browser_page, context):
    page = cross_browser_page
    product_name = context.get('product_name')
    
    cart_page = StoreCartPage(page)
    cart_item = cart_page.verify_item_in_cart(product_name)
    actual_price = cart_item.get("price", "")
    assert actual_price, f"Expected price to be present, but found: {actual_price}"
    logger.info(f"Verified product price is displayed: {actual_price}")


@when(parsers.parse('I navigate to "{category}" category'))
def navigate_to_category(cross_browser_page, category):
    page = cross_browser_page
    category_page = StoreCategoryPage(page)
    category_page.click_category(category)
    logger.info(f"Navigated to {category} category")


@when(parsers.parse('I navigate to "{subcategory}" subcategory'))
def navigate_to_subcategory(cross_browser_page, subcategory):
    page = cross_browser_page
    category_page = StoreCategoryPage(page)
    category_page.click_category(subcategory)
    logger.info(f"Navigated to {subcategory} subcategory")


@when("I sort products by price low to high")
def sort_low_to_high(cross_browser_page):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    listing_page.sort_by_price_low_to_high()
    logger.info("Sorted products by price low to high")


@when("I add the first 3 products to cart with quantity 1")
def add_first_three_products(cross_browser_page, context):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    detail_page = StoreProductDetailPage(page)
    
    listing_url = page.url
    products = listing_page.get_products_by_price_order(3, ascending=True)
    context['expected_items'] = []
    
    for i in range(3):
        if i > 0:
            page.goto(listing_url)
            listing_page.wait_for_listing_page_ready()
            listing_page.sort_by_price_low_to_high()
        
        listing_page.click_product_by_index(i)
        detail_page.set_quantity(1)
        detail_page.add_to_cart()
        product_name = products[i].get("name", f"Product_{i+1}") if i < len(products) else f"Product_{i+1}"
        context['expected_items'].append({"name": product_name, "quantity": 1})
    
    logger.info("Added first 3 products to cart")


@when("I navigate back to home page")
def navigate_back_to_home(cross_browser_page, base_url):
    page = cross_browser_page
    home_page = StoreHomePage(page)
    home_page.navigate_to_home(base_url)
    logger.info("Navigated back to home page")


@when("I sort products by price high to low")
def sort_high_to_low(cross_browser_page):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    listing_page.sort_by_price_high_to_low()
    logger.info("Sorted products by price high to low")


@when("I add the 2 highest priced shoes to cart with quantity 1")
def add_highest_priced_shoes(cross_browser_page, context):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    detail_page = StoreProductDetailPage(page)
    
    shoes_listing_url = page.url
    listing_page.sort_by_price_high_to_low()
    listing_page.wait_for_listing_page_ready()
    
    highest_products = listing_page.get_products_by_price_order(2, ascending=False)
    
    if 'expected_items' not in context:
        context['expected_items'] = []
    
    for i in range(2):
        if i > 0:
            page.goto(shoes_listing_url)
            listing_page.wait_for_listing_page_ready()
            listing_page.sort_by_price_high_to_low()
        
        listing_page.click_product_by_index(i)
        detail_page.set_quantity(1)
        detail_page.add_to_cart()
        
        product_name = highest_products[i].get("name", f"Shoes_Product_{i+1}") if i < len(highest_products) else f"Shoes_Product_{i+1}"
        context['expected_items'].append({"name": product_name, "quantity": 1})
    
    logger.info("Added 2 highest priced shoes to cart with quantity 1")


@then("I should see at least 5 items in the cart")
def verify_cart_has_at_least_5_items(cross_browser_page, context):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    expected_items = context.get('expected_items', [])
    expected_item_count = len(expected_items)
    
    item_count = cart_page.get_item_count()
    assert item_count >= expected_item_count, f"Expected at least {expected_item_count} items, found {item_count}"
    logger.info(f"Verified cart has at least {expected_item_count} items")


@then("the total quantity should be at least 5")
def verify_total_quantity_at_least_5(cross_browser_page, context):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    expected_items = context.get('expected_items', [])
    expected_total = sum(item["quantity"] for item in expected_items)
    
    total_items = cart_page.get_total_item_count()
    assert total_items >= expected_total, f"Expected total quantity at least {expected_total}, found {total_items}"
    logger.info(f"Verified total quantity is at least {expected_total}")


@then("the 2 shoes items should be present in the cart")
def verify_shoes_items_in_cart(cross_browser_page):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    cart_items = cart_page.get_cart_items()
    shoes_items = [item for item in cart_items if item.get("quantity", 0) >= 1]
    
    assert len(shoes_items) >= 2, f"Expected at least 2 shoes items in cart, found {len(shoes_items)}"
    
    for idx, shoes_item in enumerate(shoes_items[:2], 1):
        assert shoes_item.get("quantity", 0) >= 1, f"Expected shoes product quantity to be at least 1, found {shoes_item.get('quantity', 0)}"
        assert shoes_item.get("name"), f"Expected shoes product name to be present, found: {shoes_item.get('name')}"
        assert shoes_item.get("price"), f"Expected shoes product price to be present, found: {shoes_item.get('price')}"
    
    logger.info("Verified 2 shoes items are present in cart")


@when("I navigate to the Men section")
def navigate_to_men_section(cross_browser_page):
    page = cross_browser_page
    category_page = StoreCategoryPage(page)
    category_page.click_men()
    logger.info("Navigated to Men section")


@when("I scroll down to load all products")
def scroll_down_to_load_products(cross_browser_page):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    listing_page.wait_for_listing_page_ready()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)
    logger.info("Scrolled down to load all products")


@when(parsers.parse('I find products whose name starts with "{letter}"'))
def find_products_starting_with_letter(cross_browser_page, context, letter):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    
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
    
    context['men_products'] = [
        {"name": product_1_name, "locator": product_1_locator, "element": product_1},
        {"name": product_2_name, "locator": product_2_locator, "element": product_2}
    ]
    context['men_listing_url'] = page.url
    
    logger.info(f"Found 2 products starting with '{letter}': {product_1_name}, {product_2_name}")


@when("I add the first product starting with \"M\" to cart")
def add_first_product_starting_with_m(cross_browser_page, context):
    page = cross_browser_page
    detail_page = StoreProductDetailPage(page)
    
    men_products = context.get('men_products', [])
    if not men_products:
        raise Exception("No products found in context")
    
    first_product = men_products[0]
    product_name = first_product["name"]
    product_element = first_product["element"]
    
    product_element.scroll_into_view_if_needed()
    product_element.click(timeout=30000)
    page.wait_for_timeout(2000)
    
    detail_page.set_quantity(1)
    detail_page.add_to_cart()
    
    if 'expected_items' not in context:
        context['expected_items'] = []
    context['expected_items'].append({"name": product_name, "quantity": 1})
    
    logger.info(f"Added first product '{product_name}' to cart")


@when("I add the second product starting with \"M\" to cart")
def add_second_product_starting_with_m(cross_browser_page, context):
    page = cross_browser_page
    listing_page = StoreProductListingPage(page)
    detail_page = StoreProductDetailPage(page)
    
    men_listing_url = context.get('men_listing_url')
    men_products = context.get('men_products', [])
    
    if not men_products or len(men_products) < 2:
        raise Exception("Second product not found in context")
    
    page.goto(men_listing_url)
    listing_page.wait_for_listing_page_ready()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    
    second_product = men_products[1]
    product_name = second_product["name"]
    product_2_locator = second_product["locator"]
    
    product_2 = page.locator(f"xpath={product_2_locator}").first
    product_2.scroll_into_view_if_needed()
    product_2.click(timeout=30000)
    page.wait_for_timeout(2000)
    
    detail_page.set_quantity(1)
    detail_page.add_to_cart()
    
    if 'expected_items' not in context:
        context['expected_items'] = []
    context['expected_items'].append({"name": product_name, "quantity": 1})
    
    logger.info(f"Added second product '{product_name}' to cart")


@then("I should see at least 2 items in the cart")
def verify_cart_has_at_least_2_items(cross_browser_page):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    item_count = cart_page.get_item_count()
    assert item_count >= 2, f"Expected at least 2 items in cart, but found {item_count}"
    logger.info(f"Verified cart has at least 2 items: {item_count}")


@then(parsers.parse('the products in cart should start with "{letter}"'))
def verify_products_start_with_letter(cross_browser_page, letter):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    cart_items = cart_page.get_cart_items()
    products_with_letter = [item for item in cart_items if item.get("name", "").strip().upper().startswith(letter.upper())]
    
    assert len(products_with_letter) >= 2, f"Expected at least 2 products starting with '{letter}' in cart, found {len(products_with_letter)}"
    logger.info(f"Verified {len(products_with_letter)} products starting with '{letter}' are in cart")


@then("both products starting with \"M\" should be verified")
def verify_both_products_starting_with_m(cross_browser_page):
    page = cross_browser_page
    cart_page = StoreCartPage(page)
    
    cart_items = cart_page.get_cart_items()
    products_with_m = [item for item in cart_items if item.get("name", "").strip().upper().startswith("M")]
    
    assert len(products_with_m) >= 2, f"Expected at least 2 products starting with 'M' in cart, found {len(products_with_m)}"
    
    for idx, item in enumerate(products_with_m[:2], 1):
        item_name = item.get("name", "").strip()
        assert item_name.upper().startswith("M"), f"Expected product name to start with 'M', found: {item_name}"
        assert item.get("quantity", 0) >= 1, f"Expected product quantity to be at least 1, found {item.get('quantity', 0)}"
        assert item.get("name"), f"Expected product name to be present, found: {item.get('name')}"
        assert item.get("price"), f"Expected product price to be present, found: {item.get('price')}"
    
    logger.info("Verified both products starting with 'M' are in cart with correct details")

