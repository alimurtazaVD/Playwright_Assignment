Feature: Add Apparel and Shoes to Cart
  As a user
  I want to add T-shirts and shoes to my cart
  So that I can purchase multiple items

  @smoke @cross_browser
  Scenario: Add T-shirts and two highest priced shoes to cart
    Given I am logged into the automation test store
    When I navigate to the home page
    And I navigate to "APPAREL & ACCESSORIES" category
    And I navigate to "T-shirts" subcategory
    And I sort products by price low to high
    And I add the first 3 products to cart with quantity 1
    And I navigate back to home page
    And I navigate to "Apparel & accessories" category
    And I navigate to "Shoes" subcategory
    And I sort products by price high to low
    And I add the 2 highest priced shoes to cart with quantity 1
    And I navigate to the cart page
    Then I should see at least 5 items in the cart
    And the total quantity should be at least 5
    And the 2 shoes items should be present in the cart

