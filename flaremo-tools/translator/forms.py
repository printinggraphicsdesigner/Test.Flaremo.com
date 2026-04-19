from django import forms
from .languages import LANGUAGES

class TranslatorForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full border p-4 rounded-2xl',
            'rows': 8,
            'placeholder': 'Paste your text here...'
        })
    )

    source = forms.ChoiceField(
        choices=LANGUAGES,
        widget=forms.Select(attrs={'class': 'w-full border p-2 rounded-xl'})
    )

    target = forms.ChoiceField(
        choices=LANGUAGES,
        widget=forms.Select(attrs={'class': 'w-full border p-2 rounded-xl'})
    )