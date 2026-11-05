@catalogue @smoke
Feature: Searching the catalogue
  A customer who cannot find a product cannot buy it, so search is on the
  pre-merge gate rather than the nightly run.

  Scenario: Finding a product by name
    Given the shop is open
    When I search for "Pliers"
    Then every result mentions "Pliers"

  Scenario: Searching is not case sensitive
    Given the shop is open
    When I search for "pliers"
    Then at least one product is listed

  Scenario: A search that matches nothing says so
    Given the shop is open
    When I search for "zzzznotaproduct"
    Then no products are listed
