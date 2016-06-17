from django.contrib import admin
from mobiletrans.mtimport import models
from mobiletrans.mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtimport', app_label=u'Importer').main()


class InputNoteInline(admin.TabularInline):
    readonly_fields = ['note', 'created', 'type', 'exception']
    model = models.InputNote
    extra = 0
    can_delete = False


class ImputRecordAdmin(admin.ModelAdmin):
    readonly_fields = ['start', 'end', 'status', 'type', 'exception']
    list_display = [
        'start', 'end', 'status', 'type', 'get_num_errors', 'get_num_warnings']
    list_filter = ['type', ]
    inlines = [InputNoteInline, ]


admin.site.register(models.InputRecord, ImputRecordAdmin)
