// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract JobContainer {
    uint16 nModelsUntilEnd;
    uint256 batchIndex;
    int256 public currentModel;
    //int256[] private receivedModels;
    int256[] public receivedModels;
    mapping(address => int256) public workerAddressToReceivedModels;
    bool private jobFinished;
    int256 public bestModel;
    address[] private receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    mapping(int256 => uint256) private modelToCount; // count how many time each model weights were received
    uint256 private bestModelNoccurences; // count how many time each model weights were received

    mapping(bytes32 => address) private modelHashToWorkerAddress; // usefull to pay worker that did provide correct models

    modifier modelOnlySendOnce(address _workerAddress) {
        // require that the _workerAddress isn't already in receivedModelsAddresses
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            require(
                receivedModelsAddresses[i] != _workerAddress,
                "You already sent a model"
            );
        }
        // if this address didn't already pushed a model, we can add it to receivedModelsAddresses
        receivedModelsAddresses.push(_workerAddress);
        _;
    }

    constructor(
        uint16 _nModelsUntilEnd,
        int256 _currentModel,
        uint256 _batchIndex
    ) {
        nModelsUntilEnd = _nModelsUntilEnd;
        currentModel = _currentModel;
        batchIndex = _batchIndex;
    }

    function getNModelsUntilEnd() public view returns (uint16) {
        return nModelsUntilEnd;
    }

    function getModelAndBatchIndex() public view returns (int256, uint256) {
        return (currentModel, batchIndex);
    }

    function getBestModel() public view returns (int256) {
        return bestModel;
    }

    function computeBestModel() private returns (bool) {
        /** Group the received models, and keep the one with the most occurences
         * TODO implement reverse if dominant model has less than majority
         * @return the best model from receivedModels TODO null value if no consensus
         */
        for (uint256 i = 0; i < receivedModels.length; i++) {
            if (modelToCount[receivedModels[i]] > bestModelNoccurences) {
                bestModel = receivedModels[i];
                bestModelNoccurences = modelToCount[receivedModels[i]];
            }
        }

        // if less than 50% of workers agree on the same model, return null
        // TODO implement this logic
        // if (bestModelNoccurences < receivedModels.length / 2) {
        // revert
        //     return 0;
        //return false
        // }
        return true;
    }

    function submitNewModel(int256 _model, address _workerAddress)
        public
        modelOnlySendOnce(_workerAddress)
        returns (bool)
    {
        /** This method should only be called once by each worker, i.e you cannot submit same job multiple time
         * @return true if the job is finished, false otherwise
         */
        // add the model to the list of received models
        workerAddressToReceivedModels[_workerAddress] = _model;
        receivedModels.push(_model);
        // update modelToCount
        modelToCount[_model] += 1;

        // if we received enough models, we can compute the best model
        if (receivedModels.length == nModelsUntilEnd) {
            //bool foundBestModel = computeBestModel();
            computeBestModel();
            // add here handling if computeBestModel didn't found a consensus
            jobFinished = true;

            // we can now pay the workers that did provide the best model
            payWorkers();
        }
        return jobFinished;
    }

    function payWorkers() private {
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            // if the model of worker is the best model, we pay the worker
            if (
                workerAddressToReceivedModels[receivedModelsAddresses[i]] ==
                bestModel
            ) {
                //TODO compute this value such as expectation for good worker is > 0
                // transfert money to worker
                payable(address(receivedModelsAddresses[i])).transfer(0 ether);
            }
        }
    }

    // ----------- DEBUG FUNCTIONS -------------
    function getReceivedModels() public view returns (int256[] memory) {
        /** TODO this function is only for debug purpose, we will not allow people to get the current received worker */
        return receivedModels;
    }
}
