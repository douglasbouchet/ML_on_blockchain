import yaml


class Helper:
    @staticmethod
    def read_addresses_and_keys_from_yaml(self, for_worker):
        """Get the public addresses and private keys
        Args:
            for_worker (Boolean): if true fetch addresses and keys for workers, else for the learning server

        Returns: a dict with the addresses and keys if found, otw None
        """
        worker_path = "/home/user/ml_on_blockchain/resources/workers_addresses.yaml"
        server_path = (
            "/home/user/ml_on_blockchain/resources/learning_server_addresse.yaml"
        )
        yaml_path = worker_path if for_worker else server_path
        with open(yaml_path, "r") as stream:
            try:
                addresses_and_keys = yaml.safe_load(stream)
                return addresses_and_keys
            except yaml.YAMLError as exc:
                print(exc)
                return None

        return []


def get_data():
    # TODO
    return []
