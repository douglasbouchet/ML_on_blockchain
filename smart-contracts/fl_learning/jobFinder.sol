// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./jobContainer.sol";

contract JobFinder {
    /**
    The goal of this contract is to provide job task to workers willing to join learning process.
    The contract will be deployed by the owner of the learning process.
    Only the owner will be able to add tasks.
    */

    address[] private jobsAddresses;
    JobContainer private jobContainer;

    constructor() public {
        jobContainer = new JobContainer(3, new int256[](0));
    }

    function getJob() public view returns (address[] memory) {
        return address(jobContainer);
    }
}
