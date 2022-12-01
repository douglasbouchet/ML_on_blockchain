// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract LearnTask {
    struct VerificationParameters {
        bytes1[32] workerModel; // 32 bytes for the model (will change after to non fixed size)
        bytes1[32] workerSecret; // 32 bytes worker's secret key (not the private key)
    }
    mapping(address => string) addressToPublicKey; // address of a worker to its public key
    //mapping(address => bytes4) addressToEncModel; // address of a worker to the encrypted model it sends (32 bits model)
    mapping(address => bytes1[32]) addressToEncModel; // address of a worker to the encrypted model it sends (32 bits model)
    // address of a worker to the parameters used to verify the model and proof it was computed by the worker
    mapping(address => VerificationParameters) addressToVerificationParameters;

    mapping(bytes32 => uint256) modelToNSameModels; // for each model, record how many times we have seen it
    bytes32[] models; // keep track of each different model we decrypted

    uint256 thresholdForBestModel; // number of equal models needed to be considered as the best one.
    uint256 thresholdMaxNumberReceivedModels;

    address[] receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    // each time a worker sends its verification parameters it's address is added to this arra
    address[] receivedVerificationParametersAddresses;

    int256 currentModel;
    uint256 batchIndex;
    bytes32 newModel; // the weight of the new model
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

    /// @notice send a new encrypted model to the jobContainer
    /// @notice each address can send only one model
    /// @param workerAddress the address of the worker sending the model
    /// @param encryptedModel the encrypted model sent by the worker
    /// @return true if the model was added to the jobContainer, false otherwise
    function addNewEncryptedModel(
        address workerAddress,
        bytes1[32] memory encryptedModel
    ) public modelOnlySendOnce(workerAddress) returns (bool) {
        receivedModelsAddresses.push(workerAddress);
        addressToEncModel[workerAddress] = encryptedModel;
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
        bytes32 a = bytes32(
            0x300330ecd127756b824aa13e843cb1f43c473cb22eaf3750d5fb9c99279af8c3
        );
        // convert bytes32 to byte1[32]
        bytes1[32] memory b;
        for (uint256 i = 0; i < 32; i++) {
            b[i] = a[i];
        }

        return keccak256(abi.encodePacked(clearModel));
    }

    /// @notice send a new verification parameters to the jobContainer
    /// @notice each address can send only one verification parameters (if has previously sent a model)
    // function addVerificationParameters(
    //     address _workerAddress,
    //     int256 _workerNonce,
    //     bytes1[44] memory _workerSecret
    // ) public onlyReceivedModelsAddresses(_workerAddress) {
    function addVerificationParameters(
        address _workerAddress,
        bytes1[32] memory _workerSecret,
        bytes1[32] memory _clearModel
    ) public onlyReceivedModelsAddresses(_workerAddress) {
        require(
            canReceiveNewModel == false,
            "Can't send verification parameters, not enough models received"
        );
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
        ] = VerificationParameters(_clearModel, _workerSecret);
        // We check if hash of clear model is equal to the hash of the model sent by the worker during leaning phase
        bytes32 _modelHash = keccak256(abi.encodePacked(_clearModel));
        // get first byte of _modelHash
        bytes1 _firstByte = bytes1(_modelHash[0]);
        bytes1 _firstByteEnc = bytes1(addressToEncModel[_workerAddress][0]);
        require(
            _firstByte == _firstByteEnc,
            "The model sent by the worker is not the same as the one he sent during learning phase"
        );

        // we decrypt the model of this woker
        //bytes4 encryptedModel = addressToEncModel[_workerAddress];
        bytes1[32] memory encryptedModel = addressToEncModel[_workerAddress];
        //bytes4 decryptedModel = encryptedModel ^ _workerSecret;
        bytes4 decryptedModel = 0; //TODO change
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
        bytes32 _bestModel = checkEnoughSameModel();
        if (_bestModel != 0x0) {
            // in that case we elected the best model, so we can pay workers that did correct job
            modelIsReady = true;
            // publish the new model
            newModel = _bestModel;
            // pay workers
            payCorrectWorkers(_bestModel);
        }
    }

    function checkEnoughSameModel() private view returns (bytes32) {
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
            //bytes4 encryptedModel = addressToEncModel[workerAddress];
            bytes1[32] memory encryptedModel = addressToEncModel[workerAddress];
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
    function getModel() public view returns (bytes32, bool) {
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

    function getAddressToEncModelLen() public view returns (uint256) {
        return receivedModelsAddresses.length;
    }

    function compareKeccak(bytes32 modelHash) public pure returns (bool) {
        bytes32 computedModelHash = keccak256(
            abi.encodePacked(uint8(97), uint8(98), uint8(99))
        );
        return modelHash == computedModelHash;
    }
}
