from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

FORM_CSS_CLASS = "form-control form-control-lg"


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": FORM_CSS_CLASS,
                "placeholder": "Username",
                "autocomplete": None,
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": FORM_CSS_CLASS,
                "placeholder": "Password",
                "autocomplete": None,
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "id": "remember_me",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for username field
        self.fields["username"].help_text = "Username"


class CustomSignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": FORM_CSS_CLASS,
                "placeholder": "Username",
                "autocomplete": None,
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": FORM_CSS_CLASS,
                "placeholder": "Password",
                "autocomplete": None,
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": FORM_CSS_CLASS,
                "placeholder": "Confirm Password",
                "autocomplete": None,
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove default help text for cleaner appearance
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
