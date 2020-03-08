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
#print(agent.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)'))

def index(request):
    try:
        feedback = [request.POST['radio1'], request.POST['radio2'], request.POST['radio3']]
    except:
        feedback = []
    context = {
        'games': game_dict.keys(),
        'feedback': feedback,
    }
    return render(request, 'index.html', context)

def results(request):
#try:
    original_games = [request.POST['game1'],request.POST['game2'],request.POST['game3']]

    attributes = []
    attributes = [request.POST.getlist('attribute1'),request.POST.getlist('attribute2'),request.POST.getlist('attribute3')]

    original_game_facts = []
    for game_num in range(3):
        game = original_games[game_num]
        game_attributes = tuple([attr for game_attribute in attributes[game_num] for attr in game_attribute.split()])
        original_game_fact_set = agent.get_game_facts(game_dict[game])
        original_game_fact_set['gameName'] = tuple([game])
        original_game_facts.append((original_game_fact_set,game_attributes))

    game_sets = [agent.get_similar_games(game_dict[original_games[0]]), agent.get_similar_games(game_dict[original_games[1]]), agent.get_similar_games(game_dict[original_games[2]])]
    game_sets = [game_set for game_set in game_sets if len(game_set) > 0]
    game_fact_set = []
    for games in game_sets:
        game_facts = []
        for game in games:
            game_facts.append(agent.get_game_facts(game))
            game_facts[-1]['gameName'] = tuple([game])
        game_fact_set.append(game_facts)

    game_vectors = similarity_measure.find_similar_games({ 'artist': 1, 'designer': 1, 'director': 1, 'developmentStudio': 1, 'writer': 1, 'score': 1, 'releaseYear': 1, 'videoGameGenre': 1 },original_game_facts, game_fact_set)

#except:
    game_facts = []

    context = {
        'results': original_games,
    }
    return render(request, 'results.html', context)


