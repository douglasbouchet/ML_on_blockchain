// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract FragmentedJobContainer {
    struct Fragment {
        uint256 fragNumber;
        int256 weight;
    }
    //------------------- fragment attributs-------------------------------------------
    uint256 public nFragments; // the number of fragments under which our model is split
    bytes32[] public modelsHashes; // hashes of the models received sor far
    mapping(bytes32 => Fragment[]) public modelHashToFragments; // modelHash -> [Fragment]
    mapping(bytes32 => uint256) public modelHashToSize; // modelHash -> numbe of fragments
    //------------------- workers attributs-------------------------------------------
    mapping(address => bytes32) public workerAddressToModelHash;
    address[] private receivedModelsAddresses; // each time a worker sends a model, it's address is added to this array
    //------------------- model attributs-------------------------------------------
    uint256 batchIndex;
    int256 public currentModel;
    int256 newModel; // the weight of the new model
    bool modelIsReady = false; // true if a model has been merged and posses correct hash

    //     mapping(bytes32 => address) private modelHashToWorkerAddress; // usefull to pay worker that did provide correct models

    //     modifier modelOnlySendOnce(address _workerAddress) {
    //         // require that the _workerAddress isn't already in receivedModelsAddresses
    //         for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
    //             require(
    //                 receivedModelsAddresses[i] != _workerAddress,
    //                 "You already sent a model"
    //             );
    //         }
    //         // if this address didn't already pushed a model, we can add it to receivedModelsAddresses
    //         receivedModelsAddresses.push(_workerAddress);
    //         _;
    //     }

    constructor(
        uint16 _nFragments,
        int256 _currentModel,
        uint256 _batchIndex
    ) {
        nFragments = _nFragments;
        currentModel = _currentModel;
        batchIndex = _batchIndex;
    }

    function getModelAndBatchIndex() public view returns (int256, uint256) {
        return (currentModel, batchIndex);
    }

    //     function payWorkers(bytes32 _modelHash) private {
    //         for (uint256 i = 0; i < receivedModelsAddresses.length; i++) {
    //             // if the model of worker is the best model, we pay the worker
    //             if (
    //                 workerAddressToModelHash[receivedModelsAddresses[i]] ==
    //                 _modelHash
    //             ) {
    //                 //TODO compute this value such as expectation for good worker is > 0
    //                 // transfert money to worker
    //                 payable(address(receivedModelsAddresses[i])).transfer(0 ether);
    //             }
    //         }
    //     }

    //     // ----------- DEBUG FUNCTIONS -------------

    //     //------------ Fragment methods-----------------

    /// @notice Add a fragment of the model
    /// @dev handle all the logic upon adding a new fragment, including merging the model if all fragments are received,
    /// checking if the model is valid and paying the workers if the model is valid
    /// @param _fragNb identifier of the fragment
    /// @param _weight weights of the model's fragment
    /// @param _modelHash Hash of the model
    /// @return True if we don't have any fragment with this number associated to this model hash. false otw and the
    /// worker needs to send another fragment
    function addFragment(
        address _workerAddress,
        uint256 _fragNb,
        int256 _weight,
        bytes32 _modelHash
    ) public returns (bool) {
        return true;
    }

    //         // check if we have a model with this hash
    //         bool _hashExists = false;
    //         for (uint256 i = 0; i < modelsHashes.length; i++) {
    //             if (modelsHashes[i] == _modelHash) {
    //                 _hashExists = true;
    //             }
    //         }
    //         // if we don't have a model with this hash, we add it to modelsHashes
    //         if (!_hashExists) {
    //             modelsHashes.push(_modelHash);
    //             modelHashToSize[_modelHash] = 0;
    //             modelHashToFragments[_modelHash] = new Fragment[](nFragments); //TODO see if correctly created
    //         }

    //         uint256 _nFrags = modelHashToSize[_modelHash];
    //         // now we iterate over all the fragments of the model hash and see if we already have a fragment with this number
    //         for (uint256 i = 0; i < _nFrags; i++) {
    //             if (modelHashToFragments[_modelHash][i].fragNumber == _fragNb) {
    //                 // we already have a fragment with this number
    //                 return false;
    //             }
    //         }

    //         // now we know we don't have received this fragment yet, we can add it to the model

    //         // update the number of fragments for this model hash
    //         modelHashToSize[_modelHash] = _nFrags + 1;

    //         // add the fragment to the list of fragments
    //         modelHashToFragments[_modelHash][_nFrags] = Fragment(_nFrags, _weight);

    //         // add the worker to the list of workers that sent fragments for this model hash
    //         workerAddressToModelHash[_workerAddress] = _modelHash;

    //         // if we have enough fragments, we can merge them
    //         if (_nFrags + 1 == nFragments) {
    //             bool correctModel = mergeFragments(_modelHash);
    //             if (correctModel) {
    //                 // we can now pay the workers that did provide the best model
    //                 payWorkers(_modelHash);
    //             }
    //             // TODO handle case where model is not correct
    //         }

    //         return true;
    //     }

    //     /// @dev function to merge fragments
    //     /// @dev the model hash is computed as the hash of the combined weights
    //     /// @dev if the computed model hash is the same as the expected one, set the new model
    //     /// @param _modelHash of the model to merge inside modelHashToFragments
    //     /// @return true if the model is valid, false otherwise
    //     function mergeFragments(bytes32 _modelHash) private returns (bool) {
    //         // get the model weights into one array
    //         int256[] memory weights = new int256[](nFragments);
    //         for (uint256 i = 0; i < nFragments; i++) {
    //             weights[i] = modelHashToFragments[_modelHash][i].weight;
    //         }

    //         // compute the model hash
    //         bytes32 _computedModelHash = keccak256(abi.encode(weights));

    //         // if the computed model hash is the same as the expected one, set the new model
    //         newModel = weights[0]; // Only first weight as we consider model as a single int256, but we will need to change this
    //         modelIsReady = true;

    //         // check if the computed model hash is the same as the expected one
    //         return _computedModelHash == _modelHash;
    //     }

    /// @notice function to get the model
    /// @return the model's weights or empty array along with a boolean indicating if the model is valid
    function getModel() public view returns (int256, bool) {
        if (modelIsReady) {
            return (newModel, true);
        } else {
            return (0, false);
        }
    }

    function getModelIsready() public view returns (bool) {
        return modelIsReady;
    }
}
