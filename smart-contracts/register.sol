// SPDX-License-Identifier: MIT
//pragma solidity ^0.8.17;

pragma solidity ^0.7.0;

//pragma solidity ^0.8.17;

contract Register {
    address[] public workers_addresses;

    function register_worker() public {
        workers_addresses.push(msg.sender);
    }

    function unregister_worker() public {
        // if msg.sender is in workers_addresses, remove it
        for (uint256 i = 0; i < workers_addresses.length; i++) {
            if (workers_addresses[i] == msg.sender) {
                workers_addresses[i] = workers_addresses[
                    workers_addresses.length - 1
                ];
                workers_addresses.pop();
            }
        }
    }

    function get_workers() public view returns (address[] memory) {
        return workers_addresses;
    }
}
