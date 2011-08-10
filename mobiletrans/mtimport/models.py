from django.db import models
import datetime

TRANSFER_STATUS_RUNNING=1
TRANSFER_STATUS_SUCCESS=2
TRANSFER_STATUS_FAILED=3
TRANSFER_STATUS_PARTIAL=4
TRANSFER_STATUS = (
  (TRANSFER_STATUS_RUNNING, "Running"),
  (TRANSFER_STATUS_FAILED, "Failed"),                   
  (TRANSFER_STATUS_SUCCESS, "Complete"),
  (TRANSFER_STATUS_PARTIAL, "Partial Import"),
)

TRANSFER_NOTE_STATUS_NOTE = "note"
TRANSFER_NOTE_STATUS_ERROR = "error"
TRANSFER_NOTE_STATUS_WARNING = "warning"
TRANSFER_NOTE_STATUS = (
 (TRANSFER_NOTE_STATUS_NOTE, "Note"),
 (TRANSFER_NOTE_STATUS_ERROR, "Error"),
 (TRANSFER_NOTE_STATUS_WARNING, "Warning"),
)

class InputRecordManager(models.Manager):
    
    def make_note(self, input_record, note, type):
        ir = InputNote(note=note, type=type)
        ir.input_record = input_record
        #print vars(ir)
        ir.save()
    
    def end_import(self, input_record, status=None):
        if status:
            input_record.status = status
        input_record.end = datetime.datetime.now()
        input_record.save()

class InputRecord(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(choices=TRANSFER_STATUS, default=TRANSFER_STATUS_RUNNING)

    objects = InputRecordManager()

    def __unicode__(self):
        return "%s" % self.start


class InputNote(models.Model):
    input_record = models.ForeignKey(InputRecord)
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=TRANSFER_NOTE_STATUS, max_length=24)
    
    def __unicode__(self):
        return "%s" % self.created
    
