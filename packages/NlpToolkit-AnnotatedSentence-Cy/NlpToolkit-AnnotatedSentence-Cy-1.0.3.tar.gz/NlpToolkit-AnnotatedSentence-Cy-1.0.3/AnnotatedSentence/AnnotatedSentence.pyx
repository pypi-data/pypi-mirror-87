from io import TextIOWrapper

from AnnotatedSentence.AnnotatedPhrase cimport AnnotatedPhrase
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse
from MorphologicalAnalysis.MetamorphicParse cimport MetamorphicParse


cdef class AnnotatedSentence(Sentence):

    def __init__(self, fileOrStr=None, fileName=None):
        """
        Converts a simple sentence to an annotated sentence

        PARAMETERS
        ----------
        fileOrStr
            Simple sentence
        """
        cdef list wordArray
        cdef str line, word
        self.words = []
        wordArray = []
        if fileOrStr is not None:
            if fileName is not None:
                self.__fileName = fileName
            if isinstance(fileOrStr, TextIOWrapper):
                line = fileOrStr.readline()
                wordArray = line.rstrip().split(" ")
            elif isinstance(self, str):
                wordArray = fileOrStr.split(" ")
            for word in wordArray:
                if len(word) > 0:
                    self.words.append(AnnotatedWord(word))

    cpdef list getShallowParseGroups(self):
        """
        The method constructs all possible shallow parse groups of a sentence.

        RETURNS
        -------
        list
            Shallow parse groups of a sentence.
        """
        cdef list shallowParseGroups
        cdef AnnotatedWord word, previousWord
        cdef AnnotatedPhrase current
        cdef int i
        shallowParseGroups = []
        previousWord = None
        current = None
        for i in range(self.wordCount()):
            word = self.getWord(i)
            if isinstance(word, AnnotatedWord):
                if previousWord is None:
                    current = AnnotatedPhrase(i, word.getShallowParse())
                else:
                    if isinstance(previousWord, AnnotatedWord) and previousWord.getShallowParse() is not None \
                            and previousWord.getShallowParse() != word.getShallowParse():
                        shallowParseGroups.append(current)
                        current = AnnotatedPhrase(i, word.getShallowParse())
                current.addWord(word)
                previousWord = word
        shallowParseGroups.append(current)
        return shallowParseGroups

    cpdef bint containsPredicate(self):
        """
        The method checks all words in the sentence and returns true if at least one of the words is annotated with
        PREDICATE tag.

        RETURNS
        -------
        bool
            True if at least one of the words is annotated with PREDICATE tag; False otherwise.
        """
        cdef AnnotatedWord word
        for word in self.words:
            if isinstance(word, AnnotatedWord):
                if word.getArgument() is not None and word.getArgument().getArgumentType() == "PREDICATE":
                    return True
        return False

    cpdef bint updateConnectedPredicate(self, str previousId, str currentId):
        cdef bint modified
        cdef AnnotatedWord word
        modified = False
        for word in self.words:
            if isinstance(word, AnnotatedWord):
                if word.getArgument() is not None and word.getArgument().getId() is not None and \
                        word.getArgument().getId() == previousId:
                    word.setArgument(word.getArgument().getArgumentType() + "$" + currentId)
                    modified = True
                if word.getFrameElement() is not None and word.getFrameElement().getId() is not None and \
                    word.getFrameElement().getId() == previousId:
                    word.setFrameElement(word.getFrameElement().getFrameElementType() + "$" + \
                                         word.getFrameElement().getFrame() + "$" + currentId)
                    modified = True
        return modified

    cpdef list predicateCandidates(self, FramesetList framesetList):
        """
        The method returns all possible words, which is
        1. Verb
        2. Its semantic tag is assigned
        3. A frameset exists for that semantic tag

        PARAMETERS
        ----------
        framesetList : FramesetList
            Frameset list that contains all frames for Turkish

        RETURNS
        -------
        A list of words, which are verbs, semantic tags assigned, and framesetlist assigned for that tag.
        """
        cdef list candidateList
        cdef AnnotatedWord word, annotatedWord, nextAnnotatedWord
        cdef int i, j
        candidateList = []
        for word in self.words:
            if isinstance(word, AnnotatedWord):
                if word.getParse() is not None and word.getParse().isVerb() and word.getSemantic() is not None \
                        and framesetList.frameExists(word.getSemantic()):
                    candidateList.append(word)
        for i in range(2):
            for j in range(len(self.words) - i - 1):
                annotatedWord = self.words[j]
                nextAnnotatedWord = self.words[j + 1]
                if isinstance(annotatedWord, AnnotatedWord) and isinstance(nextAnnotatedWord, AnnotatedWord):
                    if annotatedWord not in candidateList and nextAnnotatedWord in candidateList \
                            and annotatedWord.getSemantic() is not None \
                            and annotatedWord.getSemantic() == nextAnnotatedWord.getSemantic():
                        candidateList.append(annotatedWord)
        return candidateList

    cpdef list predicateFrameCandidates(self, FrameNet frameNet):
        """
        The method returns all possible words, which is
        1. Verb
        2. Its semantic tag is assigned
        3. A lexicalUnit exists for that semantic tag

        PARAMETERS
        ----------
        frameNet : FrameNet
            FrameNet that contains all frames for Turkish

        RETURNS
        -------
        A list of words, which are verbs, semantic tags assigned, and frame assigned for that tag.
        """
        cdef list candidateList
        cdef AnnotatedWord word, annotatedWord, nextAnnotatedWord
        cdef int i, j
        candidateList = []
        for word in self.words:
            if isinstance(word, AnnotatedWord):
                if word.getParse() is not None and word.getParse().isVerb() and word.getSemantic() is not None \
                        and frameNet.lexicalUnitExists(word.getSemantic()):
                    candidateList.append(word)
        for i in range(2):
            for j in range(len(self.words) - i - 1):
                annotatedWord = self.words[j]
                nextAnnotatedWord = self.words[j + 1]
                if isinstance(annotatedWord, AnnotatedWord) and isinstance(nextAnnotatedWord, AnnotatedWord):
                    if annotatedWord not in candidateList and nextAnnotatedWord in candidateList \
                            and annotatedWord.getSemantic() is not None \
                            and annotatedWord.getSemantic() == nextAnnotatedWord.getSemantic():
                        candidateList.append(annotatedWord)
        return candidateList

    cpdef str getPredicate(self, int index):
        """
        Returns the nearest predicate to the index'th word in the sentence.

        PARAMETERS
        ----------
        index : int
            Word index

        RETURNS
        -------
        str
            The nearest predicate to the index'th word in the sentence.
        """
        cdef int count1, count2, i
        cdef str data
        cdef list word, parse
        count1 = 0
        count2 = 0
        data = ""
        word = []
        parse = []
        if index < self.wordCount():
            for i in range(self.wordCount()):
                word.append(self.getWord(i))
                parse.append(self.getWord(i).getParse())
            for i in range(index, -1, -1):
                if parse[i] is not None and parse[i].getRootPos() is not None and parse[i].getPos() is not None \
                        and parse[i].getRootPos() == "VERB" and parse[i].getPos() == "VERB":
                    count1 = index - i
                    break
            for i in range(index, self.wordCount() - index):
                if parse[i] is not None and parse[i].getRootPos() is not None and parse[i].getPos() is not None \
                        and parse[i].getRootPos() == "VERB" and parse[i].getPos() == "VERB":
                    count2 = i - index
                    break
            if count1 > count2:
                data = word[count1].getName()
            else:
                data = word[count2].getName()
        return data

    cpdef str getFileName(self):
        """
        Returns file name of the sentence

        RETURNS
        -------
        str
            File name of the sentence
        """
        return self.__fileName

    cpdef removeWord(self, int index):
        """
        Removes the i'th word from the sentence

        PARAMETERS
        ----------
        index : int
            Word index
        """
        self.words.pop(index)

    cpdef str toStems(self):
        """
        The toStems method returns an accumulated string of each word's stems in words {@link ArrayList}.
        If the parse of the word does not exist, the method adds the surfaceform to the resulting string.

        RETURNS
        -------
        str
             String result which has all the stems of each item in words {@link ArrayList}.
        """
        cdef AnnotatedWord annotatedWord
        cdef str result
        cdef int i
        if len(self.words) > 0:
            annotatedWord = self.words[0]
            if annotatedWord.getParse() is not None:
                result = annotatedWord.getParse().getWord().getName()
            else:
                result = annotatedWord.getName()
            for i in range(1, len(self.words)):
                annotatedWord = self.words[i]
                if annotatedWord.getParse() is not None:
                    result = result + " " + annotatedWord.getParse().getWord().getName()
                else:
                    result = result + " " + annotatedWord.getName()
            return result
        else:
            return ""

    cpdef save(self):
        """
        Saves the current sentence.
        """
        self.writeToFile(self.__fileName)

    cpdef str getUniversalDependencyFormat(self):
        cdef str result
        cdef int i
        cdef AnnotatedWord word
        result = "# sent_id = " + self.getFileName() + "\n" + "# text = " + self.toString() + "\n"
        for i in range(self.wordCount()):
            word = self.getWord(i)
            result += str(i + 1) + "\t" + word.getUniversalDependencyFormat(self.wordCount()) + "\n"
        result += "\n"
        return result

    cpdef list constructLiterals(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, int wordIndex):
        """
        Creates a list of literal candidates for the i'th word in the sentence. It combines the results of
        1. All possible root forms of the i'th word in the sentence
        2. All possible 2-word expressions containing the i'th word in the sentence
        3. All possible 3-word expressions containing the i'th word in the sentence

        PARAMETERS
        ----------
        wordNet : WordNet
            Turkish wordnet
        fsm : FsmMorphologicalAnalyzer
            Turkish morphological analyzer
        wordIndex : int
            Word index

        RETURNS
        -------
        list
            List of literal candidates containing all possible root forms and multiword expressions.
        """
        cdef AnnotatedWord word, firstSucceedingWord, secondSucceedingWord
        cdef list possibleLiterals
        cdef MorphologicalParse morphologicalParse
        cdef MetamorphicParse metamorphicParse
        word = self.getWord(wordIndex)
        possibleLiterals = []
        if isinstance(word, AnnotatedWord):
            morphologicalParse = word.getParse()
            metamorphicParse = word.getMetamorphicParse()
            possibleLiterals.extend(wordNet.constructLiterals(morphologicalParse.getWord().getName(),
                                                              morphologicalParse, metamorphicParse, fsm))
            firstSucceedingWord = None
            secondSucceedingWord = None
            if self.wordCount() > wordIndex + 1:
                firstSucceedingWord = self.getWord(wordIndex + 1)
                if self.wordCount() > wordIndex + 2:
                    secondSucceedingWord = self.getWord(wordIndex + 2)
            if firstSucceedingWord is not None and isinstance(firstSucceedingWord, AnnotatedWord):
                if secondSucceedingWord is not None and isinstance(secondSucceedingWord, AnnotatedWord):
                    possibleLiterals.extend(wordNet.constructIdiomLiterals(fsm, word.getParse(),
                                                                           word.getMetamorphicParse(),
                                                                           firstSucceedingWord.getParse(),
                                                                           firstSucceedingWord.getMetamorphicParse(),
                                                                           secondSucceedingWord.getParse(),
                                                                           secondSucceedingWord.getMetamorphicParse()))
                possibleLiterals.extend(wordNet.constructIdiomLiterals(fsm, word.getParse(), word.getMetamorphicParse(),
                                                                       firstSucceedingWord.getParse(),
                                                                       firstSucceedingWord.getMetamorphicParse()))
        return possibleLiterals

    cpdef list constructSynSets(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, int wordIndex):
        """
        Creates a list of synset candidates for the i'th word in the sentence. It combines the results of
        1. All possible synsets containing the i'th word in the sentence
        2. All possible synsets containing 2-word expressions, which contains the i'th word in the sentence
        3. All possible synsets containing 3-word expressions, which contains the i'th word in the sentence

        PARAMETERS
        ----------
        wordNet : WordNet
            Turkish wordnet
        fsm : FsmMorphologicalAnalyzer
            Turkish morphological analyzer
        wordIndex : int
            Word index

        RETURNS
        -------
        list
            List of synset candidates containing all possible root forms and multiword expressions.
        """
        cdef AnnotatedWord word, firstPrecedingWord, secondPrecedingWord, firstSucceedingWord, secondSucceedingWord
        cdef list possibleSynSets
        cdef MorphologicalParse morphologicalParse
        cdef MetamorphicParse metamorphicParse
        word = self.getWord(wordIndex)
        possibleSynSets = []
        if isinstance(word, AnnotatedWord):
            morphologicalParse = word.getParse()
            metamorphicParse = word.getMetamorphicParse()
            possibleSynSets.extend(wordNet.constructSynSets(morphologicalParse.getWord().getName(),
                                                            morphologicalParse, metamorphicParse, fsm))
            firstPrecedingWord = None
            secondPrecedingWord = None
            firstSucceedingWord = None
            secondSucceedingWord = None
            if wordIndex > 0:
                firstPrecedingWord = self.getWord(wordIndex - 1)
                if wordIndex > 1:
                    secondPrecedingWord = self.getWord(wordIndex - 2)
            if self.wordCount() > wordIndex + 1:
                firstSucceedingWord = self.getWord(wordIndex + 1)
                if self.wordCount() > wordIndex + 2:
                    secondSucceedingWord = self.getWord(wordIndex + 2)
            if firstPrecedingWord is not None and isinstance(firstPrecedingWord, AnnotatedWord):
                if secondPrecedingWord is not None and isinstance(secondPrecedingWord, AnnotatedWord):
                    possibleSynSets.extend(wordNet.constructIdiomSynSets(fsm, secondPrecedingWord.getParse(),
                                                                         secondPrecedingWord.getMetamorphicParse(),
                                                                         firstPrecedingWord.getParse(),
                                                                         firstPrecedingWord.getMetamorphicParse(),
                                                                         word.getParse(), word.getMetamorphicParse()))
                possibleSynSets.extend(wordNet.constructIdiomSynSets(fsm, firstPrecedingWord.getParse(),
                                                                     firstPrecedingWord.getMetamorphicParse(),
                                                                     word.getParse(), word.getMetamorphicParse()))
            if firstSucceedingWord is not None and isinstance(firstSucceedingWord, AnnotatedWord):
                if secondSucceedingWord is not None and isinstance(secondSucceedingWord, AnnotatedWord):
                    possibleSynSets.extend(wordNet.constructIdiomSynSets(fsm, word.getParse(),
                                                                         word.getMetamorphicParse(),
                                                                         firstSucceedingWord.getParse(),
                                                                         firstSucceedingWord.getMetamorphicParse(),
                                                                         secondSucceedingWord.getParse(),
                                                                         secondSucceedingWord.getMetamorphicParse()))
                possibleSynSets.extend(wordNet.constructIdiomSynSets(fsm, word.getParse(), word.getMetamorphicParse(),
                                                                     firstSucceedingWord.getParse(),
                                                                     firstSucceedingWord.getMetamorphicParse()))
        return possibleSynSets
