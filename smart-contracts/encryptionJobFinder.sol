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
    /// @return true if the model was added to the jobContainer, false otherwise
    // function addEncryptedModel(address workerAddress, bytes4 encryptedModel)
    function addEncryptedModel(
        address workerAddress,
        bytes1[32] memory model_keccak,
        bytes1[32] memory model_secret_keccak
    ) public returns (bool) {
        bool modelAdded = jobContainer.addNewEncryptedModel(
            workerAddress,
            model_keccak
        );
        return modelAdded;

        // // if the model is complete, create a new job and push the current one to previousJobs
        // if (jobContainer.getModelIsready()) {
        //     createNewJob();
        // }
    }

    // function addVerificationParameters(
    //     address workerAddress,
    //     int256 workerNonce,
    //     bytes1[44] memory workerSecret
    // ) public {
    //     jobContainer.addVerificationParameters(
    //         workerAddress,
    //         workerNonce,
    //         workerSecret
    //     );
    // }
    function addVerificationParameters(
        address workerAddress,
        bytes1[32] memory workerSecret,
        bytes1[32] memory clearModel
    ) public {
        jobContainer.addVerificationParameters(
            workerAddress,
            workerSecret,
            clearModel
        );
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (bytes32[] memory)
    {
        bytes32[] memory bestModels = new bytes32[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            (bytes32 newModel, bool ready) = previousJobs[i].getModel();
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

    /// @notice function to get the model
    /// @return the model's weights or empty array along with a boolean indicating if the model is valid
    function getFinalModel() public view returns (bytes32, bool) {
        return jobContainer.getModel();
    }

    // ----------- DEBUG FUNCTIONS -------------

    function getModelIsready() public view returns (bool) {
        return jobContainer.getModelIsready();
    }
}
