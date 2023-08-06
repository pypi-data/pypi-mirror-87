
import os
import json
from requests import Response
from datetime import datetime

from .json_parsers import JSONParser


class Parser(JSONParser):
    """
    Is the base class for breaking data returned from a gateway computer from BehrTech into usable components. Provides
    stander functions that apply to all sensor types connected to a gateway.
    """

    def __init__(self, req: Response):
        JSONParser.__init__(self)
        self.response: Response = req
        self.data: str = req.text

    def __repr__(self):
        return f"Parser object for request at {self.response.url} with status code {self.response.status_code}"

    def set_response(self, response: Response):
        """
        Sets the response of the class to the passed in requests Response. Also resets the data of the class from the
        text of the passed in Response.

        :param response: request Response
        """

        self.response = response
        self.data = response.text

    def get_response(self):
        """
        Returns the response of the class

        :return: The response of the class
        """

        return self.response

    def get_data(self):
        """
        Returns the data of the class

        :return: The data of the class
        """
        return self.data

    def write_data_to_file(self, file_name: str, file_path: os.path = 'Outputs/'):
        """
        Outputs the data of the class to a JSON file

        :param file_path: The path to write the file to
        :param file_name: The name of the file for the data of the class to be outputted to
        """

        file_path = file_path if os.path.isdir(file_path) else 'Outputs/'

        text_file = open(file_path + file_name + ".json", "w")
        text_file.write(self.data)
        text_file.close()

    def get_message_count(self) -> int:
        """
        Returns the total count of messages

        :return: The message count total
        """

        return json.loads(self.data).get("count")

    def get_component_data(self, component: str):
        """
        Sources all the data of the class to retrieve the data for a specified component for each message

        :return: The data for a specified component for each message as a list
        """

        component_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys() and component in data.keys():
                        component_data.append(data[component])

        return component_data

    def get_message_data(self) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for each message including a time stamp and
        sensor ID

        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        data["Time"] = x.get("time")
                        data["Command"] = x.get("command")
                        data["Type"] = x.get("type")
                        data["SensorID"] = x.get("epEui")
                        user_data.append(data)

        return user_data

    def get_all_message_types(self) -> list:
        """
        Sources all the data of the class to retrieve all messages for each message type

        :return: All messages for each message type as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:

            check = x.get("userDataJSON")

            if check:
                data = json.loads(check)
                data["Time"] = x.get("time")
                data["Command"] = x.get("command")
                data["Type"] = x.get("type")
                data["SensorID"] = x.get("epEui")
                data["ID"] = x.get('_id')

            else:
                data = {"Time": x.get("time"), "Command": x.get("command"), "Type": x.get("type"),
                        "SensorID": x.get("epEui"), "ID": x.get('_id')}

            user_data.append(data)

        return user_data

    def get_message_datetime_as_str(self) -> list:
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list broken into individual dicts and separated as date and time
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    time_info.append({"date": time_split[0], "time": time_split[1]})

        return time_info

    def get_message_datetime_as_datetime(self) -> list:
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list formatted as a datetime
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"
                    time_info.append(datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S'))

        return time_info

    def get_message_data_in_number_range(self, count: int, offset: int) -> list:
        """
        Sources all the data of the class to retrieve the amount of messages requested at the desired offset

        :param count: The amount of messages to be returned
        :param offset: The message position to start from
        :return: A list of the message data for the messages requested
        """

        amount = 0
        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):
            if index >= offset:
                if amount != count:
                    if x.get("command") == "rxData":

                        check = x.get("userDataJSON")

                        if check:
                            data = json.loads(check)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)
                                amount += 1

                else:
                    break

        return user_data

    def get_message_data_in_date_range(self, start: datetime, end: datetime) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that is within the specified date range

        :param start: Lowest date of date range
        :param end: Highest date of date range
        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"

                    message_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')

                    if start <= message_time <= end:
                        check = x.get("userDataJSON")

                        if check:
                            data = json.loads(check)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)

                    elif message_time < start:
                        break

        return user_data

    def get_date_ranges(self) -> dict:
        """
        Sources all the data of the class to retrieve the date range of the data of the class

        :return: The date range of the data of the class as a dict
        """

        time = self.get_message_datetime_as_str()

        return {"Recent": time[0]["date"], "Oldest": time[-1]["date"]}

    def get_message_ids(self) -> list:
        """
        Sources all the data of the class to retrieve the id for each message

        :return: The id of each message as a list
        """

        ids = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("_id")

                if check:
                    ids.append(check)

        return ids

    def get_message_data_for_id(self, id_number) -> dict:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that matches the requested id number

        :param id_number: The id number of the message that data is being requested for
        :return: The data of the message requested for as a dictionary
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check_id = x.get("_id")

                if check_id:
                    if check_id == id_number:

                        check_data = x.get("userDataJSON")

                        if check_data:
                            data = json.loads(check_data)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                return data

    def get_message_position_for_id(self, id_number) -> int:
        """
        Sources all the data of the class to retrieve the position of the message that matches the requested id number

        :param id_number: The id number of the message that data is being requested for
        :return: The position of the messages that matches the requested id number
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):

            check_id = x.get("_id")

            if check_id:
                if check_id == id_number:
                    return index + 1

    def get_message_epEui(self) -> list:
        """
        Sources all the data of the class to retrieve the epEui for each message

        :return: The epEui of each message as a list
        """

        ids = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("epEui")

                if check:
                    ids.append(check)

        return ids

    def get_message_data_for_epEui(self, eui_number) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that matches the requested epEui number

        :param eui_number: The epEui number of the message that data is being requested for
        :return: The data of the message requested for as a dictionary
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check_eui = x.get("epEui")

                if check_eui:
                    if check_eui == eui_number:

                        check_data = x.get("userDataJSON")

                        if check_data:
                            data = json.loads(check_data)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)

        return user_data

    def get_message_position_for_epEui(self, eui_number) -> int:
        """
        Sources all the data of the class to retrieve the position of the message that matches the requested epEui
        number

        :param eui_number: The epEui number of the message that data is being requested for
        :return: The position of the messages that matches the requested epEui number
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):

            check_eui = x.get("epEui")

            if check_eui:
                if check_eui == eui_number:
                    return index + 1

    # TODO: rewrite functions

    # def get_components(self, ep_eui: str) -> list:
    #     """
    #     Returns a list of measured components for the specified sensor
    #
    #     :param ep_eui:  The unique identifier of a node
    #     :return: List of measured components
    #     """
    #
    #     sens_type = json.loads(self.get_node(ep_eui=ep_eui).text).get('type')
    #     components = json.loads(self.get_node_model(model_type=sens_type).text).get('components')
    #
    #     return [x for x in components]
    #
    # def get_units(self, ep_eui: str) -> dict:
    #     """
    #     Returns a dict of units for measured components for the specified sensor
    #
    #     :param ep_eui: The unique identifier of a node
    #     :return: Dict of units for measured components
    #     """
    #
    #     sens_type = json.loads(self.get_node(ep_eui=ep_eui).text).get('type')
    #     components = json.loads(self.get_node_model(model_type=sens_type).text).get('components')
    #
    #     return {x: components.get(x)['unit'] for x in components}
