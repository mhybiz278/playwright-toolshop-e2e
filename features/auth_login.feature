@auth @regression
Feature: Signing in
  The application locks a customer out after three failed attempts. That is
  worth asserting deliberately — and worth knowing about before it takes a
  whole suite down by accident.

  Scenario: A customer signs in with valid credentials
    Given I have a registered account
    When I sign in with my own password
    Then I am signed in

  Scenario: The wrong password is refused
    Given I have a registered account
    When I sign in with the password "definitely-not-it"
    Then I am not signed in

  Scenario: Three failed attempts lock the account
    Given I have a registered account
    When I sign in with a wrong password 3 times
    Then the account is locked
