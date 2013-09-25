from lettuce import *
from survey.features.page_objects.question import BatchQuestionsListPage
from survey.features.page_objects.rules import AddLogicToBatchQuestionPage
from survey.models import Question


def save_batch_to_question(question, batch):
    question.batch = batch
    question.save()
@step(u'And I have a question')
def and_i_have_a_question(step):
    world.question = Question.objects.create(text="question1", answer_type=Question.NUMBER, order=1)

@step(u'And I assign batch to these questions')
def and_i_assign_batch_to_these_questions(step):
    save_batch_to_question(world.question, world.batch)

@step(u'And I visit batches question list page')
def and_i_visit_batches_question_list_page(step):
    world.page = BatchQuestionsListPage(world.browser, world.batch)
    world.page.visit()

@step(u'And I click on add logic link')
def and_i_click_on_add_logic_link(step):
    world.page.click_link_by_text(" Add Logic")

@step(u'Then I should see the add logic page')
def then_i_should_see_the_add_logic_page(step):
    world.page = AddLogicToBatchQuestionPage(world.browser, world.question)
    world.page.validate_url()
    world.page.validate_fields()

@step(u'When I fill in skip rule details')
def when_i_fill_in_skip_rule_details(step):
    form_data={'condition': 'EQUALS',
               'attribute': 'value',
               'value': '0',
               'action': 'END_INTERVIEW',
               }
    world.page.fill_valid_values(form_data)

@step(u'Then I should see the logic was successfully added to the question')
def then_i_should_see_the_logic_was_successfully_added_to_the_question(step):
    world.page.see_success_message('Logic','added')