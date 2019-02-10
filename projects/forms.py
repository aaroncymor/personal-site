from django import forms

from .models import Project

from tinymce.widgets import TinyMCE

class ProjectForm(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(
        label="Description",
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )
    rank = forms.ChoiceField(
            choices=Project.objects.get_rank_choices(),
            widget=forms.Select(attrs={'class': 'input-field'}), 
            required=False
    )
