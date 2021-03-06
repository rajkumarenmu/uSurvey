from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView
from django.conf import settings
import os
from django.views.static import serve as staticserve

urlpatterns = patterns('',
                       (r'^static/(?P<path>.*)$', staticserve,
                        {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
                       url(r'^$', 'survey.views.home_page.index', name='main_page'),
                       url(r'^home/$', 'survey.views.home_page.home',
                           name='home_page'),
                       url(r'^about/$', 'survey.views.home_page.about',
                           name='about_page'),
                       url(r'^about/edit/$', 'survey.views.home_page.edit',
                           name='edit_about_page'),
                       #     url(r'^locations/hierarchy/add/$', 'survey.views.location_hierarchy.add', name='add_location_hierarchy'),
                       #url(r'^locations/upload/$', 'survey.views.location_hierarchy.upload', name='upload_locations'),
                       url(r'^locations/weights/upload/$',
                           'survey.views.location_weights.upload', name='upload_weights'),
                       url(r'^locations/enumeration_area/upload/$',
                           'survey.views.enumeration_area.upload', name='upload_ea'),
                       url(r'^locations/weights/$',
                           'survey.views.location_weights.list_weights', name='list_weights_page'),
                       url(r'^locations/weights/error_logs/$',
                           'survey.views.location_weights.error_logs', name='weights_error_logs_page'),
                       url(r'^locations/(?P<location_id>\d+)/children',
                           'survey.views.locations.children', name='get_location_children'),
                       url(r'^locations/(?P<location_id>\d+)/enumeration_areas',
                           'survey.views.locations.enumeration_areas', name='get_enumeration_areas'),
                       url(r'^interviewers/$', 'survey.views.interviewer.list_interviewers',
                           name="interviewers_page"),
                       url(r'^interviewers/export/$', 'survey.views.interviewer.download_interviewers',
                           name="download_interviewers"),
                       url(r'^interviewers/completion_summary/(?P<interviewer_id>\d+)/$',
                           'survey.views.interviewer.show_completion_summary', name="interviewer_completion_summary"),
                       url(r'^interviewers/new/$', 'survey.views.interviewer.new_interviewer',
                           name="new_interviewer_page"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/$',
                           'survey.views.interviewer.show_interviewer', name="show_interviewer_page"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/block/$',
                           'survey.views.interviewer.block_interviewer', name="block_interviewer_page"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/block_odk/$',
                           'survey.views.interviewer.block_odk', name="block_interviewer_odk"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/block_ussd/$',
                           'survey.views.interviewer.block_ussd', name="block_interviewer_ussd"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/unblock_odk/$',
                           'survey.views.interviewer.unblock_odk', name="unblock_interviewer_odk"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/unblock_ussd/$',
                           'survey.views.interviewer.unblock_ussd', name="unblock_interviewer_ussd"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/unblock/$',
                           'survey.views.interviewer.unblock_interviewer', name="unblock_interviewer_page"),
                       url(r'^interviewers/(?P<interviewer_id>\d+)/edit/$',
                           'survey.views.interviewer.edit_interviewer', name="edit_interviewer_page"),
                       url(r'^interviewers/check_mobile_number',
                           'survey.views.interviewer.check_mobile_number', name="check_mobile_number"),
                       url(r'^ussd/simulator', permission_required('auth.can_view_interviewers')
                           (TemplateView.as_view(template_name="ussd/simulator.html")), name='simulator_page'),
                       url(r'^ussd', 'survey.ussd.handler.handle', name="ussd"),
                       url(r'^households/$', 'survey.views.household.list_households',
                           name="list_household_page"),
                       url(r'^households/(?P<household_id>\d+)/$',
                           'survey.views.household.view_household', name="view_household_page"),
                       url(r'^households/(?P<household_id>\d+)/edit/$',
                           'survey.views.household.edit_household', name="edit_household_page"),
                       url(r'^households/new/$', 'survey.views.household.new',
                           name="new_household_page"),
                       url(r'^households/download/$',
                           'survey.views.household.download_households', name="download_household"),
                       url(r'^households/interviewers',
                           'survey.views.household.get_interviewers', name='load_interviewers'),
                       url(r'^households/(?P<household_id>\d+)/member/new/$',
                           'survey.views.household_member.new', name='new_household_member_page'),
                       url(r'^households/(?P<household_id>\d+)/member/(?P<member_id>\d+)/edit/$',
                           'survey.views.household_member.edit', name='edit_household_member_page'),
                       url(r'^households/(?P<household_id>\d+)/member/(?P<member_id>\d+)/delete/$',
                           'survey.views.household_member.delete', name='delete_household_member_page'),
                       url(r'^aggregates/spreadsheet_report/$',
                           'survey.views.excel.download', name='excel_report'),
                       url(r'^aggregates/spreadsheet_results/(?P<batch_id>\d+)/$',
                           'survey.views.excel.download_results', name='download_export_results'),
                       url(r'^aggregates/download_spreadsheet',
                           'survey.views.excel.download', name='download_excel'),
                       url(r'^interviewer_report/', 'survey.views.excel.interviewer_report',
                           name='interviewer_report_page'),
                       url(r'^interviewers/completed/download/',
                           'survey.views.excel.completed_interviewer', name='download_interviewer_excel'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'accounts/login.html'}, name='login_page'),
                       url(r'^accounts/logout/$',
                           'django.contrib.auth.views.logout_then_login', name='logout_page'),
                       url(r'^accounts/reset_password/$', 'django.contrib.auth.views.password_change',
                           {'template_name': 'accounts/reset_password.html', 'post_change_redirect': '/accounts/reset_password/done/',
                            'password_change_form': PasswordChangeForm}, name='password_change'),
                       url(r'^accounts/reset_password/done/$', TemplateView.as_view(
                           template_name='accounts/password_reset_done.html'), name='password_reset_done'),
                       url(r'^bulk_sms$', 'survey.views.bulk_sms.view',
                           name='bulk_sms'),
                       url(r'^bulk_sms/send$', 'survey.views.bulk_sms.send',
                           name='send_bulk_sms'),
                       url(r'^users/$', 'survey.views.users.index',
                           name='users_index'),
                       url(r'^users/new/$', 'survey.views.users.new',
                           name='new_user_page'),
                       url(r'^users/(?P<user_id>\d+)/edit/$',
                           'survey.views.users.edit', name='users_edit'),
                       url(r'^users/(?P<user_id>\d+)/deactivate/$',
                           'survey.views.users.deactivate', name='deactivate_user'),
                       url(r'^users/(?P<user_id>\d+)/activate/$',
                           'survey.views.users.activate', name='activate_user'),
                       url(r'^users/(?P<user_id>\d+)/$',
                           'survey.views.users.show', name='users_show_details'),
                       url(r'^batches/(?P<batch_id>\d+)/assign_questions/$',
                           'survey.views.batch.assign', name='assign_questions_page'),
                       url(r'^batches/(?P<batch_id>\d+)/update_question_orders/$',
                           'survey.views.batch.update_orders', name='update_question_order_page'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/$',
                           'survey.views.questions.index', name='batch_questions_page'),
                       url(r'^batches/(?P<batch_id>\d+)/submit_questions/$',
                           'survey.views.questions.submit', name='batch_questions_submission'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/export/$',
                           'survey.views.questions.export_batch_questions', name='export_questions_in_batch'),
                       url(r'^batches/(?P<batch_id>\d+)/open_to$',
                           'survey.views.batch.open', name='batch_open_page'),
                       url(r'^batches/(?P<batch_id>\d+)/all_locs$',
                           'survey.views.batch.all_locs', name='batch_all_locs'),
                       url(r'^batches/(?P<batch_id>\d+)/non_response/activate/$',
                           'survey.views.batch.activate_non_response', name="activate_non_response_page"),
                       url(r'^batches/(?P<batch_id>\d+)/non_response/deactivate/$',
                           'survey.views.batch.deactivate_non_response', name="deactivate_non_response_page"),
                       url(r'^batches/(?P<batch_id>\d+)/close_to$',
                           'survey.views.batch.close', name='batch_close_page'),
                       ############
                       url(r'^batches/(?P<batch_id>\d+)/questions/(?P<question_id>\d+)/add_logic/$',
                           'survey.views.questions.add_logic', name='add_question_logic_page'),
                       url(r'^batches/questions/delete_logic/(?P<flow_id>\d+)/$',
                           'survey.views.questions.delete_logic', name='delete_question_logic_page'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/(?P<question_id>\d+)/questions_json/$',
                           'survey.views.questions.get_questions_for_batch', name='batch_questions_json_page'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/sub_questions/new/$',
                           'survey.views.questions.new_subquestion', name='add_batch_subquestion_page'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/(?P<question_id>\d+)/sub_questions/edit/$',
                           'survey.views.questions.edit_subquestion', name='edit_batch_subquestion_page'),
                       #    url(r'^batches/(?P<batch_id>\d+)/questions/(?P<question_id>\d+)/delete/$', 'survey.views.questions.delete', name='delete_batch_question_page'),
                       url(r'^batches/(?P<batch_id>\d+)/questions/(?P<question_id>\d+)/remove/$',
                           'survey.views.questions.remove', name='remove_question_page'),
                       ##########
                       url(r'^batches/$', 'survey.views.batch.list_batches'),
                       url(r'^groups/(?P<group_id>\d+)/$', 'survey.views.household_member_group.details',
                           name='household_member_groups_details'),
                       url(r'^groups/(?P<group_id>\d+)/conditions/new/$',
                           'survey.views.household_member_group.add_group_condition', name='new_condition_for_group'),
                       url(r'^groups/$', 'survey.views.household_member_group.index',
                           name='household_member_groups_page'),
                       url(r'^groups/new/$', 'survey.views.household_member_group.add_group',
                           name='new_household_member_groups_page'),
                       url(r'^groups/(?P<group_id>\d+)/edit/$',
                           'survey.views.household_member_group.edit_group', name='household_member_groups_edit'),
                       url(r'^groups/(?P<group_id>\d+)/delete/$',
                           'survey.views.household_member_group.delete_group', name='household_member_groups_delete'),
                       url(r'^conditions/$', 'survey.views.household_member_group.conditions',
                           name='show_group_condition'),
                       url(r'^conditions/new/$', 'survey.views.household_member_group.add_condition',
                           name='new_group_condition'),
                       url(r'^conditions/(?P<condition_id>\d+)/delete/$',
                           'survey.views.household_member_group.delete_condition', name='delete_condition_page'),
                       url(r'^surveys/$', 'survey.views.surveys.index',
                           name='survey_list_page'),
                       # url(r'^surveys/(?P<survey_id>\d+)/manage$', 'survey.views.surveys.manage', name='manage_survey_page'),
                       url(r'^surveys/new/$', 'survey.views.surveys.new',
                           name='new_survey_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/edit/$',
                           'survey.views.surveys.edit', name='edit_survey_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/delete/$',
                           'survey.views.surveys.delete', name='delete_survey'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/$',
                           'survey.views.batch.index', name='batch_index_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/survey_batches/$',
                           'survey.views.batch.batches', name='survey_batches_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/new/$',
                           'survey.views.batch.new', name='new_batch_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/(?P<batch_id>\d+)/$',
                           'survey.views.batch.show', name='batch_show_page'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/(?P<batch_id>\d+)/edit/$',
                           'survey.views.batch.edit', name='batch_edit_page'),
                       url(r'^surveys/completion/', 'survey.views.survey_completion.show',
                           name='survey_completion_rates'),
                       url(r'^surveys/ea_completion/(?P<ea_id>\d+)/(?P<batch_id>\d+)',
                           'survey.views.survey_completion.ea_completion_summary', name='ea_completion_summary'),
                       url(r'^surveys/locations_completion_summary/(?P<location_id>\d+)/(?P<batch_id>\d+)',
                           'survey.views.survey_completion.location_completion_summary', name='location_completion_summary'),
                       url(r'^surveys/completion_summary/(?P<household_id>\d+)/(?P<batch_id>\d+)',
                           'survey.views.survey_completion.survey_completion_summary', name='house_completion_summary'),
                       url(r'^surveys/interviewers_completion/$', 'survey.views.survey_completion.show_interviewer_completion_summary',
                           name='show_interviewer_completion_summary'),
                       url(r'^survey/(?P<survey_id>\d+)/completion/json/$',
                           'survey.views.survey_completion.completion_json', name='survey_completion_json'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/(?P<batch_id>\d+)/delete/$',
                           'survey.views.batch.delete', name='delete_batch'),
                       url(r'^surveys/(?P<survey_id>\d+)/batches/check_name/$',
                           'survey.views.batch.check_name'),
                       url(r'^question_library/$', 'survey.views.question_template.index',
                           name='show_question_library'),
                       url(r'^question_library/new/$', 'survey.views.question_template.add',
                           name='new_question_template'),
                       url(r'^question_library/(?P<question_id>\d+)/edit/$',
                           'survey.views.question_template.edit', name='edit_question_template_page'),
                       url(r'^question_library/(?P<question_id>\d+)/delete/$',
                           'survey.views.question_template.delete', name='delete_question_template_page'),
                       url(r'^question_library/export/$', 'survey.views.question_template.export_questions',
                           name='export_template_questions'),
                       url(r'^question_library/json_filter/',
                           'survey.views.question_template.filter', name='filter_question_list'),
                       #    url(r'^questions/new/$', 'survey.views.questions.new', name='new_question_page'),
                       #    url(r'^questions/(?P<question_id>\d+)/is_multichoice/$', 'survey.views.questions.is_multichoice', name='check_multichoice'),
                       #    url(r'^questions/(?P<question_id>\d+)/sub_questions/new/$', 'survey.views.questions.new_subquestion', name='add_subquestion_page'),
                       #    url(r'^questions/(?P<question_id>\d+)/sub_questions/edit/$', 'survey.views.questions.edit_subquestion', name='edit_subquestion_page'),
                       url(r'^questions/(?P<batch_id>\d+)/new/$',
                           'survey.views.questions.new', name='new_batch_question_page'),
                       url(r'^questions/(?P<question_id>\d+)/edit/$',
                           'survey.views.questions.edit', name='edit_question_page'),
                       url(r'^questions/(?P<question_id>\d+)/sub_questions_json/$',
                           'survey.views.questions.get_sub_questions_for_question', name='questions_subquestion_json_page'),
                       url(r'^questions/(?P<question_id>\d+)/prev_questions_json/$',
                           'survey.views.questions.get_prev_questions_for_question', name='prev_inline_questions_json_page'),
                       url(r'^questions/(?P<question_id>\d+)/delete/$',
                           'survey.views.questions.delete', name='delete_question_page'),

                       url(r'^enumeration_area/new/$', 'survey.views.enumeration_area.new',
                           name='new_enumeration_area_page'),
                       url(r'^enumeration_area/(?P<ea_id>\d+)/edit/$',
                           'survey.views.enumeration_area.edit', name='edit_enumeration_area_page'),
                       url(r'^enumeration_area/(?P<ea_id>\d+)/delete/$',
                           'survey.views.enumeration_area.delete', name='delete_enumeration_area'),
                       url(r'^enumeration_area/$', 'survey.views.enumeration_area.index',
                           name='enumeration_area_home'),
                       url(r'^enumeration_area/filter/$',
                           'survey.views.enumeration_area.location_filter', name='location_filter'),
                       url(r'^enumeration_area/sub_types/$',
                           'survey.views.enumeration_area.location_sub_types', name='location_sub_types'),
                       url(r'^enumeration_area/ea_filter/$',
                           'survey.views.enumeration_area.enumeration_area_filter', name='enumeration_area_filter'),
                       url(r'^enumeration_area/open_surveys/$',
                           'survey.views.enumeration_area.open_surveys', name='open_surveys_in_ea_area'),
                       url(r'^modules/new/$', 'survey.views.question_module.new',
                           name='new_question_module_page'),
                       url(r'^modules/$', 'survey.views.question_module.index',
                           name='question_module_listing_page'),
                       url(r'^modules/(?P<module_id>\d+)/delete/$',
                           'survey.views.question_module.delete', name='delete_question_module_page'),
                       url(r'^modules/(?P<module_id>\d+)/edit/$',
                           'survey.views.question_module.edit', name='edit_question_module_page'),
                       url(r'^indicators/new/$', 'survey.views.indicators.new',
                           name='new_indicator_page'),
                       url(r'^indicators/$', 'survey.views.indicators.index',
                           name='list_indicator_page'),
                       url(r'^indicators/(?P<indicator_id>\d+)/formula/new/$',
                           'survey.views.formula.new', name='add_formula_page'),
                       url(r'^indicators/(?P<indicator_id>\d+)/simple/$',
                           'survey.views.formula.simple_indicator', name='simple_indicator_chart_page'),
                       url(r'^indicators/(?P<indicator_id>\d+)/delete/$',
                           'survey.views.indicators.delete', name='delete_indicator_page'),
                       url(r'^indicators/(?P<indicator_id>\d+)/edit/$',
                           'survey.views.indicators.edit', name='edit_indicator_page'),
                       url(r'^indicators/(?P<indicator_id>\d+)/formula/(?P<formula_id>\d+)/delete/',
                           'survey.views.formula.delete', name='delete_indicator_formula_page'),
                       url(r'^odk/collect/(?P<username>\d+)/(?P<token>[^/]+)/forms$',
                           'survey.odk.views.form_list', name='odk_survey_forms_list'),
                       url(r'^odk/collect/forms/(?P<survey_id>\d+)$',
                           'survey.odk.views.download_xform', name='download_odk_survey_form'),
                       url(r'^odk/collect/forms$', 'survey.odk.views.form_list',
                           name='odk_survey_forms_list'),
                       url(r'^odk/collect/forms/household_list$',
                           'survey.odk.views.download_houselist_xform', name='download_odk_householdlist_form'),
                       url(r'^odk/collect/forms/submission$',
                           'survey.odk.views.submission', name='odk_submit_forms'),
                       url(r'^odk/aggregate/submission_list/$',
                           'survey.odk.views.submission_list', name='odk_submission_list'),
                       url(r'^odk/aggregate/download_attachment/(?P<submission_id>\d+)$',
                           'survey.odk.views.download_submission_attachment', name='download_submission_attachment'),
                       url(r'^object_does_not_exist/$',
                           login_required(TemplateView.as_view(template_name="empty.html")), name='empty_page')
                       )

# if not settings.PRODUCTION:
#     urlpatterns += (
#         url(r'^api/create_interviewer', 'survey.views.api.create_interviewer', name='create_interviewer'),
#         url(r'^api/delete_interviewer', 'survey.views.api.delete_interviewer', name='delete_interviewer'),
#     )
