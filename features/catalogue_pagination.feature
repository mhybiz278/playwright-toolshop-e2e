@catalogue @regression
Feature: Paging through the catalogue
  Off-by-one errors in offset/limit surface as one record repeated across a
  page boundary, never as an obvious failure.

  Scenario: Page two holds different products
    Given the shop is open
    When I go to the next page
    Then the products are not the ones from the first page

  Scenario: Paging back returns the original products
    Given the shop is open
    When I go to the next page
    And I go back to the previous page
    Then the products are the ones from the first page

  Scenario: No product appears on two consecutive pages
    Given the shop is open
    When I go to the next page
    Then no product from the first page is listed again
