from lxml import objectify

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.conditions.models import Condition
from apps.options.models import OptionSet, Option
from apps.domain.models import AttributeEntity
from apps.questions.models import Catalog, Section, Subsection, QuestionEntity
from apps.tasks.models import Task
from apps.views.models import View


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('uri_prefix', action='store', help='URI prefix to be used for all elements.')

    def handle(self, *args, **options):

        for obj in Condition.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in OptionSet.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Option.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in AttributeEntity.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Catalog.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Section.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Subsection.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in QuestionEntity.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Task.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in View.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

    def _set_uri_prefix(self, obj, uri_prefix):
        obj.uri_prefix = uri_prefix
        obj.save()
