from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelChoiceField
from django.http import Http404
from django.db import models
from profiles.models import Profile


class LoginAndPermissionRequiredMixin:
    permissions = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = self.request.get_full_path()
            return redirect_to_login(path)
        if self.kwargs.get('owner_pk'):
            try:
                owner = Profile.objects.get(pk=self.kwargs['owner_pk'])
            except Profile.DoesNotExist:
                raise Http404()
            if owner.user != request.user:
                raise PermissionDenied(f"Owner of {self} {owner} must has the same owner as request.user "
                                       f"{request.user} not {owner.user}")
        if self.permissions:
            for permission in self.permissions:
                if not request.user.has_perm(permission, obj=self.get_object()):
                    raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class MyModelChoiceField(ModelChoiceField):
    def __init__(self, queryset, old_model_choice_field):
        super().__init__(queryset=queryset)
        self._set_attrs(old_model_choice_field)

    def label_from_instance(self, obj):
        return obj.show_without_root

    def _set_attrs(self, old_model_choice_field):
        self.required = old_model_choice_field.required


class FormFieldValidation:
    def formfield(self, **kwargs):
        defaults = kwargs
        for validator in self.validators:
            if isinstance(validator, MaxValueValidator):
                defaults['max_value'] = validator.limit_value
            elif isinstance(validator, MinValueValidator):
                defaults['min_value'] = validator.limit_value
            else:
                pass
        return super().formfield(**defaults)


class ValidatedIntegerField(FormFieldValidation, models.IntegerField):
    pass


class ValidatedDecimalField(FormFieldValidation, models.DecimalField):
    pass
