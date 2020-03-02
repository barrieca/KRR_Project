from pythonian import Pythonian
from ml.ml import learn

import logging

logger = logging.getLogger('MLAgent')


class MLAgent(Pythonian):
    name = "MLAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(MLAgent, self).__init__(**kwargs)

        self.add_achieve('test_ml', self.test_ml)
        self.add_achieve('learn', self.learn)

        # self.add_ask('test_return', self.test_return, '(info ?text)')
        # self.add_ask('learn', self.learn, '(learn ?labels ?stuff)')



    def test_ml(self, content):
        # create return message.
        logger.debug('more junk mail has arrived')
        return "ok"



    def learn(self, labels, feats, out):
        # logger.debug('calling the learn function with input', labels, feats, out)
        logger.debug("ooh yeah")
        return learn(labels, feats, out)



        

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    a = MLAgent(host='localhost', port=9000, localPort=8950, debug=True)

