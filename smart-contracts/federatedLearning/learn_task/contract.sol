// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract LearnTask {
    struct VerificationParameters {
        uint256 workerModel; //  1 uint256 for the model (will change after to non fixed size)
        address workerAddress;
    }
    mapping(address => string) addressToPublicKey; // address of a worker to its public key
    mapping(address => bytes32) addressToHashModel; // address of a worker to the encrypted model it sends (32 bits model)
    // address of a worker to the parameters used to verify the model and proof it was computed by the worker
    mapping(address => VerificationParameters) addressToVerificationParameters;

    mapping(uint256 => uint256) modelToNSameModels; // for each model, record how many times we have seen it
    uint256[] models; // keep track of each different model we have seen (models are stored in clear)

    uint256 thresholdForBestModel; // number of equal models needed to be considered as the best one.
    uint256 thresholdMaxNumberReceivedModels;

    address[] receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    // each time a worker sends its verification parameters it's address is added to this arra
    address[] receivedVerificationParametersAddresses;

    uint256 currentModel;
    uint256 batchIndex;
    uint256 newModel; // the weight of the new model
    bool modelIsReady = false;
    bool canReceiveNewModel = true;

    modifier onlyReceivedModelsAddresses(address workerAddress) {
        // modified that check if a worker address is inside receivedModelsAddresses
        bool workerHasSendModel = false;
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            if (receivedModelsAddresses[i] == workerAddress) {
                workerHasSendModel = true;
            }
        }
        require(
            workerHasSendModel,
            "The worker didn't send a model during training phase, parameters refused"
        );
        _;
    }

    modifier modelOnlySendOnce(address workerAddress) {
        // modified that check if a worker address is inside receivedModelsAddresses
        bool workerHasSendModel = false;
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            if (receivedModelsAddresses[i] == workerAddress) {
                workerHasSendModel = true;
            }
        }
        require(!workerHasSendModel, "The worker already sent a model");
        _;
    }

    constructor(
        uint256 _currentModel,
        uint256 _batchIndex,
        uint256 _thresholdForBestModel,
        uint256 _thresholdMaxNumberReceivedModels
    ) {
        currentModel = _currentModel;
        batchIndex = _batchIndex;
        thresholdForBestModel = _thresholdForBestModel;
        thresholdMaxNumberReceivedModels = _thresholdMaxNumberReceivedModels;
    }

    function getModelAndBatchIndex() public view returns (uint256, uint256) {
        return (currentModel, batchIndex);
    }

    /// @notice tell weather a worker can send its verification parameters or not
    /// @param workerAddress the address of the worker
    /// @return true if the worker can send its verification parameters, false otherwise
    function canSendVerificationParameters(address workerAddress)
        public
        view
        returns (bool)
    {
        // check if the workerAddress did send a model during learning phase
        bool workerHasSendModel = false;
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            if (receivedModelsAddresses[i] == workerAddress) {
                workerHasSendModel = true;
            }
        }
        return !canReceiveNewModel && workerHasSendModel;
    }

    /// @notice send a new encrypted model to the jobContainer
    /// @notice each address can send only one model
    /// @param workerAddress the address of the worker sending the model
    /// @param modelHash the hashed model (xored with worker's public key) sent by the worker

    /// @return true if the model was added to the jobContainer, false otherwise
    //function addNewEncryptedModel(address workerAddress, bytes32 modelHash)
    //    modelOnlySendOnce(workerAddress)
    //    returns (bool)
    //{
    //function addNewEncryptedModel(uint256 workerAddress) public returns (bool) {
    //function addNewEncryptedModel(uint160 workerAddress) public returns (bool) {
    function addNewEncryptedModel(uint160 workerAddress, bytes32 modelHash)
        public
        returns (bool)
    {
        // if we already received the maximum number of models, we don't accept new ones
        if (!canReceiveNewModel) {
            return false;
        }
        //address _workerAddress = address(workerAddress); // equivalent to receiving the worker address (checked on remix)
        // receivedModelsAddresses.push(address(workerAddress));
        // addressToHashModel[workerAddress] = modelHash; TODO uncomment
        // if the number of received model is equal to the thresholdMaxNumberReceivedModels, we stop receiving
        // new models
        if (
            receivedModelsAddresses.length == thresholdMaxNumberReceivedModels
        ) {
            canReceiveNewModel = false;
        }
        return true;
    }

    function computeKeccak256(bytes1[32] memory clearModel)
        public
        pure
        returns (bytes32)
    {
        return keccak256(abi.encodePacked(clearModel));
    }

    /// @notice send a new verification parameters to the jobContainer
    /// @notice each address can send only one verification parameters (if has previously sent a model)
    function addVerificationParameters(
        address _workerAddress,
        uint256 _clearModel
    ) public onlyReceivedModelsAddresses(_workerAddress) {
        // TODO convert address to uint160 and cast it to address (also do it in the tested smart contract)
        // check that worker has send a model, that don't receive new model anymore and that model is not ready
        if (canSendVerificationParameters(_workerAddress) && !modelIsReady) {
            // require that the _workerAddress isn't already in receivedVerificationParametersAddresses
            for (
                uint256 i = 0;
                i < receivedVerificationParametersAddresses.length;
                i++
            ) {
                require(
                    receivedVerificationParametersAddresses[i] !=
                        _workerAddress,
                    "You already sent your verification parameters"
                );
            }
            // if this address didn't already pushed a model, we can add it to receivedVerificationParametersAddresses
            receivedVerificationParametersAddresses.push(_workerAddress);
            addressToVerificationParameters[
                _workerAddress
            ] = VerificationParameters(_clearModel, _workerAddress);
            // We check if hash of clear model + worker's address converted to uint256
            // is equal to the hash of the model sent by the worker during leaning phase
            // bytes32 modelHash = keccak256(abi.encodePacked(uint8(97), uint8(98), uint8(99)));
            uint256 model_with_public_key = _clearModel +
                uint256(_workerAddress);
            bytes32 modelHash = keccak256(
                abi.encodePacked(model_with_public_key)
            );
            // we get the model sent by the worker during learning phase
            bytes32 modelSentByWorker = addressToHashModel[_workerAddress];
            // we check if the two are equals
            require(
                modelHash == modelSentByWorker,
                "The model sent by the worker during learning phase is not equal to the model computed by the worker during verification phase"
            );
            // now we know the worker did prove that this model was produced by him, we can add it to the received
            // clear models
            modelToNSameModels[_clearModel] += 1; //TODO check if ok
            // check if we already registered this model
            bool modelAlreadyInModels = false;
            for (uint256 i = 0; i < models.length; i++) {
                if (models[i] == _clearModel) {
                    modelAlreadyInModels = true;
                }
            }
            // if decryptedModel not in models, we add it
            if (!modelAlreadyInModels) {
                models.push(_clearModel);
            }
            uint256 _bestModel = checkEnoughSameModel();
            if (_bestModel != 0) {
                // in that case we elected the best model, so we can pay workers that did correct job
                modelIsReady = true;
                // publish the new model
                newModel = _bestModel;
                // pay workers
                //payCorrectWorkers(_bestModel);
            }
        } else {
            revert("You can't send your verification parameters");
        }
    }

    function checkEnoughSameModel() private view returns (uint256) {
        // if one of the model has been seen more than thresholdForBestModel times, we return true
        for (uint256 i = 0; i < models.length; i++) {
            if (modelToNSameModels[models[i]] >= thresholdForBestModel) {
                return models[i];
            }
        }
        return 0x0;
    }

    function payCorrectWorkers(bytes32 correctModel) private view {
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
            //bytes4 encryptedModel = addressToHashModel[workerAddress];
            bytes32 encryptedModel = addressToHashModel[workerAddress];
            // bytes4 decryptedModel = encryptedModel ^
            //     verificationParameters.workerSecret;
            bytes4 decryptedModel = 0;
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
    function getModel() public view returns (uint256, bool) {
        if (modelIsReady) {
            return (newModel, true);
        } else {
            return (0, false);
        }
    }

    //------------ Debug functions---------------------------------
    function getModelIsready() public view returns (bool) {
        return modelIsReady;
    }

    function compareKeccak(bytes32 modelHash) public pure returns (bool) {
        bytes32 computedModelHash = keccak256(
            //abi.encodePacked(uint8(97), uint8(98), uint8(99))
            abi.encodePacked(uint256(97))
        );
        return modelHash == computedModelHash;
    }

    /// @notice dummy function to check if diablo is working
    // function testDiablo(int256) public pure returns (bool) {
    //     return true;
    // }

    /// @notice dummy function to check if diablo is working
    //function testDiablo(uint160, uint160) public pure returns (bool) {
    // function testDiablo(bytes32) public pure returns (bool) {
    function testDiablo(uint160, bytes32) public pure returns (bool) {
        return true;
    }

    // ------------- also dummy methods-------------
    int256 private count = 0;

    function push(int256 delta) public {
        count += delta;
    }

    function pull(int256 delta) public {
        if (count > delta) {
            count -= delta;
        }
    }
}
