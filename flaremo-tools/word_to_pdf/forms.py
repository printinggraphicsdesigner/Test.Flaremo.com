from django import forms

class WordToPdfForm(forms.Form):
    word_file = forms.FileField(
        label="Upload Word File (.docx)",
        help_text="only .docx format supported"
    )
