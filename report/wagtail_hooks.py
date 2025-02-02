from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from django.utils.translation import gettext as _

from .models import ReportCSV


class ReportCSVAdmin(ModelAdmin):
    model = ReportCSV
    menu_label = _("Report CSV")
    menu_icon = "folder"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "journal",
        "title",
        "publication_year",
        "created",
        "updated",
        "link_download"
    )
    list_filter = (
        "publication_year",
        "title",
    )
    
    search_fields = (
        "title",
        "journal__title",
        "journal__scielojournal__issn_scielo",
    )

    def link_download(self, obj):
        if obj.file and obj.file.url:
            return f"<a target='_blank' href={obj.file.url}>Download</a>"
        return None

    link_download.short_descriptions = 'Download'
    link_download.allow_tags = True

modeladmin_register(ReportCSVAdmin)