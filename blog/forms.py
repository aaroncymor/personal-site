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

    