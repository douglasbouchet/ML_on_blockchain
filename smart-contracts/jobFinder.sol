// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./jobContainer.sol";

contract JobFinder {
    address[] private jobsAddresses;
    JobContainer private jobContainer;

    constructor() {
        jobContainer = new JobContainer(3, new int256[](0));
    }

    function getJobContainer() public view returns (address) {
        return address(jobContainer);
    }

    function getNModelsUntilEnd() public view returns (uint16) {
        return jobContainer.getNModelsUntilEnd();
    }
}
