from django import forms
from django.forms.fields import CharField


class NewPageForm(forms.Form):
    title = CharField(label="Title:", widget=forms.TextInput(
        attrs={"class": "form-label"}))
    text = CharField(label="Enter the content of the Wiki:",
                     widget=forms.Textarea(attrs={"class": "form-label"}))
