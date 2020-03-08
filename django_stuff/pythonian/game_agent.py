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
        self.received = False
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

    def receive_tell(self, msg, content):
        """Override to store content and reply
        with nothing

        Arguments:
            msg {KQMLPerformative} -- tell to be passed along in reply
            content {KQMLPerformative} -- tell from companions to be logged
        """
        logger.debug('received tell: %s', content)  # lazy logging
        self.results = convert_to_list(content)
        reply_msg = KQMLPerformative('tell')
        reply_msg.set('sender', self.name)
        reply_msg.set('content', None)
        self.received = True
        self.reply(msg, reply_msg)

    def query(self, query):
        self.ask_agent('session-reasoner', query)
        iters = 0
        # check every 0.1 seconds (up to 100 times) until message received
        while not self.received:
            time.sleep(0.1)
            iters += 1
            if iters > 1000:
                self.received = True
                self.results = []
                break
        return self.results

    def get_games_with_attribute(self, attribute, value):
        results = self.query('(' + attribute + ' ?match ' + value + ')')
        return [re.match('(' + attribute + ' (\S+) ' + value + ')', str(item)).group(1) for item in results]

    def get_similar_games(self, game):
        game_mt = game + 'Mt'
        results = self.query('(reminding (KBCaseFn ' + game_mt + ') (CaseLibrarySansFn VideoGameCaseLibrary ' + game_mt + ') (TheSet) ?mostsimilar ?matchinfo)')
        result_list = []
        for item in results:
            matches = re.search('\(TheSet\) *(\S+) *\(.*\)\)', str(item))
            if matches != None:
                result_list.append(matches.group(1)[:-2])
        return result_list
        #return [re.search('\(TheSet\) *(\S+) *\(.*\)\)', str(item)).group(1)[:-2] for item in results]

    def get_game_facts(self, game):
        results = self.query('(?attribute ' + game + ' ?value)')
        facts_dict = {}
        for result in results:
            match_groups = re.match('\( *(\S+) +\S+ +(\S+) *\)', str(result))
            attribute = match_groups.group(1)
            if attribute in facts_dict.keys():
                facts_dict[attribute].append(match_groups.group(2))
            else:
                facts_dict[attribute] = [match_groups.group(2)]
        for key in facts_dict.keys():
            facts_dict[key] = tuple(facts_dict[key])
        return facts_dict

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

