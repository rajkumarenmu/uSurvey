# -*- coding: utf-8 -*-
from lettuce import *
from page_objects import *
from random import randint
from survey.features.page_objects.households import NewHouseholdPage, HouseholdsListPage
from survey.features.page_objects.root import HomePage
from survey.models_file import *
from rapidsms.contrib.locations.models import *
from django.template.defaultfilters import slugify

@step(u'And I visit new household page')
def and_i_visit_new_household_page(step):
    world.page = NewHouseholdPage(world.browser)
    world.page.visit()

@step(u'And I see all households fields are present')
def and_i_see_all_households_fields_are_present(step):
    world.page.valid_page()

@step(u'And I have an investigator in that location')
def and_i_have_an_investigator_in_that_location(step):
    kampala_county = Location.objects.get(name="Kampala County")
    investigator = Investigator.objects.create(name="Investigator name", location=kampala_county)

@step(u'Then I should see that the household is created')
def then_i_should_see_that_the_household_is_created(step):
    world.page.validate_household_created()

@step(u'And I click No to has children')
def and_i_click_no_to_has_children(step):
    world.page.has_children('False')

@step(u'Then I should see children number fields disabled')
def then_i_should_see_children_number_fields_disabled(step):
    world.page.are_children_fields_disabled()

@step(u'And No below 5 is also checked')
def and_no_below_5_is_also_checked(step):
    world.page.is_no_below_5_checked()

@step(u'And checking below 5 to yes does not work')
def and_checking_below_5_to_yes_does_not_work(step):
    world.page.cannot_say_yes_to_below_5()

@step(u'And Now If I click to Yes to has children')
def and_now_if_i_click_to_yes_to_has_children(step):
    world.page.has_children('True')

@step(u'Then all children number fields are enabled back')
def then_all_children_number_fields_are_enabled_back(step):
    world.page.are_children_fields_disabled(is_disabled = False)

@step(u'And I click No to has below 5')
def and_i_click_no_to_has_below_5(step):
    world.page.has_children_below_5('False')

@step(u'Then I should see below 5 number fields disabled')
def then_i_should_see_below_5_number_fields_disabled(step):
    world.page.are_children_below_5_fields_disabled(is_disabled=True)

@step(u'And Now If I click Yes to below 5')
def and_now_if_i_click_yes_to_below_5(step):
    world.page.has_children_below_5('True')

@step(u'Then below 5 number fields are enabled back')
def then_below_5_number_fields_are_enabled_back(step):
    world.page.are_children_below_5_fields_disabled(is_disabled=False)

@step(u'And I click No to has women')
def and_i_click_no_to_has_women(step):
    world.page.has_women('False')

@step(u'Then I should see has women number fields disabled')
def then_i_should_see_has_women_number_fields_disabled(step):
    world.page.are_women_fields_disabled()

@step(u'And Now If I click Yes to has women')
def and_now_if_i_click_yes_to_has_women(step):
    world.page.has_women('True')

@step(u'Then has women number fields are enabled back')
def then_has_women_number_fields_are_enabled_back(step):
    world.page.are_women_fields_disabled(is_disabled=False)

@step(u'And I fill in number_of_females lower than sum of 15_19 and 20_49')
def and_i_fill_in_number_of_females_lower_than_sum_of_15_19_and_20_49(step):
    world.page.fill_in_number_of_females_lower_than_sum_of_15_19_and_20_49()

@step(u'Then I should see an error on number_of_females')
def then_i_should_see_an_error_on_number_of_females(step):
    world.page.see_an_error_on_number_of_females()

@step(u'And Now If I choose Other as occupation')
def and_now_if_i_choose_other_as_occupation(step):
    world.page.choose_occupation('Other: ')

@step(u'Then I have to specify one')
def then_i_have_to_specify_one(step):
    world.page.is_specify_visible(True)

@step(u'And If I choose a different occupation')
def and_if_i_choose_a_different_occupation(step):
    world.page.choose_occupation('Business person')

@step(u'Then Specify disappears')
def then_specify_disappears(step):
    world.page.is_specify_visible(False)

@step(u'Given I have an investigator')
def given_i_have_an_investigator(step):
    country = LocationType.objects.create(name="Country", slug=slugify("country"))
    uganda = Location.objects.create(name="Uganda", type=country)
    world.investigator = Investigator.objects.create(name="Investigator ", mobile_number='987654321', age=20,
                                                     level_of_education="Nursery", language="Luganda", location=uganda)

@step(u'Given I have 100 households')
def given_i_have_100_households(step):
    for _ in xrange(100):
        random_number = str(randint(1, 99999))
        try:
            HouseholdHead.objects.create(surname="head" + random_number, age=30 , male = False, household = Household.objects.create(investigator=world.investigator))
        except Exception:
            pass

@step(u'And I visit households listing page')
def and_i_visit_households_listing_page(step):
    world.page=HouseholdsListPage(world.browser)
    world.page.visit()

@step(u'And I should see the households list paginated')
def and_i_should_see_the_households_list_paginated(step):
    world.page.validate_fields()
    world.page.validate_pagination()

@step(u'Given I have no households')
def given_i_have_no_households(step):
    Household.objects.all().delete()

@step(u'And I should see no household message')
def and_i_should_see_no_household_message(step):
    world.page.no_registered_huseholds()

@step(u'And I click households option')
def and_i_click_households_option(step):
    world.page = HomePage(world.browser)
    world.page.click_link_by_text("Households")

@step(u'And I select list households')
def and_i_select_list_households(step):
    world.page.click_link_by_text("List all households")
    world.page=HouseholdsListPage(world.browser)
