import re
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag
from MorphologicalAnalysis.FsmParse cimport FsmParse
from AnnotatedSentence.ViewLayerType import ViewLayerType
from Corpus.WordFormat import WordFormat
from NamedEntityRecognition.NamedEntityType import NamedEntityType


cdef class AnnotatedWord(Word):

    def __init__(self, word: str, layerType=None):
        """
        Constructor for the AnnotatedWord class. Gets the word with its annotation layers as input and sets the
        corresponding layers.

        PARAMETERS
        ----------
        word : str
            Input word with annotation layers
        """
        cdef list splitLayers, values
        cdef str layer, layerValue
        self.__parse = None
        self.__metamorphicParse = None
        self.__semantic = None
        self.__namedEntityType = None
        self.__argument = None
        self.__frameElement = None
        self.__shallowParse = None
        self.__universalDependency = None
        if layerType is None:
            splitLayers = re.compile("[{}]").split(word)
            for layer in splitLayers:
                if len(layer) == 0:
                    continue
                if "=" not in layer:
                    self.name = layer
                    continue
                layerType = layer[:layer.index("=")]
                layerValue = layer[layer.index("=") + 1:]
                if layerType == "turkish":
                    self.name = layerValue
                elif layerType == "morphologicalAnalysis":
                    self.__parse = MorphologicalParse(layerValue)
                elif layerType == "metaMorphemes":
                    self.__metamorphicParse = MetamorphicParse(layerValue)
                elif layerType == "namedEntity":
                    self.__namedEntityType = NamedEntityType.getNamedEntityType(layerValue)
                elif layerType == "propbank":
                    self.__argument = Argument(layerValue)
                elif layerType == "framenet":
                    self.__frameElement = FrameElement(layerValue)
                elif layerType == "shallowParse":
                    self.__shallowParse = layerValue
                elif layerType == "semantics":
                    self.__semantic = layerValue
                elif layerType == "universalDependency":
                    values = layerValue.split("$")
                    self.__universalDependency = UniversalDependencyRelation(int(values[0]), values[1])
        elif isinstance(layerType, NamedEntityType):
            super().__init__(word)
            self.__namedEntityType = layerType
            self.__argument = Argument("NONE")
        elif isinstance(layerType, MorphologicalParse):
            super().__init__(word)
            self.__parse = layerType
            self.__namedEntityType = NamedEntityType.NONE
            self.__argument = Argument("NONE")
        elif isinstance(layerType, FsmParse):
            super().__init__(word)
            self.__parse = layerType
            self.__namedEntityType = NamedEntityType.NONE
            self.setMetamorphicParse(layerType.withList())
            self.__argument = Argument("NONE")

    def __str__(self) -> str:
        """
        Converts an AnnotatedWord to string. For each annotation layer, the method puts a left brace, layer name,
        equal sign and layer value finishing with right brace.

        RETURNS
        -------
        str
            String form of the AnnotatedWord.
        """
        cdef str result
        result = "{turkish=" + self.name + "}"
        if self.__parse is not None:
            result = result + "{morphologicalAnalysis=" + self.__parse.__str__() + "}"
        if self.__metamorphicParse is not None:
            result = result + "{metaMorphemes=" + self.__metamorphicParse.__str__() + "}"
        if self.__semantic is not None:
            result = result + "{semantics=" + self.__semantic + "}"
        if self.__namedEntityType is not None:
            result = result + "{namedEntity=" + NamedEntityType.getNamedEntityString(self.__namedEntityType) + "}"
        if self.__argument is not None:
            result = result + "{propbank=" + self.__argument.__str__() + "}"
        if self.__frameElement is not None:
            result = result + "{framenet=" + self.__frameElement.__str__() + "}"
        if self.__shallowParse is not None:
            result = result + "{shallowParse=" + self.__shallowParse + "}"
        if self.__universalDependency is not None:
            result = result + "{universalDependency=" + self.__universalDependency.to().__str__() + "$" + \
                     self.__universalDependency.__str__() + "}"
        return result

    cpdef str getLayerInfo(self, object viewLayerType):
        """
        Returns the value of a given layer.

        PARAMETERS
        ----------
        viewLayerType : ViewLayerType
            Layer for which the value questioned.

        RETURNS
        -------
        str
            The value of the given layer.
        """
        if viewLayerType == ViewLayerType.INFLECTIONAL_GROUP:
            if self.__parse is not None:
                return self.__parse.__str__()
        elif viewLayerType == ViewLayerType.META_MORPHEME:
            if self.__metamorphicParse is not None:
                return self.__metamorphicParse.__str__()
        elif viewLayerType == ViewLayerType.SEMANTICS:
            return self.__semantic
        elif viewLayerType == ViewLayerType.NER:
            if self.__namedEntityType is not None:
                return self.__namedEntityType.__str__()
        elif viewLayerType == ViewLayerType.SHALLOW_PARSE:
            return self.__shallowParse
        elif viewLayerType == ViewLayerType.TURKISH_WORD:
            return self.name
        elif viewLayerType == ViewLayerType.PROPBANK:
            if self.__argument is not None:
                return self.__argument.__str__()
        elif viewLayerType == ViewLayerType.FRAMENET:
            if self.__frameElement is not None:
                return self.__frameElement.__str__()
        elif viewLayerType == ViewLayerType.DEPENDENCY:
            if self.__universalDependency is not None:
                return self.__universalDependency.to().__str__() + "$" + self.__universalDependency.__str__()
        else:
            return None

    cpdef MorphologicalParse getParse(self):
        """
        Returns the morphological parse layer of the word.

        RETURNS
        -------
        MorphologicalParse
            The morphological parse of the word.
        """
        return self.__parse

    cpdef setParse(self, MorphologicalParse parseString):
        """
        Sets the morphological parse layer of the word.

        PARAMETERS
        ----------
        parseString : str
            The new morphological parse of the word in string form.
        """
        if parseString is not None:
            self.__parse = MorphologicalParse(parseString)
        else:
            self.__parse = None

    cpdef MetamorphicParse getMetamorphicParse(self):
        """
        Returns the metamorphic parse layer of the word.

        RETURNS
        -------
        MetamorphicParse
            The metamorphic parse of the word.
        """
        return self.__metamorphicParse

    cpdef setMetamorphicParse(self, str parseString):
        """
        Sets the metamorphic parse layer of the word.

        PARAMETERS
        ----------
        parseString : str
            The new metamorphic parse of the word in string form.
        """
        self.__metamorphicParse = MetamorphicParse(parseString)

    cpdef str getSemantic(self):
        """
        Returns the semantic layer of the word.

        RETURNS
        -------
        str
            Sense id of the word.
        """
        return self.__semantic

    cpdef setSemantic(self, str semantic):
        """
        Sets the semantic layer of the word.

        PARAMETERS
        ----------
        semantic : str
            New sense id of the word.
        """
        self.__semantic = semantic

    cpdef object getNamedEntityType(self):
        """
        Returns the named entity layer of the word.

        RETURNS
        -------
        NamedEntityType
            Named entity tag of the word.
        """
        return self.__namedEntityType

    cpdef setNamedEntityType(self, str namedEntity):
        """
        Sets the named entity layer of the word.

        PARAMETERS
        ----------
        namedEntity : str
            New named entity tag of the word.
        """
        if namedEntity is not None:
            self.__namedEntityType = NamedEntityType.getNamedEntityType(namedEntity)
        else:
            self.__namedEntityType = None

    cpdef Argument getArgument(self):
        """
        Returns the semantic role layer of the word.

        RETURNS
        -------
        Argument
            Semantic role tag of the word.
        """
        return self.__argument

    cpdef setArgument(self, str argument):
        """
        Sets the semantic role layer of the word.

        PARAMETERS
        ----------
        argument : Argument
            New semantic role tag of the word.
        """
        if self.__argument is not None:
            self.__argument = Argument(argument)
        else:
            self.__argument = None

    cpdef FrameElement getFrameElement(self):
        """
        Returns the framenet layer of the word.

        RETURNS
        -------
        FrameElement
            Framenet tag of the word.
        """
        return self.__frameElement

    cpdef setFrameElement(self, str frameElement):
        """
        Sets the framenet layer of the word.

        PARAMETERS
        ----------
        frameElement : str
            New framenet tag of the word.
        """
        if self.__frameElement is not None:
            self.__frameElement = Argument(frameElement)
        else:
            self.__frameElement = None

    cpdef str getShallowParse(self):
        """
        Returns the shallow parse layer of the word.

        RETURNS
        -------
        str
            Shallow parse tag of the word.
        """
        return self.__shallowParse

    cpdef setShallowParse(self, str parse):
        """
        Sets the shallow parse layer of the word.

        PARAMETERS
        ----------
        parse : str
            New shallow parse tag of the word.
        """
        self.__shallowParse = parse

    cpdef UniversalDependencyRelation getUniversalDependency(self):
        """
        Returns the universal dependency layer of the word.

        RETURNS
        -------
        UniversalDependencyRelation
            Universal dependency relation of the word.
        """
        return self.__universalDependency

    cpdef setUniversalDependency(self, int to, str dependencyType):
        """
        Sets the universal dependency layer of the word.

        PARAMETERS
        ----------
        to : int
            to Word related to.
        dependencyType : str
            type of dependency the word is related to.
        """
        self.__universalDependency = UniversalDependencyRelation(to, dependencyType)

    cpdef str getUniversalDependencyFormat(self, int sentenceLength):
        cdef str result
        cdef list features
        cdef bint first
        if self.__parse is not None:
            result = self.name + "\t" + self.__parse.getWord().getName() + "\t" + \
                     self.__parse.getUniversalDependencyPos() + "\t_\t"
            features = self.__parse.getUniversalDependencyFeatures()
            if len(features) == 0:
                result = result + "_"
            else:
                first = True
                for feature in features:
                    if first:
                        first = False
                    else:
                        result += "|"
                    result += feature
            result += "\t"
            if self.__universalDependency is not None and self.__universalDependency.to() <= sentenceLength:
                result += self.__universalDependency.to().__str__() + "\t" + \
                          self.__universalDependency.__str__().lower() + "\t"
            else:
                result += "_\t_\t"
            result += "_\t_"
            return result
        else:
            return self.name + "\t" + self.name + "\t_\t_\t_\t_\t_\t_\t_"

    cpdef getFormattedString(self, object wordFormat):
        if wordFormat == WordFormat.SURFACE:
            return self.name
        return self.name

    cpdef checkGazetteer(self, Gazetteer gazetteer):
        cdef str wordLowercase
        wordLowercase = self.name.lower()
        if gazetteer.contains(wordLowercase) and self.__parse.containsTag(MorphologicalTag.PROPERNOUN):
            self.setNamedEntityType(gazetteer.getName())
        if "'" in wordLowercase and gazetteer.contains(wordLowercase[:wordLowercase.index("'")]) and \
                self.__parse.containsTag(MorphologicalTag.PROPERNOUN):
            self.setNamedEntityType(gazetteer.getName())
