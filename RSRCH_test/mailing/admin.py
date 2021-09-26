from django.contrib import admin
from .models import Tag, FiledType


class TagAdminView(admin.ModelAdmin):
    list_display = ('name', 'variable', 'is_common')


admin.site.register(Tag, TagAdminView)
admin.site.register(FiledType)
