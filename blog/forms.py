from django import forms

from tinymce.widgets import TinyMCE

CATEGORY_OPTIONS = (
    ('food', 'Food'),
    ('fitness', 'Fitness'),
    ('music', 'Music'),
    ('programming', 'Programming')
)

class PostForm(forms.Form):
    category = forms.ChoiceField(
            label="Category", 
            widget=forms.Select,
            choices=CATEGORY_OPTIONS
        )
    title = forms.CharField(label="Title")
    content = forms.CharField(
            label="Content",
            widget=TinyMCE(attrs={'cols': 80, 'rows':30})
        )
    publish = forms.BooleanField(label="Publish")




    