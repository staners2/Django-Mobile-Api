from translate import Translator

class Helpers(object):

    def translate_language(from_lnaguage, to_language, source):
        translator = Translator(from_lnag=from_lnaguage, to_lang=to_language)
        return translator.translate(source)
