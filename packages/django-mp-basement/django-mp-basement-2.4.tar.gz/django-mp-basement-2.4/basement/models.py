
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractImportTask(models.Model):

    created = models.DateTimeField(
        _('Creation date'),
        auto_now_add=True)

    file = models.FileField(
        _('File'),
        upload_to='import_cache',
        blank=True,
        null=True)

    is_completed = models.BooleanField(
        _('Is completed'),
        default=False)

    is_processing = models.BooleanField(_('Is processing'), default=False)

    status = models.CharField(_('Status'), max_length=255, blank=True)

    percent = models.CharField(_('Percent'), max_length=10, blank=True)

    def __str__(self):
        return str(self.created)

    def update_progress(
            self,
            percent,
            status=None,
            is_processing=None,
            is_completed=None):

        update_fields = ['percent']

        self.percent = percent

        if status is not None:
            self.status = status
            update_fields.append('status')

        if is_processing is not None:
            self.is_processing = is_processing
            update_fields.append('is_processing')

        if is_completed is not None:
            self.is_completed = is_completed
            update_fields.append('is_completed')

        self.save(update_fields=update_fields)

    @classmethod
    def get(cls, task_id):
        return cls.objects.get(id=task_id)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = _('Import task')
        verbose_name_plural = _('Import tasks')
