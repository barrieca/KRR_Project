from pythonian import *
import logging
import time
import json
import math
import random
import MalmoPython 


logger = logging.getLogger('MinecraftAgent')

# TODO 6/12:  check obsFlag in check_world_state

class MinecraftAgent(Pythonian):
    name = "MinecraftAgent" # This is the name of the agent to register with

    def __init__(self, missionSpec = None, missionRecordFile = None, clientPool = None, role = None, experimentId = "0", **kwargs): #TODO: setters
        super(MinecraftAgent, self).__init__(**kwargs)
        self.set_agent_host()
        self.initiate_agent(experimentId, missionSpec, missionRecordFile, clientPool, role)
        self.lastWorldState = None
        
        # setters
        self.add_achieve('set_client_pool', self.set_client_pool)
        self.add_achieve('observe_for_time', self.observe_for_time)
        #self.add_achieve('set_block', self.set_block)

        # getters
        self.add_ask('get_agent_host', self.get_agent_host, '(get_agent_host ?host)') 
        self.add_ask('get_mission_spec_summary', self.get_mission_spec_summary, '(get_mission_spec_summary ?spec)')
        self.add_ask('get_mission_spec', self.get_mission_spec, '(get_mission_spec ?spec)')

        # other asks
        self.add_ask('get_current_inventory', self.get_current_inventory, '(get_current_inventory ?world_state_update_flag ?inventory)')
        self.add_ask('get_observations', self.get_observations, '(get_observations ?world_state_update_flag ?observations)')
        self.add_ask('get_last_observation', self.get_last_observation, '(get_last_observation ?world_state_update_flag ?observation')
        self.add_ask('get_world_state', self.get_world_state, '(get_world_state ?world_state_string)')
        self.add_ask('peek_world_state', self.peek_world_state, '(peek_world_state ?world_state_string)')
        self.add_ask('get_inventory_item', self.get_inventory_item, '(get_inventory_item ?item-num  ?world_state_update_flag ?item)')
        self.add_ask('get_grid_observation', self.get_grid_observation, '(get_grid_observation ?grid_name ?world_state_update_flag ?grid)')
        self.add_ask('get_entity_observation', self.get_entity_observation, '(get_entity_observation ?grid_name ?world_state_update_flag ?entities')
        self.add_ask('check_mission_running', self.check_mission_running, '(check_mission_running ?world_state_update_flag ?is_running')
        #self.add_ask('get_ray_observation', self.get_ray_observation, '(get_ray_observation ?')


        # achieve       
        self.add_achieve('send_command', self.send_command) # might want to do separate funcs for various types of commands
        self.add_achieve('sleep', self.sleep)
        self.add_achieve('start_mission', self.start_mission)
        self.add_achieve('initiate_agent', self.initiate_agent)

    #inititate
    def initiate_agent(self, experimentId, missionSpec, missionRecordFile, clientPool, role):
        self.set_mission_spec(missionSpec)
        self.set_mission_record_spec(missionRecordFile)
        self.set_client_pool(clientPool)
        #TODO: setters and getters
        self.role = role
        self.experimentId = experimentId 
        

    # setters
    def set_client_pool(self, clientPool):
        if clientPool:
            client_pool = MalmoPython.ClientPool()
            for i in clientPool:
                client_pool.add(MalmoPython.ClientInfo("127.0.0.1", i))
            self.clientPool = clientPool
        else:
            self.clientPool = None
    

    def set_agent_host(self): 
        self.agentHost = MalmoPython.AgentHost()
        logger.debug('started agent host ' + str(self.agentHost))

    def set_mission_spec(self, missionSpec):
        if missionSpec:
            logger.debug('setting mission spec xml: ' + str(missionSpec))
            self.missionSpec = MalmoPython.MissionSpec(missionSpec, True)
        else:
            logger.debug('setting DEFAULT mission spec')
            self.missionSpec = MalmoPython.MissionSpec()

    def set_mission_record_spec(self, missionRecordFile):
        if missionRecordFile:
            logger.debug('setting mission record with file name: ' + str(missionRecordFile))
            # NOTE: currently records everything
            self.missionRecordSpec = MalmoPython.MissionRecordSpec(missionRecordFile)
            self.missionRecordSpec.recordMP4(20, 400000) #TODO: figure out what actually makes sense here
            self.missionRecordSpec.recordObservations()
            self.missionRecordSpec.recordCommands()
            self.missionRecordSpec.recordRewards() # should be empty for analogy, but might be helpful to have for RL
        else:
            logger.debug('setting EMPTY mission record')
            self.missionRecordSpec = MalmoPython.MissionRecordSpec()



    # getters
    def get_agent_host(self):
        return self.agentHost

        
    def get_mission_spec(self):
        return self.missionSpec

    def get_mission_spec_summary(self):
        return self.missionSpec.getSummary()


    # other functionality
    def start_mission(self):
        logger.debug('attempting to start mission')
        logger.debug('missionSpec is: ' + str(self.missionSpec))
        logger.debug('missionRecord is: ' + str(self.missionRecordSpec)) 
        if self.clientPool:
            logger.debug('starting mission')
            self.agentHost.startMission(self.missionSpec, self.clientPool, self.missionRecordSpec, self.role, self.experimentId)
        else:
            logger.debug('starting mission with missionSpec and missionRecord only')
            self.agentHost.startMission(self.missionSpec, self.missionRecordSpec)

    def send_command(self, command, number):
        commandString = str(command) + " " + str(number)
        logger.debug('command sent: ' + commandString)
        self.agentHost.sendCommand(commandString)

    def sleep(self, sleepLength):
        time.sleep(sleepLength)

    def peek_world_state(self):
        state = self.agentHost.peekWorldState() #peek so that the world state is available for further processing
        logger.debug('peeked state = ' +str(state))
        return str(state)

    def get_world_state(self):
        state = self.agentHost.getWorldState()
        self.lastWorldState = state
        logger.debug('got state: ' + str(state))
        return str(state)

    # TODO: is obsFlag necessary?
    def check_world_state(self, worldStateUpdateFlag=True, obsFlag=False): # obsFlag ensures that a passed in worldState has viable observations
        logger.debug('in check_world_state')
        worldState = None
       # logger.debug('in check_world_state: worldStateUpdateFlag is: ' + str(worldStateUpdateFlag))
        #logger.debug('in check_world_state: converted worldStateUpdateFlag is: ' + str(convert_to_boolean(worldStateUpdateFlag)))
        if not (worldStateUpdateFlag and convert_to_boolean(worldStateUpdateFlag)): 
            worldState = self.lastWorldState
            logger.debug('in check_world_state: worldStateUpdateFlage is False; getting self.lastWorldState')
        
        if not worldState:
            logger.debug('in check_world_state: no worldState found')
            peekedWorldState = self.agentHost.peekWorldState()
            if peekedWorldState.number_of_observations_since_last_state > 0:
                logger.debug('in check_world_state: grabbing new world state')
                worldState = self.agentHost.getWorldState()
            else:
                logger.debug('in check_world_state: no observations in new world state... skipping')
        #elif obsFlag and worldState.number_of_observations_since_last_state < 0:
        #    worldState = None
        self.lastWorldState = worldState
        logger.debug('in check_world_state: self.lastWorldState updated')
        return worldState

    def get_observations(self, worldStateUpdateFlag=True):
        observationList = []
        logger.debug('in get_observations: getting worldState')
        updatedWorldState = self.check_world_state(worldStateUpdateFlag, True)
        logger.debug('in get_observations: returned from updatedWorldState')
        logger.debug('current self.lastWorldState is:' + str(self.lastWorldState))
        if updatedWorldState:
            logger.debug('in get_observations: getting observations')
            observations = updatedWorldState.observations
            observationList = [json.loads(obs.text) for obs in observations]
        else:
            logger.debug('in get_observations: no observations in latest worldState')
        return [observationList]

    def get_last_observation(self, worldStateUpdateFlag=True):
        logger.debug("in get_last_observation: worldStateUpdateFlag is: " + str(convert_to_boolean(worldStateUpdateFlag)))
        updatedWorldState = self.check_world_state(worldStateUpdateFlag, True)
        lastObservation = None
        if updatedWorldState:
            logger.debug('in get_last_observation: getting the observation')
            observations = updatedWorldState.observations
            lastObservation = json.loads(observations[-1].text)
        else:
            logger.debug('in get_last_observation: no observations in latest worldState')

        return lastObservation #TODO: does this need to be wrapped in a list? I don't think so, but maybe...
  

    def get_current_inventory(self, worldStateUpdateFlag=True):
        updatedWorldState = self.check_world_state(worldStateUpdateFlag, True)
        inventory = {}
        if updatedWorldState:
            logger.debug('in get_current_inventory: getting inventory')
            observations = updatedWorldState.observations
            lastObservation = json.loads(observations[-1].text)
            #logger.debug('in get_current_inventory: lastObservation keys = ' + str(lastObservation.keys()))
            for i in range(40):
                #logger.debug('looking for item in slot: ' + str(i))

                key = 'InventorySlot_'+str(i)+'_item'
                var_key = 'InventorySlot_'+str(i)+'_variant'
                col_key = 'InventorySlot_'+str(i)+'_colour'
                size_key = 'InventorySlot_'+str(i)+'_size'
                if key in lastObservation:
                    #logger.debug('in get_current_inventory: getting item: ' + str(key))
                    item = lastObservation[key]
                    obs_dict={}
                    if var_key in lastObservation:
                        obs_dict["variant"] = lastObservation[var_key]
                    if col_key in lastObservation:
                        obs_dict["color"] = lastObservation[col_key]
                    if size_key in lastObservation:
                        obs_dict["size"] = lastObservation[size_key]
                    if str(item) != "air":
                        logger.debug("in get_current_inventory: adding: " + str(item))
                    inventory[item] = obs_dict 
        else:
            logger.debug('in get_current_inventory: no observations in latest worldState')
        logger.debug('inventory is: ' + str(inventory))
        return inventory
        
    def get_inventory_item(self, itemNum=0, worldStateUpdateFlag=True):
       
        updatedWorldState = self.check_world_state(worldStateUpdateFlag,True)
        item = None
        if updatedWorldState:
            logger.debug('in get_inventory_item: getting item number: ' + str(itemNum))
            key = 'InventorySlot_' + str(itemNum) + "_item"
            observations = updatedWorldState.observations
            lastObservation = json.loads(observations[-1].text)
            item = lastObservation[key]
        else:
            logger.debug('in get_inventory_item: no observations in latest worldState for item number ' + str(itemNum))
        return item

    def get_grid_observation(self, gridName, worldStateUpdateFlag=True):
        worldState = self.check_world_state(worldStateUpdateFlag,True)
        grid=[]
        logger.debug('in get_grid_observation: got worldState')
        if worldState:
            logger.debug('in get_grid_observation: getting grid: ' + str(gridName))
            observations = worldState.observations
            lastObservation = json.loads(observations[-1].text)
            
            if str(gridName) in lastObservation:
                logger.debug('in get_grid_observation: getting grid WITH wrapper')
                grid=lastObservation[str(gridName)]
            
            else:
                logger.debug('in get_grid_observation: did not find ' + str(gridName) + " in lastObservation")
            logger.debug('got grid: ' + str(grid))
        else:
            logger.debug('in get_grid_observation: no observations in latest worldState')
        return [grid]

    def get_entity_observation(self, gridName, worldStateUpdateFlag=True):
        worldState = self.check_world_state(worldStateUpdateFlag,True)
        grid=[]
        logger.debug('in get_entity_observation: got worldState')
        if worldState:
            logger.debug('in get_entity_observation: getting entitities: ' + str(gridName))
            observations = worldState.observations
            lastObservation = json.loads(observations[-1].text)
            
            if str(gridName) in lastObservation:
                logger.debug('in get_entity_observation: getting entitities WITH wrapper')
                grid=lastObservation[str(gridName)]
            
            else:
                logger.debug('in get_entity_observation: did not find ' + str(gridName) + " in lastObservation")
            logger.debug('got entitities: ' + str(grid))
        else:
            logger.debug('in get_entity_observation: no observations in latest worldState')
        return [grid]

    def check_mission_running(self, worldStateUpdateFlag=True):
        worldState = self.check_world_state(worldStateUpdateFlag, False) #doesn't matter if the state has new observations, I suppose
        return worldState.is_mission_running

    def observe_for_time(self, obsTime):
        start_time = time.time()
        end_time = time.time()
        worldState = self.check_world_state(True, True)
        logger.debug('in observe_for_time: got worldState')
       
        while end_time - start_time <= 10: #TODO: waiting on convert_to_int implementation for obsTime
            if worldState:
                logger.debug('in observe_for_time: sending to observation')
                observation = self.get_last_observation(False)
                self.send_observation_data(observation)

            time.sleep(1)
            worldState = self.check_world_state(True, True)
            end_time = time.time()
        logger.debug('in observe_for_time: finished observation')
        return None

    def send_observation_data(self, observation):
        logger.debug("in send_observation_data: starting observations")
        observation_time = observation["WorldTime"] # observation is already observation.text
        grid_data = self.get_grid_observation("WholeMap", False)[0]
        entity_data = self.get_entity_observation("EntitiesCompanion", False)[0]
        my_inventory_data = self.get_current_inventory(False)
        #alex_inventory_data = TODO!!!
        #my_line_of_sight_data = TODO!!! <--should be easier todo than the ones for alex
        #alex_line_of_sight_data = TODO!!!

        mt_fact = ["(ist-Information MinecraftObservationsMt (genlMts (ObservationMtFn " + str(self.experimentId) + " " + str(observation_time) + ") MinecraftObservationsMt))"] #TODO: check Mt structure
        
        grid_facts = self.process_grid_data(observation_time, grid_data)
        entity_facts = self.process_entity_data (observation_time, entity_data) # need to adjust coordinates
        my_inventory_facts = self.process_inventory_data(observation_time, "Companion", my_inventory_data)

        all_facts = mt_fact + grid_facts + entity_facts + my_inventory_facts #TODO: add other facts as we get them

        for f in all_facts:
            logger.debug('in send_observation_data: sending fact' + f)
            Pythonian.insert_data(self, 'interaction-manager', f) # TODO: shouldl be sending to WM only (not working--pythonian bug)
        return True
            

    def process_grid_data(self, obsTime, grid_data):
        logger.debug("in process_grid_data: starting processing")
        ist_info_string = "(ist-Information (ObservationMtFn " + str(self.experimentId) + " " + str(obsTime) + ") "
        facts = []
        width = int(math.sqrt(len(grid_data))) # NOTE: assumes square map (may need to consider cube or do layers; perhaps one at ground level and one at eye-level)
        logger.debug("in process_grid_data: got width " + str(width))
        for i in range(width):
            for j in range(width):
                #logger.debug("in process_grid_data: i=" + str(i) + " j=" + str(j))
                grid_object = grid_data[i+j*width]
                #logger.debug("in process_grid_data: got grid_object")
                token = "x" + str(i) + "z" + str(j) 
                collection = self.get_collection(grid_object)
                isa_fact = ist_info_string + "(blockOfType + " + token + " " + collection + "))"
                logger.debug('in process_grid_data: storing isa fact ' + isa_fact)
                adjacenct_tokens = self.get_adjacent(x, y)
                adjacent_facts = ["(nextTo " + token + " " + neighbor for neighbor in adjacenct_tokens]
                logger.debug('in process_grid_data: storing ' + str(len(adjacent_facts)) + " adjacency facts") 
                facts.append(isa_fact)
                facts+=adjacent_facts

        return facts

    def get_adjacent(self, x, y):
        h_neighbors = range(x-1,x+1)
        v_neighbors = range(y-1,y+1)
        tokens=[]
        for h in h_neighbors:
            for v in v_neighbors:
                if h!=x or v!=y:
                    token = "x" + str(h) + "z" + str(v)
                    tokens.append(token)
        return tokens 

    def process_entity_data(self, obsTime, entity_data):
        logger.debug("in process_entity_data: starting processing")
        ist_info_string = "(ist-Information (ObservationMtFn " + str(self.experimentId) + " " + str(obsTime) + ") "
        facts = []
        logger.debug("in process_entity_data: starting for loop")

        for ent in entity_data:
            
            isa = self.get_collection(ent["name"])
            if isa != "Companion":
                if isa == "Alex":
                    token = isa
                else:
                    # TODO: what if the entity has been seen in a prior observation? How to ensure that it has the same token?
                    #       one possibility is naming e.g. (NameFn isa location) and piggybacking off of location
                    #       i.e. if an entity is missing, but a new one of the same type appears elsewhere, it's the same
                    #       need to think this one through, though
                    #       Laura suggests not bothering with individuals... sort of like the way I was going to handle inventory items
                    #       so just e.g. (EntityFn Pig)
                    #       This might mess with one-to-one mapping, though. So maybe doing it with random tokens assigned
                    #       is fine... achieves the same effect without having to worry about one-to-one issues
                    token = isa.lower() + str(random.randint(0, 1000000000000000))
                    isa_fact = ist_info_string + "(entityOfType " + token + " " + isa + "))"
                    logger.debug('in process_entity_data: storing fact ' + isa_fact)
                    facts.append(isa_fact)
                
                i = int(ent["x"])
                j = int(ent["z"])
                
                location_fact = ist_info_string + "(on-Physical " + token +  " x" + str(i) + "z" + str(j) + "))"
                logger.debug('in process_entity_data: storing fact ' + location_fact)
                facts.append(location_fact)
        return facts

    def process_inventory_data(self, obsTime, owner, inventory_data):
        logger.debug("in process_inventory_data: starting processing")
        ist_info_string = "(ist-Information (ObservationMtFn " + str(self.experimentId) + " " + str(obsTime) + ") "
        facts = []
        logger.debug("in process_inventory_data: starting for loop")
        for item in inventory_data:
            collection = self.get_collection(item)
            token = collection.lower() + str(random.randint(0, 1000000000000000))
            size = inventory_data[item]["size"]
            isa_fact = ist_info_string + "((InventoryItemFn  " + collection + ") " + token + str(size) + "))"
                #+ token + " (GroupOfCardinalityFn " + collection + " " + str(size) + ")))"
            logger.debug('in process_inventory_data: storing fact ' + isa_fact)
            facts.append(isa_fact)
            # TODO: color and other attribute facts?
            owns_fact = ist_info_string + "(owns " + owner + " " + token + "))"
            logger.debug('in process_inventory_data: storing fact ' + owns_fact)
            facts.append(owns_fact)
        return facts


    def get_collection (self, name):
        collection = ""
        split = name.split("_")
       
        if name[0].isupper(): # already CamelCased
            collection = name
        elif len(split) < 2:
            collection = split[0].capitalize()
        elif split[1] == "seeds":
            item_type = split[0].capitalize()
            collection = "(SeedFn " + item_type + ")"
        else:
            collection = split[0].capitalize() + split[1].capitalize()
        return collection



if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    mission_file_no_ext = "C:/qrg/irina/minecraft/test/test_mission"
    #mission_file_no_ext = "C:/qrg/irina/minecraft/test/test_mission_multi"

    mission_file = mission_file_no_ext + ".xml"
    with open(mission_file, 'r') as f:
        print("Loading mission from %s" % mission_file)
        mission_xml = f.read()

    my_mission_record = mission_file_no_ext + ".tgz" # details set inside set_mission_record_spec
    
    a = MinecraftAgent(host='localhost', port=9000, localPort=8950, debug=True, missionSpec = mission_xml, missionRecordFile=my_mission_record)
 
   
    #a = MinecraftAgent(host='localhost', port=9000, localPort=8950, debug=True, missionSpec = mission_xml, missionRecordFile=my_mission_record, clientPool= client_pool, role=0)


