from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telephone = forms.CharField(required=True)
    adminname = forms.CharField(required=True)
    adminmail = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", \
            "telephone", "adminname", "adminmail")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.telephone = self.cleaned_data["telephone"]
        user.adminname = self.cleaned_data["adminname"]
        user.adminmail = self.cleaned_data["adminmail"]

        if commit:
            user.save()
        return user
