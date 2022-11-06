// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract JobContainer {
    uint16 nModelsUntilEnd;
    uint256 batchIndex;
    int256 public currentModel;
    //int256[] private receivedModels;
    int256[] public receivedModels;
    bool private jobFinished;
    int256 public bestModel;
    address[] private receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array

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

    function setBestModel(int256 _bestModel) private {
        bestModel = _bestModel;
    }

    function computeBestModel() private returns (int256) {
        // return a trivial model
        //int256[] memory _bestModel = new int256[](10);
        //for (uint256 i = 0; i < 10; i++) {
        //    _bestModel[i] = 0;
        //}
        //return _bestModel;
        return receivedModels[0];
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
        receivedModels.push(_model);
        // if we received enough models, we can compute the best model
        if (receivedModels.length == nModelsUntilEnd) {
            int256 _bestModel = computeBestModel();
            // set the best model
            setBestModel(_bestModel);
            // set jobFinished to true
            jobFinished = true;
        }
        return jobFinished;
    }

    // ----------- DEBUG FUNCTIONS -------------
    function getReceivedModels() public view returns (int256[] memory) {
        /** TODO this function is only for debug purpose, we will not allow people to get the current received worker */
        return receivedModels;
    }
}
