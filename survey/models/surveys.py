from django.db import models

from survey.models.base import BaseModel


class Survey(BaseModel):
    name = models.CharField(max_length=100, blank=False,null=True)
    description = models.CharField(max_length=300,blank=True,null=True)
    sample_size = models.PositiveIntegerField(max_length=2, null=False, blank=False, default=10, verbose_name="Number of Households per Investigator")
    type = models.BooleanField(default=False)
    has_sampling = models.BooleanField(default=True)

    class Meta:
        app_label = 'survey'

    def is_open(self, location=None):
        all_batches = self.batch.all()
        for batch in all_batches:
            batch_open_locations = batch.open_locations.all()
            all_locations = batch_open_locations.filter(location=location) if location else batch_open_locations
            if all_locations:
                return True
        return False

    def is_open_for(self, location):
        all_batches = self.batch.all()
        for batch in all_batches:
            if batch.is_open_for(location):
                return True
        return False

    @classmethod
    def currently_open_survey(cls, location=None):
        for survey in Survey.objects.filter():
            if survey.is_open(location):
                return survey
        return None

    @classmethod
    def save_sample_size(cls, survey_form):
        survey = survey_form.save(commit=False)
        if not survey.has_sampling:
            survey.sample_size = 0
        survey.save()


    def __unicode__(self):
        return self.name
