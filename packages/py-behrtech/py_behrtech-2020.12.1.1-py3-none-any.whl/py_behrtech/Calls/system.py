import requests

from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError, ConnectTimeoutError
from py_behrtech.parsers import Parser
from py_behrtech.exceptions import JWTError, check_status_code


class System:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def authTicketGet(self) -> str:
        """
        Get ticket information from which you can request an upgrade to a websocket connection at /ws

        :return: Parser object of ticket information
        """

        req = requests.get(url=self.server_address + f"/v2/auth/ticket",
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json().get("ticket")
        else:
            check_status_code(req=req)

    def login(self) -> str:
        """
        Gets the JWT token of the login endpoint

        :return: The JWT token of the login endpoint
        """
        try:
            req = requests.post(
                self.server_address + "/v2/login",
                json={'user': self.username, 'password': self.password},
                timeout=3
            )

            if req.status_code == 200:
                # Successfully logged in
                return req.json().get("JWT")
            else:
                check_status_code(req=req)

        except (TimeoutError, ConnectTimeoutError, MaxRetryError, RequestException):
            raise JWTError(message="The wrong server IP address or login credentials were provided")

    def systemGet(self) -> Parser:
        """
        Gets system status information

        :return: Parser object of system status information
        """

        req = requests.get(url=self.server_address + f"/v2/system",
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)

    def wsGet(self, access_token: str = None) -> Parser:
        """
        Request an upgrade to a websocket connection (Handshake is handled by goland http upgrader)

        :param access_token: Unique token to authenticate to for requesting an upgrade to a websocket connection
        :return: Parser object of a websocket connection upgrade
        """
        if not access_token:
            access_token = self.authTicketGet()

        req = requests.get(url=self.server_address + f"/v2/ws?accessToken={access_token}",
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)
