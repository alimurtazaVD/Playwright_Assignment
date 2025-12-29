Feature: Add DOVE Brand Newest Product to Cart
  As a user
  I want to add the newest DOVE product to my cart
  So that I can purchase it

  @smoke @cross_browser
  Scenario: Add newest DOVE product to cart and verify
    Given I am logged into the automation test store
    When I navigate to the home page
    And I click on the DOVE brand
    And I select the newest product
    And I add the product to cart
    And I navigate to the cart page
    Then I should see at least 1 item in the cart
    And the product should be present in the cart
    And the product quantity should be 1
    And the product price should be displayed

