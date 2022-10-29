from src.modules.hypervisor import Hypervisor
from src.modules.learning_server import LearningServer


class Network:
    def __init__(self, hypervisor, learning_server):
        self.msg_box = {
            hypervisor.ip_address: [],
            learning_server.ip_address: [],
        }

    def send_message(self, msg, to_ip_address):
        """Send a message to a specific ip address by adding it to the message box of the destination ip address

        Args:
            msg (Message): message to send
            to_ip_address (_type_): ip address of the destination (either hypervisor or learning server ip addresses)

        Returns: True if the message has been sent, False otherwise
        """
        # check that msg_box contains the key to_ip_address
        if to_ip_address in self.msg_box:
            self.msg_box[to_ip_address].append(msg)
            return True
        else:
            print("No such ip address")
            return False

    def read_messages(self, from_ip_address):
        """Read the messages from a specific ip address. The messages are removed from the message box

        Args:
            from_ip_address (str): ip address of the source (either hypervisor or learning server ip addresses)

        Returns: list of messages
        """
        # check that msg_box contains the key from_ip_address
        if from_ip_address in self.msg_box:
            messages = self.msg_box[from_ip_address]
            self.msg_box[from_ip_address] = []
            return messages
        else:
            print("No such ip address")
            return None
