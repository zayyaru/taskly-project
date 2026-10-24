from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Task


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "အသုံးပြုသူအမည်"
        self.fields["password"].label = "စကားဝှက်"
        for field in self.fields.values():
            field.widget.attrs["class"] = "input"


class SignUpForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "စကားဝှက် နှစ်ခု မတူညီပါ။",
    }

    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "username": "အသုံးပြုသူအမည်",
            "password1": "စကားဝှက်",
            "password2": "စကားဝှက် အတည်ပြု",
        }
        for name, field in self.fields.items():
            field.label = labels.get(name, field.label)
            field.help_text = ""
            field.widget.attrs["class"] = "input"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "details", "priority", "status", "due_date")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input", "placeholder": "ဥပမာ၊ အစီရင်ခံစာ ရေးရန်"}
            ),
            "details": forms.Textarea(
                attrs={
                    "class": "input",
                    "rows": 4,
                    "placeholder": "မှတ်ချက် ထည့်ချင်မှ ထည့်ပါ",
                }
            ),
            "priority": forms.Select(attrs={"class": "input"}),
            "status": forms.Select(attrs={"class": "input"}),
            "due_date": forms.DateInput(attrs={"class": "input", "type": "date"}),
        }
