# -*- coding: utf-8 -*-
from pysbd.languages import Language
from pysbd.processor import Processor
from pysbd.cleaner import Cleaner

class Segmenter(object):

    def __init__(self, language="en", clean=False, doc_type=None, char_span=False):
        """Segments a text into an list of sentences
        with or withour character offsets from original text

        Parameters
        ----------
        language : str, optional
            specify a language use its two character ISO 639-1 code,
            by default "en"
        clean : bool, optional
            cleans original text, by default False
        doc_type : [type], optional
            Normal text or OCRed text, by default None
            set to `pdf` for OCRed text
        char_span : bool, optional
            Get start & end character offsets of each sentences
            within original text, by default False
        """
        self.language = language
        self.language_module = Language.get_language_code(language)
        self.clean = clean
        self.doc_type = doc_type
        self.char_span = char_span

    def cleaner(self, text):
        if hasattr(self.language_module, "Cleaner"):
            return self.language_module.Cleaner(text, self.language_module,
                                                doc_type=self.doc_type)
        else:
            return Cleaner(text, self.language_module, doc_type=self.doc_type)

    def processor(self, text):
        if hasattr(self.language_module, "Processor"):
            return self.language_module.Processor(text, self.language_module,
                                                  char_span=self.char_span)
        else:
            return Processor(text, self.language_module,
                             char_span=self.char_span)

    def segment(self, text):
        if not text:
            return []
        if self.clean and self.char_span:
            raise ValueError("char_span must be False if clean is True. "
                             "Since `clean=True` will modify original text.")
        if self.language != 'en' and self.char_span:
            raise ValueError("char_span functionality not supported for "
                             "languages other than English (`en`)")
        elif self.clean:
            text = self.cleaner(text).clean()
        segments = self.processor(text).process()
        return segments
