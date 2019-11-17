from itertools import chain

from django import forms
from django.db.utils import ProgrammingError

from tinymce.widgets import TinyMCE

from .models import Category

def generate_category_choices(category_fields):
    try:
        choices = list(chain([('', 'None')], 
                Category.objects.all().values_list(*category_fields)))
    except ProgrammingError:
        choices = (('', 'None'))

    return choices

class PostForm(forms.Form):
    category_id = forms.ChoiceField(
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=generate_category_choices(['id', 'name'])
        )
    title = forms.CharField(label="Title")
    content = forms.CharField(
            label="Content",
            widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
        )
    publish = forms.BooleanField(required=False, label="Publish")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category_id'] = forms.ChoiceField(
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=generate_category_choices(['id', 'name'])
        )


class PostSearchForm(forms.Form):
    category = forms.ChoiceField(
            required=False,
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=generate_category_choices(['name', 'name'])
        )
    title = forms.CharField(
            required=False,
            label="Title"
        )

    def __init__(self, *args, **kwargs):
        super(PostSearchForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
            required=False,
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=generate_category_choices(['name', 'name'])
        )


class DecipherForm(forms.Form):
    challenge = forms.CharField(
            required=False,
            label="Challenge",
            widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
        )
    clue = forms.CharField(
            required=False,
            label="Clue",
            widget=forms.Textarea(attrs={'class': 'materialize-textarea'})
        )
    code = forms.CharField(required=False, label="Code")
