cdef class AnnotatedPhrase(Sentence):

    def __init__(self, wordIndex: int, tag: str):
        """
        Constructor for AnnotatedPhrase. AnnotatedPhrase stores information about phrases such as
        Shallow Parse phrases or named entity phrases.

        PARAMETERS
        ----------
        wordIndex : int
            Starting index of the first word in the phrase w.r.t. original sentence the phrase occurs.
        tag : str
            Tag of the phrase. Corresponds to the shallow parse or named entity tag.
        """
        super().__init__()
        self.__wordIndex = wordIndex
        self.__tag = tag

    cpdef int getWordIndex(self):
        """
        Accessor for the wordIndex attribute.

        RETURNS
        -------
        int
            Starting index of the first word in the phrase w.r.t. original sentence the phrase occurs.
        """
        return self.__wordIndex

    cpdef str getTag(self):
        """
        Accessor for the tag attribute.

        RETURNS
        -------
        str
            Tag of the phrase. Corresponds to the shallow parse or named entity tag.
        """
        return self.__tag
