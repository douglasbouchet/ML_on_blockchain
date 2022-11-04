// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./jobContainer.sol";

contract JobFinder {
    address[] private jobsAddresses;
    JobContainer private jobContainer;

    // some initial values, to be changed by values sent by fl server
    int256[] private currentModel = new int256[](10);
    uint256[] private batchIndex = new uint256[](10);

    constructor() {
        jobContainer = new JobContainer(3, 0, 1);
    }

    function getJob() public view returns (int256, uint256) {
        return jobContainer.getModelAndBatchIndex();
    }

    function getNModelsUntilEnd() public view returns (uint16) {
        return jobContainer.getNModelsUntilEnd();
    }
}
