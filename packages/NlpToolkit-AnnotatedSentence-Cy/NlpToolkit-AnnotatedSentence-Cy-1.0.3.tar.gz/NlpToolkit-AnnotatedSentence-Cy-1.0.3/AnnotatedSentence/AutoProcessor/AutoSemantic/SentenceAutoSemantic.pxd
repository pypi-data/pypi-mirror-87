from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence


cdef class SentenceAutoSemantic:

    cpdef autoLabelSingleSemantics(self, AnnotatedSentence sentence)
    cpdef autoSemantic(self, AnnotatedSentence sentence)
