from pythonian import *
import logging
import time

logger = logging.getLogger('GameAgent')

class GameAgent(Pythonian):
    name = "GameAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(GameAgent, self).__init__(**kwargs)

        self.add_achieve('some_achieve', self.some_achieve)
        self.add_ask('some_ask', self.some_ask, '(isa ?_input ?return)')

    def some_achieve(self):
        logger.debug('some_func')
        return '58'

    def some_ask(self, _input):
        logger.debug('testing ask with _input ' + str(_input))
        return "pass"

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    a = GameAgent(host='localhost', port=9000, localPort=8950, debug=True)

