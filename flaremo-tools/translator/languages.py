from deep_translator import GoogleTranslator

def get_languages():
    langs = GoogleTranslator().get_supported_languages(as_dict=True)

    return [('auto', '🌐 Auto Detect')] + [
        (code, f"{name.title()} ({code})") for name, code in langs.items()
    ]

LANGUAGES = get_languages()