// SPDX-License-Identifier: MIT
//pragma solidity ^0.8.17;

pragma solidity ^0.7.0;

//pragma solidity ^0.8.17;

contract Register {
    uint256 public number;

    constructor() {
        number = 0;
    }

    function register_worker() public {
        number += 1;
    }

    function unregister_worker() public {
        // add check to see if worker is registered to learning
        if (number > 0) {
            number -= 1;
        }
    }

    function reset() public {
        number = 0;
    }
}
