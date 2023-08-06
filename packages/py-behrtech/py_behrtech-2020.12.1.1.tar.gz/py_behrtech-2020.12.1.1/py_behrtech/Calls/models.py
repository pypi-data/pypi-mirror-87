import requests

from py_behrtech.parsers import Parser
from py_behrtech.exceptions import check_status_code


class Models:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def models_delete(self):
        pass

    def models_get(self, return_count: int = '', offset: int = ''):
        """
        Gets information on all registered node models

        :param return_count: The amount of node models to be requested. (-1 for all)
        :param offset: Node model amount to start the request from
        :return: Parser object of configured node models
        """

        parameters = ''

        if return_count:
            parameters += f"?returnCount={return_count}"
        if offset:
            parameters += (f"&offset={offset}" if parameters else f"?offset={offset}")

        req = requests.get(url=self.server_address + f"/v2/sensormodels" + parameters,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)

    def models_post(self):
        pass

    def models_type_delete(self):
        pass

    def models_type_get(self, model_type: str):
        """
        Gets information on a registered node model

        :param model_type: Unique identifier of the node model to be requested
        :return: Parser object of configured node model
        """

        req = requests.get(url=self.server_address + f"/v2/sensormodels/{model_type}",
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)

    def models_type_post(self):
        pass
