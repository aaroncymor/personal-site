from django import forms

from tinymce.widgets import TinyMCE

class ProjectForm(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(
        label="Description",
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )
