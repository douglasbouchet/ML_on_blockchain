// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./jobContainer.sol";

contract JobFinder {
    JobContainer[] public previousJobs;
    JobContainer private jobContainer;

    // some initial values, to be changed by values sent by fl server
    int256[] private currentModel = new int256[](10);
    uint256[] private batchIndex = new uint256[](10);

    constructor() {
        jobContainer = new JobContainer(3, 0, 1);
    }

    function getJob() public view returns (int256, uint256) {
        /**No condition, everyone can claim the job, and reclaim it */
        return jobContainer.getModelAndBatchIndex();
    }

    function createNewJob() private {
        //jobsAddresses.push(address(jobContainer));
        // push current job to previousJobs
        previousJobs.push(jobContainer);
        // create a new job TODO dummies value atm, should be getted from fl server
        jobContainer = new JobContainer(3, 1, 2);
    }

    //function submitNewModel(int256 _model, address _workerAddress) public {
    function submitNewModel(int256 _model) public {
        bool jobFinished = jobContainer.submitNewModel(_model, msg.sender);

        if (jobFinished) {
            // publish the best model
            // TODO
            // create a new job
            createNewJob();
        }
    }

    function getNModelsUntilEnd() public view returns (uint16) {
        return jobContainer.getNModelsUntilEnd();
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (int256[] memory)
    {
        int256[] memory bestModels = new int256[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            bestModels[i] = previousJobs[i].getBestModel();
        }
        return bestModels;
    }

    // ----------- DEBUG FUNCTIONS -------------
    function getReceivedModels() public view returns (int256[] memory) {
        return jobContainer.getReceivedModels();
    }
}
