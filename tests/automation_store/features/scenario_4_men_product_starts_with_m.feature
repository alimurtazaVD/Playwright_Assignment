Feature: Add Men Section Products Starting with 'M' to Cart
  As a user
  I want to add products from Men section whose name starts with 'M' to my cart
  So that I can purchase them

  @smoke @cross_browser
  Scenario: Add products starting with 'M' from Men section to cart
    Given I am logged into the automation test store
    When I navigate to the home page
    And I navigate to the Men section
    And I scroll down to load all products
    And I find products whose name starts with "M"
    And I add the first product starting with "M" to cart
    And I add the second product starting with "M" to cart
    And I navigate to the cart page
    Then I should see at least 2 items in the cart
    And the products in cart should start with "M"
    And both products starting with "M" should be verified

