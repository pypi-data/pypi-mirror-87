from Corpus.Sentence cimport Sentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from PropBank.FramesetList cimport FramesetList
from FrameNet.FrameNet cimport FrameNet
from WordNet.WordNet cimport WordNet


cdef class AnnotatedSentence(Sentence):

    cdef str __fileName

    cpdef list getShallowParseGroups(self)
    cpdef bint containsPredicate(self)
    cpdef bint updateConnectedPredicate(self, str previousId, str currentId)
    cpdef list predicateCandidates(self, FramesetList framesetList)
    cpdef list predicateFrameCandidates(self, FrameNet frameNet)
    cpdef str getPredicate(self, int index)
    cpdef str getFileName(self)
    cpdef removeWord(self, int index)
    cpdef str toStems(self)
    cpdef save(self)
    cpdef str getUniversalDependencyFormat(self)
    cpdef list constructLiterals(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, int wordIndex)
    cpdef list constructSynSets(self, WordNet wordNet, FsmMorphologicalAnalyzer fsm, int wordIndex)
