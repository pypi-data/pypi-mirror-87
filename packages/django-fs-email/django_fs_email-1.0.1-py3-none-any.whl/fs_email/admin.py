from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['when', 'whom', 'subject', 'status']
    search_fields = ['whom', 'subject']
    readonly_fields = ['when', '_body']
    fieldsets = [
        [None, {'fields': ['when', 'whom', 'subject', 'status']}],
        [None, {'fields': ['_body']}],
    ]

    def _body(self, obj):
        return obj.body
    _body.short_description = _('body')
    _body.allow_tags = True
