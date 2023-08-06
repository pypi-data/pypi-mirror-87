
import requests
from .parsers import Parser
from .exceptions import JWTError, PermissionsError, QueryError
from .Calls import Azure, BaseStation, Messages, Models, Mqtt, Nodes, Plugins, System


class Calls(Azure, BaseStation, Messages, Models, Mqtt, Nodes, Plugins, System):
    """
    Is a class for connecting to and accessing messages on BehrTech's industrial gateways
    """

    def __init__(self, username: str, password: str, server_address: str):
        Azure.__init__(self)
        BaseStation.__init__(self)
        Messages.__init__(self)
        Models.__init__(self)
        Mqtt.__init__(self)
        Nodes.__init__(self)
        Plugins.__init__(self)
        System.__init__(self)
        self.username = username
        self.password = password
        self.server_address = server_address
        self.jwt_token = self.login()

    def __repr__(self):
        return f"Connection to {self.server_address} for user {self.username}"

    def set_username(self, username: str):
        """
        Sets the login username for the given gateway

        :param username: username credential
        """

        self.username = username

    def get_username(self) -> str:
        """
        Returns the username credential for the given gateway

        :return: The username credential for the given gateway
        """

        return self.username

    def set_password(self, password: str):
        """
        Sets the login password for the given gateway

        :param password: password credential
        """

        self.password = password

    def get_password(self) -> str:
        """
        Returns the password credential for the given gateway

        :return: The password credential for the given gateway
        """

        return self.password

    def set_server_address(self, server_address):
        """
        Sets the IP address for the given gateway

        :param server_address: The IP address of the given gateway
        """

        self.server_address = server_address

    def get_server_address(self) -> str:
        """
        Returns the set IP address of the gateway

        :return: The set IP address of the gateway
        """

        return self.server_address

    def test_connection(self) -> bool:
        if self.jwt_token:
            return True
        else:
            return False

    def get_MQTT_mappings(self, return_count: int, offset: int) -> Parser:
        """
        Returns data on all setup MQTT Topics from the gateway.

        :param return_count: Is the amount of MQTT Topics to be requested
        :param offset: Is the MQTT Topic count to start the MQTT Topic data request from
        :return: the requested MQTT Topic data from the gateway
        """

        message = self.server_address + f"/v2/mqttmapping?returnCount={return_count}&offset={offset}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_all_MQTT_brokers(self, return_count: int, offset: int) -> Parser:
        """
        Returns data on all setup MQTT Brokers from the gateway.

        :param return_count: Is the amount of MQTT Brokers to be requested
        :param offset: Is the MQTT Broker count to start the MQTT Broker data request from
        :return: the requested MQTT Broker data from the gateway
        """

        message = self.server_address + f"/v2/broker?returnCount={return_count}&offset={offset}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_MQTT_broker(self, broker_id: str) -> Parser:
        """
        Returns data on a requested MQTT Broker from the gateway.

        :param broker_id: Is the unique identifier of the MQTT Broker to be requested
        :return: the requested MQTT Broker data from the gateway
        """

        message = self.server_address + f"/v2/broker/{broker_id}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_azure_mapping(self) -> Parser:
        """
        Returns data for setup Azure connections on the gateway.

        :return: the requested Azure connection data
        """

        message = self.server_address + "/v2/azuremapping"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))
