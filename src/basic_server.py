from .script.deploy import deploy_smart_contract


class BasicServer:
    def __init__(self, from_address, from_private_key):
        self.from_address = from_address
        self.from_private_key = from_private_key

    def deploy(self):
        contract_name = "incrementer"
        contract_adress = deploy_smart_contract(
            contract_name, self.from_address, self.from_private_key
        )


def main():
    contract_name = "incrementer"
    from_address = "fce75e885241b4b465ad8e5919416ad4c9290d3e"
    from_private_key = (
        "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
    )
    print(deploy_smart_contract(contract_name, from_address, from_private_key))
