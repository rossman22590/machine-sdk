from .api import agents, threads
from .agent import MachineAgent
from .thread import MachineThread
from .tools import AgentPressTools, MCPTools


class Machine:
    def __init__(self, api_key: str, api_url="https://the-machine-api-v9-2-production.up.railway.app/api"):
        self._agents_client = agents.create_agents_client(api_url, api_key)
        self._threads_client = threads.create_threads_client(api_url, api_key)

        self.Agent = MachineAgent(self._agents_client)
        self.Thread = MachineThread(self._threads_client)
