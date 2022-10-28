class Helper:
    @staticmethod
    def read_addresses_and_keys_from_yaml(self, for_worker):
        """Get the public addresses and private keys
        Args:
            for_worker (Boolean): if true fetch addresses and keys for workers, else for the learning server

        Returns: a dict with the addresses and keys if found, otw None
        """
        # read from the file ../ressources/addresses_and_keys.yaml
        with open("../ressources/addresses_and_keys.yaml", "r") as stream:
            try:
                addresses_and_keys = yaml.safe_load(stream)
                return addresses_and_keys
            except yaml.YAMLError as exc:
                print(exc)
                return None

        return []
