from django.shortcuts import render
import logging
from pythonian import game_agent
import time
import data_manager

logger = logging.getLogger('GameAgent')
logger.setLevel(logging.DEBUG)
agent = game_agent.GameAgent(host='localhost', port=9000, localPort=8950, debug=True)
#print(agent.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)'))

def index(request):
    context = {
        'games': data_manager.get_games()
    }
    return render(request, 'index.html', context)

def results(request):
    try:
        games_facts = [] # agent.get_game_facts([request.POST['game1'], request.POST['game2'], request.POST['game3']])
    except:
        games_facts = ''

    context = {
        'results': agent.get_isa('NUPhDStudent'),
    }
    return render(request, 'results.html', context)


