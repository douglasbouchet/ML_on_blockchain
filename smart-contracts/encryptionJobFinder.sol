// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./encryptionJobContainer.sol";

contract EncryptionJobFinder {
    EncyptionJobContainer[] public previousJobs;
    EncyptionJobContainer private jobContainer;

    constructor() {
        uint256 thresholdForBestModel = 2;
        uint256 thresholdMaxNumberReceivedModels = 3; //stop receiving models when we have 5 models
        jobContainer = new EncyptionJobContainer(
            5, // model weight (TODO change to bytes4)
            0, // batch index
            thresholdForBestModel,
            thresholdMaxNumberReceivedModels
        );
    }

    function getJob() public view returns (int256, uint256) {
        /**No condition, everyone can claim the job, and reclaim it */
        return jobContainer.getModelAndBatchIndex();
    }

    function createNewJob() private {
        // push current job to previousJobs
        previousJobs.push(jobContainer);
        // create a new job TODO dummies value atm, should be getted from fl server
        uint256 thresholdForBestModel = 2;
        uint256 thresholdMaxNumberReceivedModels = 5;
        jobContainer = new EncyptionJobContainer(
            5,
            1,
            thresholdForBestModel,
            thresholdMaxNumberReceivedModels
        );
    }

    /// @notice send a new encrypted model to the jobContainer
    /// @param workerAddress the address of the worker sending the model
    /// @param encryptedModel the encrypted model sent by the worker
    /// @return true if the model was added to the jobContainer, false otherwise
    function addEncryptedModel(address workerAddress, bytes4 encryptedModel)
        public
        returns (bool)
    {
        bool modelAdded = jobContainer.addNewEncryptedModel(
            workerAddress,
            encryptedModel
        );
        return modelAdded;

        // // if the model is complete, create a new job and push the current one to previousJobs
        // if (jobContainer.getModelIsready()) {
        //     createNewJob();
        // }
    }

    function addVerificationParameters(
        address workerAddress,
        int256 workerNonce,
        bytes4 workerSecret
    ) public {
        jobContainer.addVerificationParameters(
            workerAddress,
            workerNonce,
            workerSecret
        );
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (bytes4[] memory)
    {
        bytes4[] memory bestModels = new bytes4[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            (bytes4 newModel, bool ready) = previousJobs[i].getModel();
            if (ready) {
                bestModels[i] = newModel;
            } else {
                bestModels[i] = 0;
            }
        }
        return bestModels;
    }

    function canSendVerificationParameters() public view returns (bool) {
        return jobContainer.canSendVerificationParameters();
    }

    // ----------- DEBUG FUNCTIONS -------------
}
