import copy
import types
import warnings

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.utils.datastructures import SortedDict

typemapper = {}
handler_tracker = []

class Field(object):
    def __init__(self, name, xform_obj=None, destination=None, required=True, iterable_xform_obj=False):
        self.name = name
        self.name_parts = [x for x in name.split('.') if x]
        self.required = required
        self.xform_obj = xform_obj
        self.iterable_xform_obj = iterable_xform_obj
        self.destination = destination or name
        if destination is None and '.' in name:
            raise ValueError('Cannot specify a non top-level attribute (%s) and not specify a destination name.' % name)

    def get_value(self, obj):
        value = obj
        for name in self.name_parts:
            try:
                value = getattr(value, name)
                # Might be attribute or callable
                if type(value) in (types.FunctionType, types.MethodType):
                    try:
                        value = value()
                    except TypeError:
                        if self.required:
                            raise TypeError("%s is a required field but not in %s." % name, value)
                        return None
            except AttributeError:
                try:
                    value = value[name]
                except (KeyError, TypeError):
                    if self.required:
                        raise KeyError("%s is a required field but not in %s" % (name, value))
                    return None

        if value is not None and self.xform_obj:
            if self.iterable_xform_obj:
                value = [self.xform_obj(x) for x in value]
            else:
                value = self.xform_obj(value)

        return value


class PistonViewMetaclass(type):
    """
    Metaclass that converts Field attributes to a dictionary called
    'base_fields', taking into account parent class 'base_fields' as well.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(PistonViewMetaclass, cls).__new__
        parents = [b for b in bases if isinstance(b, PistonViewMetaclass)]
        if not parents:
            # If this isn't a subclass of PistonViewMetaclass, don't do anything special.
            return super_new(cls, name, bases, attrs)

        base_fields = SortedDict()
        for parent_cls in parents:
            for field in getattr(parent_cls, 'base_fields', []):
                # if the superclass has defined a field, don't add
                # that field from the base class since inspect.getmro
                # lists classes in order from super to base
                if field.destination not in base_fields:
                    base_fields[field.destination] = field

        for field in attrs.get('fields', []):
            if isinstance(field, basestring):
                field = Field(field)
            base_fields[field.destination] = field

        attrs['base_fields'] = base_fields.values()

        new_class = super_new(cls, name, bases, attrs)
        return new_class


class BasePistonView(object):
    def __new__(cls, data, *args, **kwargs):
        if isinstance(data, (list, tuple)):
            return [cls.__new__(cls, x, *args, **kwargs) for x in data]
        obj = object.__new__(cls)
        obj.__init__(data, *args, **kwargs)
        return obj

    def __init__(self, data):
        self.data = data
        self.fields = copy.deepcopy(self.base_fields)

    def render(self):
        result = {}
        for field in self.fields:
            value = field.get_value(self.data)
            # skip if field is None and not required
            if not (value is None and not field.required):
                destination = result
                keys = field.destination.split('.')
                sub_keys, key = keys[:-1], keys[-1]
                for sub_key in sub_keys:
                    try:
                        destination = destination[sub_key]
                    except KeyError:
                        destination[sub_key] = {}
                        destination = destination[sub_key]

                destination[key] = value
        return result

    def __emittable__(self):
        return self.render()


class PistonView(BasePistonView):
    __metaclass__ = PistonViewMetaclass
