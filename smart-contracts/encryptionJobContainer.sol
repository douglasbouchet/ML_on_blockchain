// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract EncyptionJobContainer {
    struct VerificationParameters {
        int256 workerNonce;
        bytes4 workerSecret;
    }
    mapping(address => string) addressToPublicKey; // address of a worker to its public key
    mapping(address => bytes4) addressToEncModel; // address of a worker to the encrypted model it sends (32 bits model)
    // address of a worker to the parameters used to verify the model and proof it was computed by the worker
    mapping(address => VerificationParameters) addressToVerificationParameters;

    mapping(bytes4 => uint256) modelToNSameModels; // for each model, record how many times we have seen it
    bytes4[] models; // keep track of each different model we decrypted

    uint256 thresholdForBestModel; // number of equal models needed to be considered as the best one.
    uint256 thresholdMaxNumberReceivedModels;

    address[] receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    // each time a worker sends its verification parameters it's address is added to this arra
    address[] receivedVerificationParametersAddresses;

    int256 currentModel;
    uint256 batchIndex;
    bytes4 newModel; // the weight of the new model
    bool modelIsReady = false;
    bool canReceiveNewModel = true;

    constructor(
        int256 _currentModel,
        uint256 _batchIndex,
        uint256 _thresholdForBestModel,
        uint256 _thresholdMaxNumberReceivedModels
    ) {
        currentModel = _currentModel;
        batchIndex = _batchIndex;
        thresholdForBestModel = _thresholdForBestModel;
        thresholdMaxNumberReceivedModels = _thresholdMaxNumberReceivedModels;
    }

    function getModelAndBatchIndex() public view returns (int256, uint256) {
        return (currentModel, batchIndex);
    }

    function canSendVerificationParameters() public view returns (bool) {
        return !canReceiveNewModel;
    }

    function addNewEncryptedModel(address workerAddress, bytes4 encryptedModel)
        public
    {
        // require that the _workerAddress isn't already in receivedModelsAddresses
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            require(
                receivedModelsAddresses[i] != workerAddress,
                "You already sent a model"
            );
        }
        // if this address didn't already pushed a model, we can add it to receivedModelsAddresses
        receivedModelsAddresses.push(workerAddress);
        addressToEncModel[workerAddress] = encryptedModel;
        // if the number of received model is equal to the thresholdMaxNumberReceivedModels, we stop receiving
        // new models
        if (
            receivedModelsAddresses.length == thresholdMaxNumberReceivedModels
        ) {
            canReceiveNewModel = false;
        }
    }

    function addVerificationParameters(
        address _workerAddress,
        int256 _workerNonce,
        bytes4 _workerSecret
    ) public {
        // require that the _workerAddress isn't already in receivedVerificationParametersAddresses
        for (
            uint256 i = 0;
            i < receivedVerificationParametersAddresses.length;
            i++
        ) {
            require(
                receivedVerificationParametersAddresses[i] != _workerAddress,
                "You already sent your verification parameters"
            );
        }
        // if this address didn't already pushed a model, we can add it to receivedVerificationParametersAddresses
        receivedVerificationParametersAddresses.push(_workerAddress);
        addressToVerificationParameters[
            _workerAddress
        ] = VerificationParameters(_workerNonce, _workerSecret);
        // we decrypt the model of this woker
        bytes4 encryptedModel = addressToEncModel[_workerAddress];
        bytes4 decryptedModel = encryptedModel ^ _workerSecret;
        // we add the decrypted model to the modelToNSameModels mapping
        modelToNSameModels[decryptedModel] += 1;
        // if decryptedModel not in models, we add it
        bool modelAlreadyInModels = false;
        for (uint256 i = 0; i < models.length; i++) {
            if (models[i] == decryptedModel) {
                modelAlreadyInModels = true;
            }
        }
        if (!modelAlreadyInModels) {
            models.push(decryptedModel);
        }
        bytes4 _bestModel = checkEnoughSameModel();
        if (_bestModel != 0x0) {
            // in that case we elected the best model, so we can pay workers that did correct job
            modelIsReady = true;
            // publish the new model
            newModel = _bestModel;
            // pay workers
            payCorrectWorkers(_bestModel);
        }
    }

    function checkEnoughSameModel() private view returns (bytes4) {
        // if one of the model has been seen more than thresholdForBestModel times, we return true
        for (uint256 i = 0; i < models.length; i++) {
            if (modelToNSameModels[models[i]] >= thresholdForBestModel) {
                return models[i];
            }
        }
        return 0x0;
    }

    function payCorrectWorkers(bytes4 correctModel) private view {
        require(modelIsReady, "The model is not ready yet");
        for (
            uint256 i = 0;
            i < receivedVerificationParametersAddresses.length;
            i++
        ) {
            address workerAddress = receivedVerificationParametersAddresses[i];
            VerificationParameters
                memory verificationParameters = addressToVerificationParameters[
                    workerAddress
                ];
            bytes4 encryptedModel = addressToEncModel[workerAddress];
            bytes4 decryptedModel = encryptedModel ^
                verificationParameters.workerSecret;
            if (decryptedModel == correctModel) {
                // // now we check that the secret and the nonce are correct
                // bytes4 secret = verificationParameters.workerSecret;
                // int256 nonce = verificationParameters.workerNonce;
                // // we try to decrypt the secret with the public key of worker
                // string memory workerPublicKey = addressToPublicKey[
                //     workerAddress
                // ];
                // decrypt secret with workerPublicKey
                // if the result is equal to nonce, we pay the worker else we don't
                //TODO
            }
        }
    }

    /// @notice function to get the model
    /// @return the model's weights or empty array along with a boolean indicating if the model is valid
    function getModel() public view returns (bytes4, bool) {
        if (modelIsReady) {
            return (newModel, true);
        } else {
            return ("0x0", false);
        }
    }

    //------------ Debug functions---------------------------------
    function getModelIsready() public view returns (bool) {
        return modelIsReady;
    }

    function setModelIsready(bool _modelIsReady) public {
        modelIsReady = _modelIsReady;
    }
}
