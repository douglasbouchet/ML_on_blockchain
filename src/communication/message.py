class Message:
    def __init__(self, worker_address, model_weight):
        """Create a message to send to the workers or learning server

        Args:
            worker_address (str): worker public address (either worker that send or should receive the message)
            model_weight (int[]): learning model weights TODO TBD
        """
        self.worker_address = worker_address
        self.model_weight = model_weight

    def get_worker_address(self):
        """Get the worker address

        Returns: worker address
        """
        return self.worker_address

    def get_model_weight(self):
        """Get the model weight

        Returns: model weight
        """
        return self.model_weight
