from translate import Translator

class Helpers(object):

    def translate_language(to_language, source, from_lnaguage = "en", status_translate=False):
        translator = Translator(from_lnag=from_lnaguage, to_lang=to_language)
        if (status_translate == False):
            return source
        return translator.translate(source)
