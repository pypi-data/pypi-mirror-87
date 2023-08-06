
import json
from datetime import datetime
from typing import Union


class JSONParser:

    def __init__(self):
        self.data = None

    def get_rxData_messages(self) -> str:
        """
        Sources all data of the class and returns only rxData messages as a json string

        :return: All sensor data for each message as a json string
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        remove = [x for x in messages if x.get("command") != "rxData"]

        for rem in remove:
            messages.remove(rem)

        data['count'] = data['count'] - len(remove)
        data['total'] = data['total'] - len(remove)
        data['messages'] = messages

        return json.dumps(data, indent=4, sort_keys=True)

    def get_attPrpAcc_messages(self) -> str:
        """
        Sources all data of the class and returns only attPrpAcc messages as a json string

        :return: All attPrpAcc messages as a json string
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        remove = [x for x in messages if x.get("command") != "attPrpAcc"]

        for rem in remove:
            messages.remove(rem)

        data['count'] = data['count'] - len(remove)
        data['total'] = data['total'] - len(remove)
        data['messages'] = messages

        return json.dumps(data, indent=4, sort_keys=True)

    def get_detPrpAcc_messages(self) -> str:
        """
        Sources all data of the class and returns only detPrpAcc messages as a json string

        :return: All detPrpAcc messages as a json string
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        remove = [x for x in messages if x.get("command") != "detPrpAcc"]

        for rem in remove:
            messages.remove(rem)

        data['count'] = data['count'] - len(remove)
        data['total'] = data['total'] - len(remove)
        data['messages'] = messages

        return json.dumps(data, indent=4, sort_keys=True)

    def get_message_for_id(self, id_number) -> str:
        """
        Sources all the data of the class to retrieve a message for the provided id

        :param id_number: The id number of the message that is being requested
        :return: The message as a json string
        """

        data = json.loads(self.data)

        for x in data.get("messages"):
            if x.get("_id") == id_number:

                data['count'] = 1
                data['total'] = 1
                data['messages'] = x

                return json.dumps(data, indent=4, sort_keys=True)

    def get_messages_in_date_range(self, start: datetime, end: datetime) -> str:
        """
        Sources all the data of the class to retrieve all messages that are within the specified date range

        :param start: Lowest date of date range
        :param end: Highest date of date range
        :return: Messages within the specified date range as a list
        """

        user_data = []
        data = json.loads(self.data)

        for x in data.get("messages"):
            if x.get("time"):
                time_split = x.get("time").strip("Z").split("T")
                message_time = datetime.strptime(f"{time_split[0]} {time_split[1]}", '%Y-%m-%d %H:%M:%S')

                if start <= message_time <= end:
                    user_data.append(x)

                elif message_time < start:
                    data['count'] = data['total'] = len(user_data)
                    data['messages'] = user_data

                    return json.dumps(data, indent=4, sort_keys=True)

    def get_messages_to_id(self, id_num: str) -> Union[str, bool]:
        """
        Sources all the data of the class to retrieve all messages up to the message with the provided ID

        :param id_num: The ID number of the message to requested messages to
        :return: Messages from the start to the message with the provided id or False if id isn't found
        """

        user_data = []
        data = json.loads(self.data)

        for x in data.get("messages"):

            if x.get('_id') == id_num:
                data['count'] = data['total'] = len(user_data)
                data['messages'] = user_data

                return json.dumps(data, indent=4, sort_keys=True)

            user_data.append(x)

        return False
