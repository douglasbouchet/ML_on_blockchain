// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./fragmentedJobContainer.sol";

contract FragmentedJobFinder {
    FragmentedJobContainer[] public previousJobs;
    FragmentedJobContainer private jobContainer;

    // some initial values, to be changed by values sent by fl server
    int256[] private currentModel = new int256[](10);
    uint256[] private batchIndex = new uint256[](10);

    constructor() {
        jobContainer = new FragmentedJobContainer(5, 0, 1);
    }

    function getJob() public view returns (int256, uint256) {
        /**No condition, everyone can claim the job, and reclaim it */
        return jobContainer.getModelAndBatchIndex();
    }

    function createNewJob() private {
        // push current job to previousJobs
        previousJobs.push(jobContainer);
        // create a new job TODO dummies value atm, should be getted from fl server
        jobContainer = new FragmentedJobContainer(5, 1, 2);
    }

    /// @notice submit a new model to the jobContainer
    /// @param _fragNb of the model submitted
    /// @param _weight of the fragment submitted
    /// @param _modelHash of the complete model
    /// @return true is the fragment was accepted, false otherwise so worker needs to resubmit another fragment
    function addFragment(
        uint256 _fragNb,
        int256 _weight,
        bytes32 _modelHash
    ) public returns (bool) {
        // bool fragmentAccepted = jobContainer.addFragment(
        //     msg.sender,
        //     _fragNb,
        //     _weight,
        //     _modelHash
        // );

        // // if the model is complete, create a new job and push the current one to previousJobs
        // if (jobContainer.getModelIsready()) {
        //     createNewJob();
        // }
        // return fragmentAccepted;
        return false;
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (int256[] memory)
    {
        int256[] memory bestModels = new int256[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            (int256 value, bool ready) = previousJobs[i].getModel();
            if (ready) {
                bestModels[i] = value;
            } else {
                bestModels[i] = 0;
            }
        }
        return bestModels;
    }

    // ----------- DEBUG FUNCTIONS -------------
}
