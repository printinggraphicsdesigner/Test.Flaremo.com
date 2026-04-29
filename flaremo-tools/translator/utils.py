import re
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

MAX_CHUNK = 4000  # আগে 1000 ছিল → এখন বড় করলাম

def smart_split(text):
    sentences = re.split(r'(?<=[.!?।]) +', text)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < MAX_CHUNK:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


def translate_chunk(chunk, source, target):
    return GoogleTranslator(source=source, target=target).translate(chunk)


def translate_large_text(text, source, target):
    chunks = smart_split(text)

    results = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(translate_chunk, c, source, target)
            for c in chunks
        ]

        for future in futures:
            try:
                results.append(future.result())
            except:
                results.append("")

    return " ".join(results)