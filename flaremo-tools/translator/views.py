from django.shortcuts import render
from .forms import TranslatorForm
from .utils import translate_large_text

def translator_view(request):
    result = None
    error = None

    if request.method == 'POST':
        form = TranslatorForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']

            try:
                result = translate_large_text(text, source, target)
            except Exception as e:
                error = str(e)
    else:
        form = TranslatorForm()

    return render(request, 'translator/index.html', {
        'form': form,
        'result': result,
        'error': error
    })