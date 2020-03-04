import spacy

class SpacyParser():
    
    """
    EA new POS tags:
    (Verb Quantifier-SP Punctuation-SP Pronoun Preposition Noun Interjection Determiner SubordinatingConjunction Conjunction
     OrdinalAdjective Number-SP AuxVerb Adverb Adjective)

    USED:
    Verb, Punctuation-SP, Pronoun, Preposition, Noun,
    Interjection, Determiner, Conjunction, Adverb, Adjective,
    Number-SP, AuxVerb, SubordinatingConjunction

    NOT USED:
    Quantifier-SP, OrdinalAdjective
    """
    SPACY_POS_TO_EA_LEXTAG = {
        "NOUN" : "Noun",
        "PRON" : "Pronoun",
        "VERB" : "Verb",
        "ADV" : "Adverb",
        "PUNCT" : "Punctuation-SP",
        "DET" : "Determiner",
        "ADJ" : "Adjective",
        "SYM" : "unknown",
        "X" : "unknown",
        "CONJ" : "Conjunction",
        "NUM" : "Number-SP", # (ordinal numbers "ordinal" not present in Spacy)
        "ADP" : "Preposition",
        "PROPN" : "pname",
        "PART" : "advpart",
        "SPACE" : "unknown",
        "INTJ" : "Interjection",
        "AUX" : "AuxVerb",
        "SCONJ" : "SubordinatingConjunction", # TODO: this doesn't work (might have to change that in lisp code)
        # Missing:
        # quant (quantifiers), name, scope (scope markers), unit, word (grammatical function words), 
        # misc, title (Title occurring before a proper name, e.g., Mr., Ms., etc)
    }
    
    def __init__(self):
        # load Spacy English model.
        self.nlp = spacy.load('en')
        
    def pos_tags(self, text):
        # Convert to a normal string and remove the " "
        text = str(text)[1:-1]
        doc = self.nlp(text)
        pos = [(token.text, self.SPACY_POS_TO_EA_LEXTAG[token.pos_]) for token in doc]
        return pos_list

    def dependency_parse(self, text):
        # Convert to a normal string and remove the " "
        text = str(text)[1:-1]
        dep = ["(%s %s %s)" % (token.dep_, str(token.head.i), str(token.i)) for token in doc]
        return dep
