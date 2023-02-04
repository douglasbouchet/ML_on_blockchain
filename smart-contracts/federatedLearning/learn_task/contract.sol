// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract SplittedModelLearnTask {
    // In this version, we don't use phase 0 (useless in diablo). Phase 1 same as previously. New phase 2.
    // It do not reconstruct the whole model and then compute hash, but rather used chain hash properties
    // in order to compute the hash of the model.
    struct VerificationParameters {
        uint256[] workerModel; // store weights of the model
        address workerAddress;
    }
    mapping(address => string) addressToPublicKey; // address of a worker to its public key
    mapping(address => bytes32) addressToHashModel; // address of a worker to the encrypted model it sends (32 bits model)
    // address of a worker to the parameters used to verify the model and proof it was computed by the worker
    mapping(address => VerificationParameters) addressToVerificationParameters;

    // for each model, record how many times we have seen it. In solidity we can't use a dynamic array as a key
    // for a mapping, so we use hash of the model as a key
    mapping(bytes32 => uint256) modelToNSameModels;
    // uint256[] models; // keep track of each different model we have seen (models are stored in clear)
    uint256[][] models; // keep track of each different model we have seen (models are stored in clear)
    uint256 nModels = 0; // number of different models we have seen

    address[] receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    // each time a worker sends its verification parameters it's address is added to this arra
    address[] receivedVerificationParametersAddresses;

    uint256 nWorkers = 10;
    uint256 thresholdForBestModel = 50; // number of equal models needed to be considered as the best one.
    uint256 thresholdMaxNumberReceivedModels = 90; // maximum number of models we can receive before we compute the best model
    uint256 model_length = 5000000; // length of the model
    uint256 modelChunkSize = 1000; // length of the model
    uint256 nChunks = model_length / modelChunkSize; // number of chunks in the model
    uint256[] newModel; // the weight of the new model
    bool modelIsReady = false;
    bool canReceiveNewModel = true;
    uint256 resetCounter = 0;
    // TODO don't forget that this should be the number of workers (use this in script to generate this file)
    bytes32[10] workerModelHashes; // hashes of worker's model. Will be udpated by chain hashing in phase 2
    uint256[10] workerModelIdxCount; // The expected model number for each worker
    mapping(address => uint256) hashPosition; // The position of the worker address in workerModelHashes and workerModelIdxCount

    // create a constuctor to initialize the newModel array
    constructor() {
        // fill workerModelHashes with empty values
        for (uint256 i = 0; i < workerModelHashes.length; i++) {
            workerModelHashes[i] = 0x0;
        }
        // fill workerModelIdxCount with starting idx
        for (uint256 i = 0; i < workerModelIdxCount.length; i++) {
            workerModelIdxCount[i] = 0;
        }
    }

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
    /// @notice also reset the learn task if previous learning is done.
    /// @param workerAddress the address of the worker sending the model
    /// @param modelHash the hashed model (xored with worker's public key) sent by the worker
    /// @return true if the model hash was recorderd, false otherwise
    function addNewEncryptedModel(uint160 workerAddress, bytes32 modelHash)
        public
        returns (bool)
    {
        // if (getModelIsready()) {
        // TODO Modified to handle case where we don't actually store models on the smart contract
        // if (resetCounter > thresholdMaxNumberReceivedModels) {
        if (resetCounter > thresholdMaxNumberReceivedModels * nChunks) {
            resetLearnTask();
        }
        // if we already received the maximum number of models, we don't accept new ones
        if (!canReceiveNewModel) {
            return false;
        }
        address _workerAddress = address(workerAddress); // equivalent to receiving the worker address (checked on remix)
        receivedModelsAddresses.push(_workerAddress);
        addressToHashModel[_workerAddress] = modelHash; // TODO uncomment
        hashPosition[_workerAddress] = receivedModelsAddresses.length - 1;
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
    /// @param array the array containing the verification parameters.
    /// By convention, array[0] = worker address, array[1] = model part index, array[2...] = model weights
    function addVerificationParameters(uint256[] memory array)
        public
        returns (bool)
    {
        // onlyReceivedModelsAddresses(address(uint160(array[0])))
        address _workerAddress = address(uint160(array[0]));
        uint256 modelPartIdx = array[1];
        uint256 position = hashPosition[_workerAddress];
        resetCounter += 1; // we expect # workers * N model chunk before resetting
        // TODO not mandatory to copy the array, see later
        // uint256[] memory newModelPart = new uint256[](model_length);
        // for (uint256 i = 0; i < model_length; i++) {
        //     newModelPart[i] = array[i + 2];
        // }
        // we check if the model part index is the expected one
        if (modelPartIdx == workerModelIdxCount[position]) {
            // we get the old hash value for this worker
            bytes32 hashToUpdate = workerModelHashes[position];
            // we compute the hash value by concatenating the old hash value and the new model part
            for (uint256 i = 0; i < modelChunkSize; i++) {
                hashToUpdate = keccak256(
                    abi.encodePacked(hashToUpdate, array[i + 2])
                ); // chained hash
            }
            // we increment the model part index
            workerModelIdxCount[position] = workerModelIdxCount[position] + 1;
            // we update the hash value for this worker
            workerModelHashes[position] = hashToUpdate;
            return true;
        } else {
            return false;
        }
    }

    function checkEnoughSameModel() private view returns (uint256[] memory) {
        // if one of the model has been seen more than thresholdForBestModel times, we return true
        for (uint256 i = 0; i < models.length; i++) {
            if (
                getValueModelToNSameModels(models[i]) >= thresholdForBestModel
            ) {
                return models[i];
            }
        }
        // return an empty dynamic array
        return new uint256[](0);
    }

    function payCorrectWorkers(bytes32 correctModel) private view {
        require(modelIsReady, "The model is not ready yet");
        // TODO: pay the correct workers
    }

    /// @notice function to get the model
    /// @return the model's weights or empty array along with a boolean indicating if the model is valid
    function getModel() public view returns (uint256[] memory, bool) {
        if (modelIsReady) {
            return (newModel, true);
        } else {
            return (new uint256[](0), false);
        }
    }

    /// @notice simple function we use to test the maximum array length its possible to build without running out of gas
    function createArray() public view {
        uint256[] memory array = new uint256[](model_length);
        for (uint256 i = 0; i < model_length; i++) {
            array[i] = i;
        }
    }

    /// @notice reset the contract for a new task
    function resetLearnTask() public {
        for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
            delete addressToHashModel[receivedModelsAddresses[i]];
            delete addressToVerificationParameters[receivedModelsAddresses[i]];
            delete hashPosition[receivedModelsAddresses[i]];
        }
        for (
            uint256 i = 0;
            i < receivedVerificationParametersAddresses.length;
            i++
        ) {
            delete addressToVerificationParameters[
                receivedVerificationParametersAddresses[i]
            ];
        }
        for (uint256 i = 0; i < nModels; i++) {
            bytes32 modelHash = bytes32(keccak256(abi.encodePacked(models[i])));
            delete modelToNSameModels[modelHash];
        }
        for (uint256 i = 0; i < workerModelHashes.length; i++) {
            delete workerModelHashes[i];
            delete workerModelIdxCount[i];
        }
        models = new uint256[][](0);
        receivedModelsAddresses = new address[](0);
        receivedVerificationParametersAddresses = new address[](0);
        newModel = new uint256[](0);
        modelIsReady = false;
        canReceiveNewModel = true;
        resetCounter = 0;
    }

    // ------------- argument checking methods-------------

    /// @notice function to check if the address are correctly sent as uint160
    /// @notice if the argument isn't correct, we go into an infinite loop, which will cause diablo to never commit
    /// @param _workerAddress the address of the worker as an uint160
    /// @return true if the address is correct, otw never returns
    function checkAddressEncoding(uint160 _workerAddress)
        public
        pure
        returns (bool)
    {
        if (
            _workerAddress == 725016507395605870152133310144839532665846457513 // expected address
        ) {
            return true;
        }
        uint256 x = 0;
        while (true) {
            x += 1;
        }
    }

    function checkUint160AndBytes32(uint160 _workerAddress, bytes32 _modelHash)
        public
        pure
        returns (bool)
    {
        // expected address: 725016507395605870152133310144839532665846457513
        // expected modelHash: 0xe72c25d7ca23adf3090d18988974cb4633e9261db2fb0a4a4d5d703a19cd356d
        uint160 trueAddress = 725016507395605870152133310144839532665846457513;
        bytes32 trueModelHash = 0xe72c25d7ca23adf3090d18988974cb4633e9261db2fb0a4a4d5d703a19cd356d;
        if (_workerAddress == trueAddress && _modelHash == trueModelHash) {
            //if (_workerAddress == trueAddress && _modelHash == trueAddressBis) {
            return true;
        }
        uint256 x = 0;
        while (true) {
            x += 1;
        }
    }

    function checkDynamicUint256Array(
        uint256[] memory testArray,
        uint160 checkInt
    ) public pure returns (bool) {
        uint160 trueCheckInt = 42;
        if (trueCheckInt != trueCheckInt) {
            uint256 x = 0;
            while (true) {
                x += 1;
            }
            return true;
        } else {
            uint256[] memory trueArray = new uint256[](5);
            for (uint256 i = 0; i < testArray.length; i++) {
                trueArray[i] = i + 1;
            }
            if (testArray.length != trueArray.length) {
                uint256 x = 0;
                while (true) {
                    x += 1;
                }
            } else {
                for (uint256 i = 0; i < testArray.length; i++) {
                    if (testArray[i] != trueArray[i]) {
                        uint256 x = 0;
                        while (true) {
                            x += 1;
                        }
                    }
                }
                return true;
            }
        }
    }

    function checkUint160AndUint256(
        uint160 _uintWorkerAddress,
        uint256 _clearModel
    ) public pure returns (bool) {
        uint160 trueAddress = 725016507395605870152133310144839532665846457513;
        uint256 trueClearModel = 42;
        if (
            _uintWorkerAddress == trueAddress && _clearModel == trueClearModel
        ) {
            return true;
        }
        uint256 x = 0;
        while (true) {
            x += 1;
        }
    }

    function getModelIsready() public view returns (bool) {
        return modelIsReady;
    }

    //------------Helper functions---------------------------------
    /// @notice update the value of the modelToNSameModels
    /// @param key the key of the model
    /// @param value the value to set
    function setValueModelToNSameModels(uint256[] memory key, uint256 value)
        public
    {
        modelToNSameModels[bytes32(keccak256(abi.encodePacked(key)))] = value;
    }

    /// @notice get the value of the modelToNSameModels
    /// @param key the key of the model
    /// @return the value of the modelToNSameModels
    function getValueModelToNSameModels(uint256[] memory key)
        public
        view
        returns (uint256)
    {
        return modelToNSameModels[bytes32(keccak256(abi.encodePacked(key)))];
    }

    //------------ Debug functions---------------------------------
    function compareKeccak(bytes32 modelHash) public pure returns (bool) {
        bytes32 computedModelHash = keccak256(
            //abi.encodePacked(uint8(97), uint8(98), uint8(99))
            abi.encodePacked(uint256(97))
        );
        return modelHash == computedModelHash;
    }
}
