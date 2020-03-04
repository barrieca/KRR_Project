from pythonian import Pythonian
import nltk
import logging

logger = logging.getLogger('NLTKAgent')

class NLTKAgent(Pythonian):
    name = "NLTKAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(NLTKAgent, self).__init__(**kwargs)
        self.add_achieve('pos_tag', self.pos_tag)
        self.add_ask('pos_tag', self.pos_tag, '(pos_tag ?text ?tags)')
        self.add_ask('subj_verb', self.subj_verb, '(subj_verb ?text ?subj ?verb)')

    def pos_tag(self, text):
        logger.debug('tagging ' + str(text))
        tokenized = nltk.word_tokenize(str(text))
        result = nltk.pos_tag(tokenized)
        return result

    def subj_verb(self, text):
        logger.debug('finding subject and verb in ' + str(text))
        tags = self.pos_tag(text)
        # this isn't actually right, don't worry, I know
        # I just want an example for returning bindings
        results = list()
        for pair in tags:
            if pair[1] == 'NN':
                results.append(pair[0])
        for pair in tags:
            if pair[1] == 'VBZ':
                results.append(pair[0])
        return results

        

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    a = NLTKAgent(host='localhost', port=9000, localPort=8950, debug=True)

