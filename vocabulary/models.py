from django.db import models
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel

from core.forms import CoreAdminModelForm
from core.models import CommonControlField, TextWithLang


class Vocabulary(CommonControlField):
    name = models.TextField(_("Vocabulary name"), null=True, blank=True)
    acronym = models.CharField(
        _("Vocabulary acronym"), max_length=10, null=True, blank=True
    )

    autocomplete_search_field = "name"

    def autocomplete_label(self):
        return str(self)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.acronym) or ""

    def __str__(self):
        return "%s - %s" % (self.name, self.acronym) or ""

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "acronym",
                ]
            ),
        ]

    panels = [
        FieldPanel("name"),
        FieldPanel("acronym"),
    ]

    @property
    def data(self):
        d = {
            "vocabulary__name": self.name,
            "vocabulary__acronym": self.acronym,
        }
        return d

    @classmethod
    def load(cls, user, items=None):
        if cls.objects.count() == 0:
            items = items or [
                {"name": "Health Science Descriptors", "acronym": "decs"},
                {"name": "Not defined", "acronym": "nd"},
            ]
            for item in items:
                cls.get_or_create(user, **item)

    @classmethod
    def get(cls, acronym=None):
        if not acronym:
            raise ValueError("Vocabulary.get_or_create requires acronym")
        return cls.objects.get(acronym=acronym)

    @classmethod
    def get_or_create(cls, user, name=None, acronym=None):
        try:
            return cls.get(acronym=acronym)
        except cls.DoesNotExist:
            vocabulary = cls()
            vocabulary.name = name
            vocabulary.acronym = acronym
            vocabulary.creator = user
            vocabulary.save()
            return vocabulary

    base_form_class = CoreAdminModelForm


class Keyword(CommonControlField, TextWithLang):
    vocabulary = models.ForeignKey(
        Vocabulary,
        verbose_name=_("Vocabulary"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    autocomplete_search_field = "text"

    def autocomplete_label(self):
        return str(self.text)

    def __unicode__(self):
        return "%s - %s" % (self.text, self.language) or ""

    def __str__(self):
        return "%s - %s" % (self.text, self.language) or ""

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "text",
                ]
            ),
            models.Index(
                fields=[
                    "language",
                ]
            ),
            models.Index(
                fields=[
                    "vocabulary",
                ]
            ),
        ]

    panels = [
        FieldPanel("text"),
        FieldPanel("language"),
        AutocompletePanel("vocabulary"),
    ]

    @property
    def data(self):
        d = {
            "keyword__text": self.text,
            "keyword__language": self.language,
            "keyword__vocabulary": self.vocabulary,
        }
        return d

    @classmethod
    def get_or_create(cls, text, language, user):
        try:
            return cls.objects.get(text=text, language=language)
        except cls.DoesNotExist:
            keyword = cls()
            keyword.text = text
            keyword.language = language
            # keyword.vocabulary = vocabulary
            keyword.creator = user
            keyword.save()
            return keyword

    base_form_class = CoreAdminModelForm
