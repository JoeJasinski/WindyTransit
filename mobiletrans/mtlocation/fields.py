from django.db import models

from south.modelsinspector import add_introspection_rules
from django_extensions.db.fields import UUIDField as ExtUUIDField

class UUIDField(ExtUUIDField):

    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 40
        if auto:
            self.empty_strings_allowed = False
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto = auto
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        models.CharField.__init__(self, verbose_name, name, **kwargs)


class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, *args, **kwargs):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)

add_introspection_rules([], ["^mobiletrans\.mtlocation\.fields\.SeparatedValuesField"])