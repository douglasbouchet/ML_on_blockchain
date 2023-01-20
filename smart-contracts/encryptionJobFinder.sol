// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

import "./encryptionJobContainer.sol";

contract EncryptionJobFinder {
    EncryptionJobContainer[] public previousJobs;
    EncryptionJobContainer private jobContainer;

    constructor() {
        jobContainer = new EncryptionJobContainer();
    }

    function getJob() public view returns (uint256, uint256) {
        /**No condition, everyone can claim the job, and reclaim it */
        return jobContainer.getModelAndBatchIndex();
    }

    function createNewJob() private {
        // push current job to previousJobs
        previousJobs.push(jobContainer);
        // create a new job TODO dummies value atm, should be getted from fl server
        jobContainer = new EncryptionJobContainer();
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

    function addVerificationParameters(uint256[] memory array) public {
        jobContainer.addVerificationParameters(array);
    }

    function getAllPreviousJobsBestModel()
        public
        view
        returns (uint256[][] memory)
    {
        // create a dynamic array of 2 dimension to store the best models
        uint256[][] memory bestModels = new uint256[][](previousJobs.length);
        // uint256[] memory bestModels = new uint256[](previousJobs.length);
        for (uint256 i = 0; i < previousJobs.length; i++) {
            (uint256[] memory newModel, bool ready) = previousJobs[i]
                .getModel();
            if (ready) {
                bestModels[i] = newModel;
            } else {
                bestModels[i] = new uint256[](0);
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
    function getFinalModel() public view returns (uint256[] memory, bool) {
        return jobContainer.getModel();
    }

    /// @notice reset the contract for a new task
    function resetLearnTask() public {
        jobContainer.resetLearnTask();
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
