cdef class SentenceAutoSemantic:

    cpdef autoLabelSingleSemantics(self, AnnotatedSentence sentence):
        """
        The method should set the senses of all words, for which there is only one possible sense.

        PARAMETERS
        ----------
        sentence: AnnotatedSentence
            The sentence for which word sense disambiguation will be determined automatically.
        """
        pass

    cpdef autoSemantic(self, AnnotatedSentence sentence):
        self.autoLabelSingleSemantics(sentence)
