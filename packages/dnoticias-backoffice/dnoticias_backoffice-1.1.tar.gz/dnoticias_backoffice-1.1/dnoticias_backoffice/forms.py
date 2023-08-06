from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from flags.models import FlagState
from flags.conditions import get_conditions, get_condition
from flags.sources import get_flags
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class FlagStateForm(forms.ModelForm):
    class Meta:
        model = FlagState
        fields = (
            "value",
            "required",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        available_conditions_choices = [
            [condition, condition] for condition in sorted(get_conditions())
        ]
        self.fields["condition"] = forms.ChoiceField(
            label=_("Condição"),
            choices=available_conditions_choices,
        )

        available_name_choices = [
            [condition, condition] for condition in sorted(get_flags().keys())
        ]
        self.fields["name"] = forms.ChoiceField(
            label=_("Nome"),
            choices=available_name_choices,
        )

        if self.instance.pk:
            self.initial["condition"] = self.instance.condition
            self.initial["name"] = self.instance.name

    def clean(self):
        cleaned_data = super().clean()
        condition_name = cleaned_data.get("condition")
        value = cleaned_data.get("value")
        condition = get_condition(condition_name)
        validator = getattr(condition, "validate")

        if validator is not None:
            try:
                validator(value)
            except Exception as e:
                raise forms.ValidationError(e)

        cleaned_data["value"] = value
        return cleaned_data

    def save(self, *args, **kwargs):
        commit = kwargs.pop("commit", True)
        kwargs["commit"] = False

        self.instance = super().save(*args, **kwargs)
        self.instance.name = self.cleaned_data["name"]
        self.instance.condition = self.cleaned_data["condition"]

        if commit:
            self.instance.save()

        return self.instance

class PermissionForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def save(self):
        user = self.cleaned_data["user"]
        
        user.groups.set(self.cleaned_data["groups"])

        user.user_permissions.set(self.cleaned_data["permissions"])

        return user