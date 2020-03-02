### this is the file where helper functions go.  There are two import principles to using this:
### every function has to take the pythonian agent that is calling it as its FIRST argument
### do all necessary imports within the helper functions
### assign new variables to the agent as needed, even if they are sessions; this will implicitly start new threads

def labelImage (agent, path):
    from im2txt import run_inference as ri  
    import tensorflow as tf
    if not hasattr(agent, 'imgModel'): [agent.imgModel,
                                     agent.imgVocab, 
                                     agent.imgGraph, agent.imgR, 
                                     agent.imgGenerator] = ri.preplabelImg("C:/qrg/companions/v1/pythonian/labelimg/model.ckpt-2000000","C:/qrg/companions/v1/pythonian/labelimg/word_counts.txt")
    if not hasattr(agent, 'tfSess'): 
        agent.tfSess = tf.Session(graph=agent.imgGraph)
        agent.imgR(agent.tfSess)
    
    #model,vocab,g,r = ri.preplabelImg("C:/qrg/companions/v1/pythonian/labelimg/model.ckpt-1000000","C:/qrg/companions/v1/pythonian/labelimg/word_counts.txt")
    #cap = ri.labelImg("C:/qrg/companions/v1/pythonian/labelimg/model.ckpt-1000000","C:/qrg/companions/v1/pythonian/labelimg/word_counts.txt", path)
    
    cap = ri.labelImgg(agent.imgModel,agent.imgVocab, 
                       agent.imgGraph, agent.imgR, 
                       agent.imgGenerator, agent.tfSess, 
                       eval(path))
    print("cap: ")
    print(cap)
    return [[x] for x in cap]

#def uppercase(agent, string):
#    # if you needed an import it would go here
#    return [[string.upper()]]

def endTfSession(agent):
    if hasattr(agent, 'tfSess'): 
        self.tfSess.close()
        delattr(agent, 'tfSess')

def importHelper(agent, package):
    ### If you are not sure whether the module is installed, you can use importHelper
    ### The syntax for import helper within a function is package = importHelper("package")
    ### So if you weren't sure whether you had numpy installed, inside your function where
    ### you were trying to install it you would call
    ### numpy = importHelper("numpy")
    ### it returns the variable, so whatever calls this needs to be ready to assign it
    import pip
    import subprocess as sp
    try: exec('import ' + package)
    except ImportError:
        print("no local package named " + package)
        print("trying to install it in a separate process")
        ### This next thing should be thread safe but maybe just don't install packages from code?
        try: sp.Popen([pip.main(['install', '--user', package]), shell == True])
        except NameError: print(package + " is not a package known to pip. Try again.")    
    return eval(package)

def uptime(agent):
    from datetime import datetime
    import numpy
    now = datetime.now()
    years = now.year-agent.starttime.year
    #months
    if now.year==agent.starttime.year: months = now.month - agent.starttime.month
    else: months = 12 - agent.starttime.month + now.month
    #days
    if now.month == agent.starttime.month: days = now.day - agent.starttime.day
    elif agent.starttime.month in [1, 3, 5, 7, 8, 10, 12]:
        days = 31 - agent.starttime.day + now.day
    elif agent.starttime.month in [4, 6, 9, 11]:
        days = 30 - agent.starttime.day + now.day
    else: days = 28 - agent.starttime.day + now.day
    #hours
    if agent.starttime.day == now.day: hours = now.hour - agent.starttime.hour
    else: hours = 24 - agent.starttime.hour + now.hour
    #minutes
    if agent.starttime.hour == now.hour: minutes = now.minute - agent.starttime.minute
    else: minutes = 60 - agent.starttime.minute + now.minute
    #seconds
    if agent.starttime.minute == now.minute: seconds = now.second - agent.starttime.second
    else: seconds = 60 - agent.starttime.second + now.second
    return str('('+ " ".join([str(i) for i in [years, months, days, hours, minutes, seconds]]) + ')')


