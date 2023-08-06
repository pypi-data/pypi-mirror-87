import requests

from py_behrtech.parsers import Parser
from py_behrtech.exceptions import check_status_code


class Nodes:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def nodesEpEuiGet(self, ep_eui: str):
        """
        Gets information on a configured node with the matching EpEui

        :param ep_eui: The unique epEui number of the node to be requested
        :return: Parser object of the configured node
        """
        req = requests.get(url=self.server_address + f"/v2/nodes/{ep_eui}",
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)

    def nodesGet(self, return_count: int = '', offset: int = '', sensor_type: str = ''):
        """
        Gets information on all configured nodes

        :param return_count: The amount of nodes to be requested. (-1 for all)
        :param offset: Node amount to start the request from
        :param sensor_type: Node type to be requested
        :return: Parser object of configured nodes
        """
        parameters = ''

        if return_count:
            parameters += f"?returnCount={return_count}"
        if offset:
            parameters += (f"&offset={offset}" if parameters else f"?offset={offset}")
        if sensor_type:
            parameters += (f"&sensorType={sensor_type}" if parameters else f"?sensorType={sensor_type}")

        req = requests.get(url=self.server_address + f"/v2/nodes" + parameters,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)
