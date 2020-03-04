from pythonian import *
import logging
import time

logger = logging.getLogger('GameAgent')

class GameAgent(Pythonian):
    name = "GameAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(GameAgent, self).__init__(**kwargs)

        self.facts = []

        self.add_achieve('some_achieve', self.some_achieve)
        self.add_ask('some_ask', self.some_ask, '(isa ?_input ?return)')

    def receive_tell(self, msg, content):
        """Override to store content and reply
        with nothing

        Arguments:
            msg {KQMLPerformative} -- tell to be passed along in reply
            content {KQMLPerformative} -- tell from companions to be logged
        """
        logger.debug('received tell: %s', content)  # lazy logging
        self.facts += convert_to_list(content)
        reply_msg = KQMLPerformative('tell')
        reply_msg.set('sender', self.name)
        reply_msg.set('content', None)
        self.reply(msg, reply_msg)

    def some_achieve(self):
        logger.debug('some_func')
        return '58'

    def some_ask(self, _input):
        logger.debug('testing ask with _input ' + str(_input))
        return "pass"

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    a = GameAgent(host='localhost', port=9000, localPort=8950, debug=True)
    print(a.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)'))

