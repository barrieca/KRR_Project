from pythonian.pythonian import *
# from pythonian import *
import logging
import time
import re

logger = logging.getLogger('GameAgent')

class GameAgent(Pythonian):
    '''
    Pythonian agent for communicating with Companions.
    '''
    name = "GameAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(GameAgent, self).__init__(**kwargs)

        self.results = []
        self.received = True

        self.add_achieve('some_achieve', self.some_achieve)
        self.add_ask('some_ask', self.some_ask, '(isa ?_input ?return)')

    def ask_agent(self, receiver, data, query_type='user::query'):
        '''
        sends a query to Companions
        :param receiver - the agent to send the query to (usually 'session-reasoner')
        :param data - the query to send to Companions
        :param query_type - should be left as default for internal usage
        '''
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
        '''
        overridden Pythonian method for receiving query results from Companions
        :param msg - tell to be passed along in reply
        :param content - the results of the query (asked by ask_agent)
        '''
        logger.debug('received tell: %s', content)  # lazy logging
        self.results = convert_to_list(content)
        reply_msg = KQMLPerformative('tell')
        reply_msg.set('sender', self.name)
        reply_msg.set('content', None)
        self.received = True
        self.reply(msg, reply_msg)

    def query(self, query):
        '''
        Wrapper function for ask_agent and receive_tell for sending and receiving
            queries in companions
        :param query - the query to send to Companions
        :return: a list containing the results of the query
        '''
        self.ask_agent('session-reasoner', query)
        iters = 0
        # check every 0.1 seconds (up to 100 times) until message received
        while not self.received:
            time.sleep(0.1)
            iters += 1
            if iters > 600:
                self.received = True
                self.results = []
                break
        return self.results

    def get_games_with_attribute(self, attribute, value):
        '''
        Queries Companions for a list of games having the given attribute value
        :param attribute - the attribute name to be filtered by
        :param value - the value of the attribute to be filtered by
        :return: a list of games having the specified value for the given attribute
        '''
        results = self.query('(' + attribute + ' ?match ' + value + ')')
        result_list = []
        for item in results:
            matches = re.search('(' + attribute + ' (\S+) ' + value + ')', str(item))
            if matches != None:
                result_list.append(matches.group(1))
        return result_list

    def get_similar_games(self, game, case_library):
        '''
        Queries Companions for a list of games that are similar to the input game
        :param game - the game from which similar games will be returned
        :param case_library - a case library in which to search for similar games
            (we use this to ensure that the returned games are in the same genre as the original game)
        :return: a list of games that are similar to the given game
        '''
        game_mt = game + 'Mt'
        results = self.query('(reminding (KBCaseFn ' + game_mt + ') (CaseLibrarySansFn ' + case_library + ' ' + game_mt
                             + ') (TheSet) ?mostsimilar ?matchinfo)')
        result_list = []
        for item in results:
            matches = re.search('\(TheSet\) *(\S+) *\(.*\)\)', str(item))
            if matches != None:
                result_list.append(matches.group(1)[:-2])
        return result_list
        #return [re.search('\(TheSet\) *(\S+) *\(.*\)\)', str(item)).group(1)[:-2] for item in results]

    def get_game_facts(self, game):
        '''
        Queries Companions for a list of facts corresponding to the given game
        :param game - the game from which to find associated facts
        :return: a list of facts corresponding to the given game
        '''
        results = self.query('(?attribute ' + game + ' ?value)')
        facts_dict = {}
        for result in results:
            match_groups = re.match('\( *(\S+) +\S+ +(\S+) *\)', str(result))
            attribute = match_groups.group(1)
            if attribute != 'isa':
                if attribute in facts_dict.keys():
                    facts_dict[attribute].append(match_groups.group(2))
                else:
                    facts_dict[attribute] = [match_groups.group(2)]
        for key in facts_dict.keys():
            facts_dict[key] = tuple(facts_dict[key])
        return facts_dict

    def get_isa(self, what_it_is):
        '''
        Queries Companions for a list of isa relationships
        :param what_it_is - the first second argument (type) of the isa relationship
        :return: the games matching the given isa type
        '''
        results = self.query('(isa ?match ' + what_it_is + ')')
        return [re.match('\(isa (\S+)', str(item)).group(1) for item in results]

    def insert_game_in_case_library(self, case_library, game):
        '''
        Inserts a game into a given case library (in Companions)
        :param case_library - the case library to insert into
        :param game - the game to insert into the given case lirary
        :return: True
        '''
        game_mt = game+'Mt'
        data = '(caseLibraryContains '+case_library+' '+game_mt+')'
        self.insert_data('session-reasoner', data)
        return True

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

