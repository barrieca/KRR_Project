from pythonian.pythonian import *
# from pythonian import *
import logging
import time
import re

logger = logging.getLogger('GameAgent')

class GameAgent(Pythonian):
    name = "GameAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(GameAgent, self).__init__(**kwargs)

        self.results = []
        self.received = True

        self.add_achieve('some_achieve', self.some_achieve)
        self.add_ask('some_ask', self.some_ask, '(isa ?_input ?return)')

    def ask_agent(self, receiver, data, query_type='user::query'):
        msg = KQMLPerformative('ask-all')
        msg.set('sender', self.name)
        msg.set('receiver', receiver)
        if isinstance(data, KQMLList):
            msg.set('content', data)
        else:
            msg.set('content', listify(data))
        msg.set('query-type', query_type)
        self.connect(self.host, self.port)
        self.send(msg)
        self.received = False

    def receive_tell(self, msg, content):
        """Override to store content and reply
        with nothing

        Arguments:
            msg {KQMLPerformative} -- tell to be passed along in reply
            content {KQMLPerformative} -- tell from companions to be logged
        """
        logger.debug('received tell: %s', content)  # lazy logging
        self.results = convert_to_list(content)
        self.received = True
        reply_msg = KQMLPerformative('tell')
        reply_msg.set('sender', self.name)
        reply_msg.set('content', None)
        self.reply(msg, reply_msg)

    def query(self, query):
        self.ask_agent('session-reasoner', query)
        while not self.received:
            time.sleep(0.1) # check every 0.1 seconds until message received
        return self.results

    def get_games_with_attribute(self, attribute, value):
        results = self.query('(' + attribute + ' ?match ' + value + ')')
        return [re.match('(' + attribute + ' (\S+) ' + value + ')', str(item)).group(1) for item in results]

    def get_game_facts(self, game_mt):
        # need to ensure proper usage of this
        results = self.query('(reminding (KBCaseFn ' + game_mt + ') VideoGameCaseLibrary ?mostsimilar ?matchinfo)')
        games = [re.match('(\S+) *\(.*\)\)$', str(item)).group(1)[:-2] for item in results]
        game_facts = {}
        for game in games:
            results = self.query_agent('(get_attributes ' + game + '?attribute)')
            game_facts[game] = tuple([re.match('(\S+) *\)$', str(item)).group(1) for item in results])
        return game_facts

    def get_isa(self, what_it_is):
        results = self.query('(isa ?match ' + what_it_is + ')')
        return [re.match('\(isa (\S+)', str(item)).group(1) for item in results]

    def some_achieve(self):
        logger.debug('some_func')
        return '58'

    def some_ask(self, _input):
        logger.debug('testing ask with _input ' + str(_input))
        return "pass"

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    # a = GameAgent(host='localhost', port=9000, localPort=8950, debug=True)
    # a.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)')

