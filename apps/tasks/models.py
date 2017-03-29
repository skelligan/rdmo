from __future__ import unicode_literals

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from datetime import timedelta

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.utils import get_uri_prefix
from apps.core.models import TranslationMixin
from apps.domain.models import Attribute
from apps.conditions.models import Condition
from apps.projects.models import Value

from .managers import TaskManager
from .validators import TaskUniqueKeyValidator


@python_2_unicode_compatible
class Task(TranslationMixin, models.Model):

    objects = TaskManager()

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this task (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this task.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this task. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this task.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this task.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this task.')
    )
    text_en = models.CharField(
        max_length=256,
        verbose_name=_('Text (en)'),
        help_text=_('The English text for this task.')
    )
    text_de = models.CharField(
        max_length=256,
        verbose_name=_('Text (de)'),
        help_text=_('The German text for this task.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('The list of conditions evaluated for this task.')
    )

    class Meta:
        ordering = ('uri',)
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        permissions = (('view_task', 'Can view Task'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(Task, self).save(*args, **kwargs)

    def clean(self):
        TaskUniqueKeyValidator(self).validate()

    @property
    def title(self):
        return self.trans('title')

    @property
    def text(self):
        return self.trans('text')

    @property
    def has_conditions(self):
        return bool(self.conditions.all())

    def build_uri(self):
        return get_uri_prefix(self) + '/tasks/' + self.key


@python_2_unicode_compatible
class TimeFrame(models.Model):

    task = models.OneToOneField(
        Task,
        verbose_name=_('Task'),
        help_text=_('The task this time frame belongs to.')
    )
    start_attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Start date attribute'),
        help_text=_('The Attribute that is setting the start date for this task.')
    )
    end_attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('End date attribute'),
        help_text=_('The Attribute that is setting the end date for this task (optional).')
    )
    days_before = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('Days before start date.'),
        help_text=_('.')
    )
    days_after = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('Attribute'),
        help_text=_('Days after end date.')
    )

    class Meta:
        ordering = ('task', )
        verbose_name = _('Time frame')
        verbose_name_plural = _('Time frames')
        permissions = (('view_timeframe', 'Can view Time frame'),)

    def __str__(self):
        return self.task.uri

    def get_dates(self, project):
        if self.start_attribute:
            start_values = Value.objects.filter(project=project, attribute=self.start_attribute)
        else:
            start_values = []

        if self.end_attribute:
            end_values = Value.objects.filter(project=project, attribute=self.end_attribute)
        else:
            end_values = []

        days_before = timedelta(self.days_before) if self.days_before else timedelta()
        days_after = timedelta(self.days_after) if self.days_after else timedelta()

        if len(start_values) == 0:
            if end_values:
                dates = [(end_value.value - days_before + days_after, ) for end_value in end_values]
            else:
                dates = []

        elif len(start_values) == 1:

            if end_values:
                dates = [(start_values[0].value - days_before, end_value.value + days_after) for end_value in end_values]
            else:
                dates = [(start_values[0].value - days_before + days_after, )]

        else:
            if end_values:
                dates = []
                for start_value, end_value in zip_longest(start_values, end_values):

                    if start_value and end_value:
                        dates.append((start_value.value - days_before, end_value.value + days_after))
                    elif start_value:
                        dates.append((start_value.value - days_before + days_after, ))
                    elif end_value:
                        dates.append((end_value.value - days_before + days_after, ))
            else:
                dates = [(start_value.value - days_before + days_after, ) for start_value in start_values]

        return dates
