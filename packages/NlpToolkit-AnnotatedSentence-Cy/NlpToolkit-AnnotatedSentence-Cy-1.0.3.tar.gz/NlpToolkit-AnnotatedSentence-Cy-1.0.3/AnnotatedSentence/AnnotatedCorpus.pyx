import os
import re
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord


cdef class AnnotatedCorpus(Corpus):

    def __init__(self, folder: str, pattern: str = None):
        """
        A constructor of AnnotatedCorpus class which reads all AnnotatedSentence files with the file
        name satisfying the given pattern inside the given folder. For each file inside that folder, the constructor
        creates an AnnotatedSentence and puts in inside the list parseTrees.

        PARAMETERS
        ----------
        folder : str
            Folder where all sentences reside.
        pattern : str
            File pattern such as "." ".train" ".test".
        """
        cdef str fileName
        cdef AnnotatedSentence sentence
        self.sentences = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                fileName = os.path.join(root, file)
                if (pattern is None or pattern in fileName) and re.match("\\d+\\.", file):
                    f = open(fileName, "r", encoding='utf8')
                    sentence = AnnotatedSentence(f, fileName)
                    self.sentences.append(sentence)

    cpdef exportUniversalDependencyFormat(self, str outputFileName):
        cdef int i
        cdef AnnotatedSentence sentence
        file = open(outputFileName, "w")
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            file.write(sentence.getUniversalDependencyFormat())
        file.close()

    cpdef checkMorphologicalAnalysis(self):
        """
        The method traverses all words in all sentences and prints the words which do not have a morphological analysis.
        """
        cdef int i, j
        cdef AnnotatedSentence sentence
        cdef AnnotatedWord word
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            if isinstance(sentence, AnnotatedSentence):
                for j in range(sentence.wordCount()):
                    word = sentence.getWord(j)
                    if isinstance(word, AnnotatedWord):
                        if word.getParse() is None:
                            print("Morphological Analysis does not exist for sentence " + sentence.getFileName())
                            break

    cpdef checkNer(self):
        """
        The method traverses all words in all sentences and prints the words which do not have named entity annotation.
        """
        cdef int i, j
        cdef AnnotatedSentence sentence
        cdef AnnotatedWord word
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            if isinstance(sentence, AnnotatedSentence):
                for j in range(sentence.wordCount()):
                    word = sentence.getWord(j)
                    if isinstance(word, AnnotatedWord):
                        if word.getNamedEntityType() is None:
                            print("NER annotation does not exist for sentence " + sentence.getFileName())
                            break

    cpdef checkShallowParse(self):
        """
        The method traverses all words in all sentences and prints the words which do not have shallow parse annotation.
        """
        cdef int i, j
        cdef AnnotatedSentence sentence
        cdef AnnotatedWord word
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            if isinstance(sentence, AnnotatedSentence):
                for j in range(sentence.wordCount()):
                    word = sentence.getWord(j)
                    if isinstance(word, AnnotatedWord):
                        if word.getShallowParse() is None:
                            print("Shallow parse annotation does not exist for sentence " + sentence.getFileName())
                            break

    cpdef checkSemantic(self):
        """
        The method traverses all words in all sentences and prints the words which do not have sense annotation.
        """
        cdef int i, j
        cdef AnnotatedSentence sentence
        cdef AnnotatedWord word
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            if isinstance(sentence, AnnotatedSentence):
                for j in range(sentence.wordCount()):
                    word = sentence.getWord(j)
                    if isinstance(word, AnnotatedWord):
                        if word.getSemantic() is None:
                            print("Semantic annotation does not exist for sentence " + sentence.getFileName())
                            break
