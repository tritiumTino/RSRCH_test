from django.contrib import admin
from .models import RegistrationCard


class RegistrationCardAdminView(admin.ModelAdmin):
    list_display = ('reg_doc', 'receiver', 'reg_doc_date', 'updated_at',)
    readonly_fields = ('receiver', 'reg_doc', 'reg_doc_date', 'doc_content', 'updated_at',
                       'key', 'signature', 'is_approved', 'is_refused')


admin.site.register(RegistrationCard, RegistrationCardAdminView)
