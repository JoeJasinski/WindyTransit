from django.contrib import admin
from . import models


class InputNoteInline(admin.TabularInline):
    readonly_fields = ['note','created','type']
    model = models.InputNote
    extra = 0 

class ImputRecordAdmin(admin.ModelAdmin):
    readonly_fields = ['start','end', 'status']
    list_display = ['start','end','status']
    inlines = [InputNoteInline,]


admin.site.register(models.InputRecord, ImputRecordAdmin)