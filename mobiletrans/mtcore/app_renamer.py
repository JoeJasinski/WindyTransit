from django.db.models.base import ModelBase
from django.core.urlresolvers import resolve
from django.contrib import admin

class AppLabelRenamer(object):
    ''' Rename app label and app breadcrumbs in admin. '''

    def __init__(self, native_app_label, app_label):
        self.native_app_label = native_app_label
        self.app_label = app_label
        self.module = '.'.join([native_app_label, 'models'])

    class string_with_realoaded_title(str):
        ''' tnx to Ionel Maries Cristian for http://ionelmc.wordpress.com/2011/06/24/custom-app-names-in-the-django-admin/'''
        def __new__(cls, value, title):
            instance = str.__new__(cls, value)
            instance._title = title
            return instance

        def title(self):
            return self._title

        __copy__ = lambda self: self
        __deepcopy__ = lambda self, memodict: self

    def rename_app_label(self, f):
        app_label = self.app_label

        def rename_breadcrumbs(f):
            def wrap(self, *args, **kwargs):
                extra_context = kwargs.get('extra_context', {})
                extra_context['app_label'] = app_label
                kwargs['extra_context'] = extra_context
                return f(self, *args, **kwargs)
            return wrap

        def wrap(model_or_iterable, admin_class=None, **option):
            if isinstance(model_or_iterable, ModelBase):
                model_or_iterable = [model_or_iterable]
            for model in model_or_iterable:
                if model.__module__ != self.module:
                    continue
                if admin_class is None:
                    admin_class = type(model.__name__+'Admin',
                                       (admin.ModelAdmin,), {})
                admin_class.add_view = rename_breadcrumbs(admin_class.add_view)
                admin_class.change_view = rename_breadcrumbs(admin_class.change_view)
                admin_class.changelist_view = rename_breadcrumbs(admin_class.changelist_view)
                model._meta.app_label = self.string_with_realoaded_title(
                    self.native_app_label,
                    self.app_label)
            return f(model, admin_class, **option)
        return wrap

    def rename_app_index(self, f):
        def wrap(request, app_label, extra_context=None):
            requested_app_label = resolve(request.path).kwargs.get('app_label', '')
            if requested_app_label and requested_app_label == self.native_app_label:
                app_label = self.string_with_realoaded_title(self.native_app_label,
                                                             self.app_label)
            else:
                app_label = requested_app_label
            return f(request, app_label, extra_context=None)
        return wrap

    def main(self):
        admin.site.register = self.rename_app_label(admin.site.register)
        admin.site.app_index = self.rename_app_index(admin.site.app_index)
