from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telephone = forms.CharField(required=True)
    team_manager = forms.CharField(required=True)
    team_manager_email = forms.EmailField(required=True)
    administrator = forms.CharField(required=True)
    admin_email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "telephone", \
            "team_manager", "team_manager_email", "administrator", "admin_email")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.telephone = self.cleaned_data["telephone"]
        user.team_manager = self.cleaned_data["team_manager"]
        user.team_manager_email = self.cleaned_data["team_manager_email"]
        user.administrator = self.cleaned_data["administrator"]
        user.admin_email = self.cleaned_data["admin_email"]

        if commit:
            user.save()
        return user
