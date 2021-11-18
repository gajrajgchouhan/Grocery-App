from django import forms
from django.contrib.auth.forms import UserCreationForm
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
    """
    Form for adding grocery, it is a Model Form and
    uses the Grocery model in class Meta.
    The 4 fields are required and initial is set to 0 (Pending) for status.
    """

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
    """
    For filtering the grocery, Widget for selecting date is used.
    """

    date_filter = forms.DateField(widget=forms.SelectDateWidget())
