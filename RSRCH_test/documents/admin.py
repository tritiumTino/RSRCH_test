from django.contrib import admin
from .models import YAMLTemplate, EDocument, Value


class YAMLTemplateAdminView(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'content')


class ValueInline(admin.TabularInline):
    model = Value


class EDocumentAdminView(admin.ModelAdmin):
    inlines = [
        ValueInline,
    ]
    list_display = ('id_doc', 'doc_name',)
    list_display_links = ('id_doc', 'doc_name',)
    readonly_fields = ('id_doc', 'doc_name', )
    fields = ('id_doc', 'template', 'doc_name', 'send_list')


admin.site.register(YAMLTemplate, YAMLTemplateAdminView)
admin.site.register(EDocument, EDocumentAdminView)
