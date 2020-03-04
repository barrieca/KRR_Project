from pythonian import Pythonian
from spacy_parser import SpacyParser
import logging

logger = logging.getLogger('SpacyAgent')

class SpacyAgent(Pythonian):
    """
    Agent serving as API to Spacy NLP.
    """

    name = "SpacyAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(SpacyAgent, self).__init__(**kwargs)
        self.spacy = SpacyParser()
        self.add_achieve('pos_tags', self.pos_tags)
        self.add_achieve('dependency_parse', self.dependency_parse)

    def pos_tags(self, content):
        # create return message.
        logger.debug("parsing sentence" + str(content))
        pos_tags = self.spacy.pos_tags(content)
        logger.debug("finished\n\n")
        return pos_tags

    def dependency_parse(self, content):
        # create return message.
        logger.debug("parsing sentence" + str(content))
        dependency_parse = self.spacy.dependency_parse(content)
        logger.debug("finished\n\n")
        return dependency_parse

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    a = SpacyAgent(host='localhost', port=9000, localPort=8950, debug=True)