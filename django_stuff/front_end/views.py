from django.shortcuts import render
import logging
from pythonian import game_agent
import time

logger = logging.getLogger('GameAgent')
logger.setLevel(logging.DEBUG)
agent = game_agent.GameAgent(host='localhost', port=9000, localPort=8950, debug=True)
#print(agent.ask_agent('session-reasoner', '(emailOfCourseInstructor CS348-Winter2019 ?email)'))

def index(request):
    context = {}
    return render(request, 'index.html', context)

def results(request):
    try:
        subclass = request.POST['subclass']
    except:
        subclass = ''
    agent.ask_agent('session-reasoner', '(isa ?system ' + subclass + ')')
    while not agent.received:
        time.sleep(0.1) # check every 0.1 seconds until message received
    context = {
            'games': agent.facts,
    }
    return render(request, 'results.html', context)


