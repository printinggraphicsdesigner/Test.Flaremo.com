from django import forms

class WordToPdfForm(forms.Form):
    word_file = forms.FileField(
        label="Word ফাইল আপলোড করুন (.docx)",
        help_text="শুধুমাত্র .docx ফরম্যাট সমর্থিত"
    )