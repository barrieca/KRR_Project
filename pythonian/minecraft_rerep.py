
from qsr_lib_communicator import QSRLibCommunicator


class MinecraftRerepAgent(QSRLibCommunicator):
    def __init__(self, **kwargs):
        self.name = "MinecraftRerepAgent"  # TODO: possibly need to put this after the super constructor
        super(MinecraftRerepAgent, self).__init__(**kwargs)

        self.add_asks()
        self.add_achieves()
        self.add_to_knowledge_converters()
        self.add_from_knowledge_converters()

    def add_to_knowledge_converters(self):
        self.add_to_knowledge_converter("events", self.get_event_facts)
        super(MinecraftRerepAgentRerepAgent, self).add_to_knowledge_converters()

