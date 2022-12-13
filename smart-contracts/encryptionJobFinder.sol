// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./encryptionJobContainer.sol";

contract EncryptionJobFinder {
    EncryptionJobContainer[] public previousJobs;
    EncryptionJobContainer private jobContainer;

    uint256 thresholdForBestModel = 3; // require 3 equals model to validate
    uint256 thresholdMaxNumberReceivedModels = 6; //stop receiving models when we have 6 models

    constructor() {
        jobContainer = new EncryptionJobContainer(
            5, // model weight (TODO change to bytes4)
            0, // batch index
            thresholdForBestModel,
            thresholdMaxNumberReceivedModels
        );
    }

    function getJob() public view returns (uint256, uint256) {
        /**No condition, everyone can claim the job, and reclaim it */
        return jobContainer.getModelAndBatchIndex();
    }

    function createNewJob() private {
        // push current job to previousJobs
        previousJobs.push(jobContainer);
        // create a new job TODO dummies value atm, should be getted from fl server
        jobContainer = new EncryptionJobContainer(
            5,
            1,
            thresholdForBestModel,
            thresholdMaxNumberReceivedModels
        );
    }

    /// @notice send a new encrypted model to the jobContainer
    /// @param workerAddress the address of the worker sending the model
    /// @param modelHash the hashed model (xored with worker's public key) sent by the worker
    /// @return true if the model was added to the jobContainer, false otherwise
    function addEncryptedModel(uint160 workerAddress, bytes32 modelHash)
        public
        returns (bool)
    {
        // if the model is complete, create a new job and push the current one to previousJobs
        if (jobContainer.getModelIsready()) {
            createNewJob();
        }
        bool modelAdded = jobContainer.addNewEncryptedModel(
            workerAddress,
            modelHash
        );
        return modelAdded;
    }

    function addVerificationParameters(
        uint160 workerAddress,
        uint256 clearModel
    ) public {
        jobContainer.addVerificationParameters(workerAddress, clearModel);
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (uint256[] memory)
    {
        uint256[] memory bestModels = new uint256[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            (uint256 newModel, bool ready) = previousJobs[i].getModel();
            if (ready) {
                bestModels[i] = newModel;
            } else {
                bestModels[i] = 0;
            }
        }
        return bestModels;
    }

    function canSendVerificationParameters(address workerAddress)
        public
        view
        returns (bool)
    {
        return jobContainer.canSendVerificationParameters(workerAddress);
    }

    /// @notice function to get the model
    /// @return the model's weights or empty array along with a boolean indicating if the model is valid
    function getFinalModel() public view returns (uint256, bool) {
        return jobContainer.getModel();
    }

    // ----------- DEBUG FUNCTIONS -------------

    function getModelIsready() public view returns (bool) {
        return jobContainer.getModelIsready();
    }

    function computeKeccak256(bytes1[32] memory clearModel)
        public
        view
        returns (bytes32)
    {
        return jobContainer.computeKeccak256(clearModel);
    }

    function compareKeccak(bytes32 modelHash) public view returns (bool) {
        return jobContainer.compareKeccak(modelHash);
    }
}
