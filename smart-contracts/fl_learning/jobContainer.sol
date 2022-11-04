// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract JobContainer {
    /**
    Contains all the informations needed to perform a learning task, namely:
    - The model to perform learning on
    - The data batch index to use for learning

    Once nModelsUntilEnd models have been sent by workers, correct model is decided by this contract and made public.
     */

    uint16 nModelsUntilEnd;
    int256[] batchIndex;
    int256[nModelsUntilEnd][] receivedModels;

    mapping(bytes32 => address) private modelHashToWorkerAddress; // usefull to pay worker that did provide correct models

    constructor(uint16 _nModelsUntilEnd, int256[] memory _batchIndex) public {
        nModelsUntilEnd = _nModelsUntilEnd;
        batchIndex = _batchIndex;
    }
}
