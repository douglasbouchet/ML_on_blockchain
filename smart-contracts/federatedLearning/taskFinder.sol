// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

// import "./learnTask.sol";
import "./learn_task/learnTask.sol";

contract TaskFinder {
    LearnTask[] public previousJobs;
    LearnTask private jobContainer;

    constructor() {
        //uint256 thresholdForBestModel = 2;
        //uint256 thresholdMaxNumberReceivedModels = 3; //stop receiving models when we have 5 models
        uint256 thresholdForBestModel = 3; // require 3 equals model to validate
        uint256 thresholdMaxNumberReceivedModels = 6; //stop receiving models when we have 6 models
        jobContainer = new LearnTask(
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
        uint256 thresholdForBestModel = 2;
        uint256 thresholdMaxNumberReceivedModels = 3; //stop receiving models when we have 3 models
        jobContainer = new LearnTask(
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
    // function addEncryptedModel(address workerAddress, bytes4 encryptedModel)
    function addEncryptedModel(address workerAddress, bytes32 modelHash)
        public
        returns (bool)
    {
        bool modelAdded = jobContainer.addNewEncryptedModel(
            workerAddress,
            modelHash
        );
        // // if the model is complete, create a new job and push the current one to previousJobs
        // if (jobContainer.getModelIsready()) {
        //     createNewJob();
        // }
        return modelAdded;
    }

    function addVerificationParameters(
        address workerAddress,
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
