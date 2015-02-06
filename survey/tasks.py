from celery.task import task

@task
def upload_task(upload_form):
    return upload_form.upload()

@task
def email_task(composer):
    return composer.send_mail()

@task
def save_attachments(odk_submission, media_files, submission_function=None):
    """A function to save the media files associated with this ODK submissions
    using a celery task."""
    if submission_function is None:
        return odk_submission.save_attachments(media_files)
    else:
        return submission_function(odk_sumission, media_files)
