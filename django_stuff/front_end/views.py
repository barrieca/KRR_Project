from django.shortcuts import render
import logging
from pythonian import game_agent
import time
import data_manager
from similarity_measure import similarity_measure

logger = logging.getLogger('GameAgent')
logger.setLevel(logging.DEBUG)
agent = game_agent.GameAgent(host='localhost', port=9000, localPort=8950, debug=True)
game_dict = data_manager.get_games()
game_score_vectors = None
case_lib_appendix = 0
#print(agent.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)'))

def index(request):
    '''
    view for index.html
    :param request - the page request object
    :return: rendered page
    '''
    global game_score_vectors
    total_game_score_vector = {}
    feedback_dict = {'good': 1, 'bad': -1, 'neutral': 0}
    similarity_dict = {}
    '''
    Create pseudo similarity_vector
    '''
    with open('./similarity_vector.txt') as f:
        for line in f:
            (key, val) = line.split()
            similarity_dict[key] = float(val)
    '''
    Get feedback from user
    '''
    try:
        feedback = [request.POST['radio1'], request.POST['radio2'], request.POST['radio3']]
        feedback = [feedback_dict[f] for f in feedback]
    except:
        feedback = []
    vec = 0
    if feedback:
        '''
        Change sign on values in game_score_vectors depending on whether feedback was negative or positive (or neutral)
        '''
        for i in range(len(feedback)):
            if vec == 0:
                for k, v in game_score_vectors[i][1].items():
                    total_game_score_vector[k] = v * feedback[i]
                    vec += 1
            else:
                for k, v in game_score_vectors[i][1].items():
                    total_game_score_vector[k] += v * feedback[i]
    if feedback:
        '''
        Alter similarity vector and normalize, then write to file for storage
        '''
        for k, v in similarity_dict.items():
            similarity_dict[k] = (v+0.01*total_game_score_vector[k])
        factor = 1.0/sum(similarity_dict.values())
        for k, v in similarity_dict.items():
            similarity_dict[k] = v*factor
        with open('./similarity_vector.txt', 'w') as f:
            for k, v in similarity_dict.items():
                f.write(k+' '+str(v)+'\n')
    context = {
        'games': game_dict.keys(),
        'feedback': feedback,
    }
    return render(request, 'index.html', context)

def results(request):
    '''
    view for results.html
    :param request - the page request object
    :return: rendered page
    '''
#try:
    original_games = [request.POST['game1'], request.POST['game2'], request.POST['game3']]

    attributes = []
    attributes = [tuple(request.POST.getlist('attribute1')[0].split(',')),
                  tuple(request.POST.getlist('attribute2')[0].split(',')),
                  tuple(request.POST.getlist('attribute3')[0].split(','))]

    original_game_facts = []
    for game_num in range(3):
        game = original_games[game_num]
        game_attributes = tuple([attr for game_attribute in attributes[game_num] for attr in game_attribute.split()])
        original_game_fact_set = agent.get_game_facts(game_dict[game])
        original_game_fact_set['gameName'] = tuple([game])
        original_game_facts.append((original_game_fact_set, game_attributes))

    global case_lib_appendix

    case_libraries = []
    case_library_base = 'VideoGameCaseLibrary_'+str(case_lib_appendix)
    case_lib_appendix += 1
    extra_appendix = 1
    mt_name = 'VideoGamesMt'
    for game in original_game_facts:
        case_library = case_library_base + '_' +str(extra_appendix)
        data = '(isa '+case_library+' CaseLibrary)'
        new_data = f'(ist-Information {mt_name} {data})'
        agent.insert_data('session-reasoner', new_data)
        case_libraries.append(case_library)
        extra_appendix += 1
        game_genres = game[0]['videoGameGenre']
        for genre in game_genres:
            games_for_case_library = agent.get_games_with_attribute('videoGameGenre', genre)
            games_for_case_library = [triple.split()[1] for triple in games_for_case_library]
            for g in games_for_case_library:
                agent.insert_game_in_case_library(case_library, g)

    game_sets = [agent.get_similar_games(game_dict[original_games[0]], case_libraries[0]),
                 agent.get_similar_games(game_dict[original_games[1]], case_libraries[1]),
                 agent.get_similar_games(game_dict[original_games[2]], case_libraries[2])]

    game_sets = [game_set for game_set in game_sets if len(game_set) > 0]

    game_fact_set = []
    for games in game_sets:
        game_facts = []
        for game in games:
            game_facts.append(agent.get_game_facts(game))
            game_facts[-1]['gameName'] = tuple([game])
        game_fact_set.append(game_facts)

    similarity_dict = {}
    '''
    Create game score vectors
    '''
    with open('./similarity_vector.txt') as f:
        for line in f:
            (key, val) = line.split()
            similarity_dict[key] = float(val)

    game_vectors = similarity_measure.find_similar_games(similarity_dict,
                                                         original_game_facts, game_fact_set)

#except:
    game_facts = [game_dict_tuple[0][0] for game_dict_tuple in game_vectors]
    global game_score_vectors
    game_score_vectors = [(game_dict_tuple[0][0], game_dict_tuple[1]) for game_dict_tuple in game_vectors]

    context = {
        'results': game_facts,
    }
    return render(request, 'results.html', context)


