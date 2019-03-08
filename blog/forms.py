from itertools import chain

from django import forms

from tinymce.widgets import TinyMCE

from .models import Category

class PostForm(forms.Form):
    category_id = forms.ChoiceField(
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=Category.objects.all().values_list('id', 'name')
        )
    title = forms.CharField(label="Title")
    content = forms.CharField(
            label="Content",
            widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
        )
    publish = forms.BooleanField(required=False, label="Publish")


class PostSearchForm(forms.Form):
    category = forms.ChoiceField(
            required=False,
            label="Category", 
            widget=forms.Select(attrs={'class': 'input-field'}),
            choices=list(chain([('', 'None')], Category.objects.all().values_list('name', 'name')))
        )
    title = forms.CharField(
            required=False,
            label="Title"
        )


class DecipherForm(forms.Form):
    challenge = forms.CharField(
            label="Challenge",
            widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
        )
    clue = forms.CharField(
            label="Clue",
            widget=forms.Textarea(attrs={'class': 'materialize-textarea'})
        )
    code = forms.CharField(label="Code")