// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract Register {
    uint256 public number;

    constructor() {
        number = 0;
    }

    function register_worker() public {
        number += 1;
    }

    function reset() public {
        number = 0;
    }
}
