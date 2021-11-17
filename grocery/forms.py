from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.forms.widgets import SelectDateWidget
from .models import Grocery, ProfileModel


class Profile(UserCreationForm):
    class Meta:
        model = ProfileModel
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class AddGrocery(forms.ModelForm):
    class Meta:
        model = Grocery
        fields = ["name", "quantity", "status", "date"]
        exclude = ["user"]
        widgets = {"date": SelectDateWidget()}

    def __init__(self, *args, **kwargs):
        super(AddGrocery, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["quantity"].required = True
        self.fields["status"].required = True
        self.fields["date"].required = True

        self.fields["status"].initial = 0


class FilterGrocery(forms.Form):
    date_filter = forms.DateField(widget=forms.SelectDateWidget())
