from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rapidsms.contrib.locations.models import Location, LocationType
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from survey.investigator_configs import *
from survey.models import HouseholdMemberGroup
from survey.models.surveys import Survey
from survey.models.batch import Batch

from survey.forms.batch import BatchForm, BatchQuestionsForm


@login_required
@permission_required('auth.can_view_batches')
def index(request, survey_id):
    batches = Batch.objects.filter(survey__id= survey_id)
    context = {'batches': batches, 'survey': Survey.objects.get(id=survey_id),
               'request': request, 'batchform':BatchForm(),
               'action':'/surveys/%s/batches/new/' %survey_id, }
    return render(request, 'batches/index.html',
                  context)

@login_required
@permission_required('auth.can_view_batches')
def show(request, survey_id, batch_id):
    batch = Batch.objects.get(id=batch_id)
    prime_location_type = LocationType.objects.get(name=PRIME_LOCATION_TYPE)
    locations = Location.objects.filter(type=prime_location_type).order_by('name')
    open_locations = Location.objects.filter(id__in = batch.open_locations.values_list('location_id', flat=True))
    return render(request, 'batches/show.html', {'batch': batch, 'locations': locations, 'open_locations': open_locations})

@login_required
@permission_required('auth.can_view_batches')
def open(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    locations = Location.objects.get(id=request.POST['location_id']).get_descendants(include_self=True)
    for location in locations:
        batch.open_for_location(location)
    return HttpResponse()

@login_required
@permission_required('auth.can_view_batches')
def close(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    location = Location.objects.get(id=request.POST['location_id'])
    batch.close_for_location(location)
    return HttpResponse()

@login_required
@permission_required('auth.can_view_batches')
def new(request, survey_id):
    batchform = BatchForm()
    return _process_form(request=request, survey_id=survey_id, batchform=batchform, action_str='added')

def _process_form(request,survey_id, batchform, action_str='added', **batchform_kwargs):
    if request.method =='POST':
        batchform = BatchForm(data=request.POST, **batchform_kwargs)
        if batchform.is_valid():
            batch = batchform.save(commit=False)
            batch.survey= Survey.objects.get(id=survey_id)
            batch.save()
            _add_success_message(request, action_str)
            batch_list_url = '/surveys/%s/batches/' % str(survey_id)
            return HttpResponseRedirect(batch_list_url)
    return  render(request, 'batches/new.html', {'batchform':batchform,
                                                        'button_label':'Save',
                                                        'id':'add-batch-form'
                                                        })

@permission_required('auth.can_view_batches')
def edit(request, survey_id, batch_id):
    batch= Batch.objects.get(id=batch_id)
    batchform= BatchForm(instance=batch)
    return _process_form(request=request, survey_id=survey_id, batchform=batchform, action_str='edited',instance=batch)

def _add_success_message(request, action_str):
    messages.success(request, 'Batch successfully %s.'%action_str)

@permission_required('auth.can_view_batches')
def delete(request, survey_id, batch_id):
    Batch.objects.get(id=batch_id).delete()
    _add_success_message(request, 'deleted')
    return HttpResponseRedirect('/surveys/%s/batches/'%survey_id)

@permission_required('auth.can_view_batches')
def assign(request, batch_id):
    batch_questions_form = BatchQuestionsForm()
    groups = HouseholdMemberGroup.objects.all()
    batch = Batch.objects.get(id=batch_id)
    if request.method == 'POST':
        batch_question_form = BatchQuestionsForm(data=request.POST, instance=batch)
        if batch_question_form.is_valid():
            batch_question_form.save()
            success_message ="Questions successfully assigned to batch: %s."%batch.name.capitalize()
            messages.success(request, success_message)
            return HttpResponseRedirect("/batches/%s/questions/" %batch_id)
    context = {'batch_questions_form': batch_questions_form, 'batch': batch,
               'button_label':'Save', 'id':'assign-question-to-batch-form', 'groups':groups}
    return render(request, 'batches/assign.html',
                  context)