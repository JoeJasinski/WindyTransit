from django.contrib import admin
from . import models
from mobiletrans.mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtimport', app_label=u'Importer').main()


class InputNoteInline(admin.TabularInline):
    readonly_fields = ['note','created','type']
    model = models.InputNote
    extra = 0 

class ImputRecordAdmin(admin.ModelAdmin):
    readonly_fields = ['start','end', 'status','type']
    list_display = ['start','end','status','type']
    list_filter = ['type',]
    inlines = [InputNoteInline,]


admin.site.register(models.InputRecord, ImputRecordAdmin)



