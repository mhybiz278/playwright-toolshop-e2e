@catalogue @smoke
Feature: Catalogue API contract
  These run in a couple of seconds without a browser. If the products endpoint
  changed shape there is no point discovering it as "element not found" three
  layers up in a UI test.

  Scenario: The products endpoint returns a pagination envelope
    When I request page 1 of the products
    Then the response carries a pagination envelope

  Scenario: Every product carries the fields the catalogue renders
    When I request page 1 of the products
    Then every product has an id, a name and a price

  Scenario: No product is priced at or below zero
    When I request page 1 of the products
    Then every product costs more than zero
