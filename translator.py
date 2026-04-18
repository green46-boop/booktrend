from deep_translator import GoogleTranslator


def translate_titles(titles: list) -> list:
    try:
        translator = GoogleTranslator(source="auto", target="ko")
        return [translator.translate(t) or t for t in titles]
    except Exception:
        return titles
