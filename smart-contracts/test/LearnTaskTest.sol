// // SPDX-License-Identifier: GPL-3.0

// pragma solidity >=0.7.0 <0.9.0;
// import "remix_tests.sol"; // this import is automatically injected by Remix.
// import "hardhat/console.sol";
// import "../contracts/3_Ballot.sol";
// import "../contracts/taskFinder.sol";

// //contract BallotTest {
// //
// //    bytes32[] proposalNames;
// //
// //    Ballot ballotToTest;
// //    function beforeAll () public {
// //        proposalNames.push(bytes32("candidate1"));
// //        ballotToTest = new Ballot(proposalNames);
// //    }
// //
// //    function checkWinningProposal () public {
// //        console.log("Running checkWinningProposal");
// //        ballotToTest.vote(0);
// //        Assert.equal(ballotToTest.winningProposal(), uint(0), "proposal at index 0 should be the winning proposal");
// //        Assert.equal(ballotToTest.winnerName(), bytes32("candidate1"), "candidate1 should be the winner name");
// //    }
// //
// //    function checkWinninProposalWithReturnValue () public view returns (bool) {
// //        return ballotToTest.winningProposal() == 0;
// //    }
// //}

// contract LearnTaskTest {
//     address workerAdd0 =
//         address(
//             uint160(
//                 uint256(
//                     keccak256(
//                         abi.encodePacked(uint256(1), blockhash(block.number))
//                     )
//                 )
//             )
//         );
//     address workerAdd1 =
//         address(
//             uint160(
//                 uint256(
//                     keccak256(
//                         abi.encodePacked(uint256(2), blockhash(block.number))
//                     )
//                 )
//             )
//         );
//     address workerAdd2 =
//         address(
//             uint160(
//                 uint256(
//                     keccak256(
//                         abi.encodePacked(uint256(3), blockhash(block.number))
//                     )
//                 )
//             )
//         );
//     address workerAdd3 =
//         address(
//             uint160(
//                 uint256(
//                     keccak256(
//                         abi.encodePacked(uint256(4), blockhash(block.number))
//                     )
//                 )
//             )
//         );
//     // creates a bytes1[32] random array
//     bytes1[32] _worker0Secret;
//     bytes1[32] _worker0Model;
//     bytes1[32] clearModel;

//     int256 currentModel = 5;
//     uint256 batchIndex = 1;
//     uint256 thresholdForBestModel = 2;
//     uint256 thresholdMaxNumberReceivedModels = 3;

//     LearnTask learnTaskToTest;

//     function beforeAll() public {
//         learnTaskToTest = new LearnTask(
//             currentModel,
//             batchIndex,
//             thresholdForBestModel,
//             thresholdMaxNumberReceivedModels
//         );
//         for (uint256 i = 0; i < 32; i++) {
//             _worker0Secret[i] = bytes1(
//                 uint8(
//                     uint256(
//                         keccak256(
//                             abi.encodePacked(
//                                 block.timestamp,
//                                 block.difficulty,
//                                 i
//                             )
//                         )
//                     ) % 256
//                 )
//             );
//             _worker0Model[i] = bytes1(
//                 uint8(
//                     uint256(
//                         keccak256(
//                             abi.encodePacked(
//                                 block.timestamp,
//                                 block.difficulty,
//                                 i + 32
//                             )
//                         )
//                     ) % 256
//                 )
//             );
//             clearModel[i] = bytes1("1");
//         }
//     }

//     function initParemeter() public {
//         console.log("Running checkWinningProposal");
//         Assert.equal(
//             learnTaskToTest.getAddressToEncModelLen(),
//             uint256(0),
//             "Len not good"
//         );
//     }

//     function checkAddNewEncryptedModel() public {
//         console.log("checking addNewEncryptedModel....");
//         console.log("Worker0 address ", workerAdd0);
//         // we add a new model
//         bool returnValue = learnTaskToTest.addNewEncryptedModel(
//             workerAdd0,
//             _worker0Model
//         );
//         // see if adding was correct
//         Assert.equal(
//             learnTaskToTest.getAddressToEncModelLen(),
//             uint256(1),
//             "Len not good"
//         );
//         Assert.equal(returnValue, true, "return value should be true");
//         Assert.equal(
//             learnTaskToTest.canSendVerificationParameters(),
//             false,
//             "shouldn't be possible to send model"
//         );
//         returnValue = learnTaskToTest.addNewEncryptedModel(
//             workerAdd1,
//             _worker0Model
//         );
//         // see if adding was correct
//         Assert.equal(
//             learnTaskToTest.getAddressToEncModelLen(),
//             uint256(2),
//             "Len not good"
//         );
//         Assert.equal(returnValue, true, "return value should be true");
//         Assert.equal(
//             learnTaskToTest.canSendVerificationParameters(),
//             false,
//             "shouldn't be possible to send model"
//         );
//         returnValue = learnTaskToTest.addNewEncryptedModel(
//             workerAdd2,
//             _worker0Model
//         );
//         // see if adding was correct
//         Assert.equal(
//             learnTaskToTest.getAddressToEncModelLen(),
//             uint256(3),
//             "Len not good"
//         );
//         Assert.equal(returnValue, true, "return value should be true");
//         Assert.equal(
//             learnTaskToTest.canSendVerificationParameters(),
//             true,
//             "should be possible to send model"
//         );
//     }

//     function checkComputeKeccak256() public {
//         bytes memory encoded = abi.encodePacked("aaa");
//         console.log("packed argument = ", string(encoded));
//         bytes32 encodingRes = keccak256(encoded);
//         console.log(
//             "hashed packed = ",
//             learnTaskToTest.bytes32ToString(encodingRes)
//         );
//         console.log(
//             "hashed packed v2 = ",
//             learnTaskToTest.bytes32ToStringV2(encodingRes)
//         );
//         // we see the compute hash of a clear model
//         //bytes32 hashedModel = learnTaskToTest.computeKeccak256(clearModel);
//         bytes32 hashedModel = learnTaskToTest.computeKeccak256("aaa");
//         //console.log("The model hash is:" , hashedModel);
//         //console.log("The hashed model is: ", learnTaskToTest.bytes32ToString(hashedModel));
//         console.log(
//             "The hashed model is: ",
//             learnTaskToTest.bytes32ToString(hashedModel)
//         );
//         Assert.equal(
//             learnTaskToTest.getAddressToEncModelLen(),
//             uint256(3),
//             "Len not good"
//         );
//     }
//     //function checkAddNewEncryptedModel () public {
//     //    console.log("checking addNewEncryptedModel....");
//     //    console.log("WOrker0 address ", workerAdd0);
//     //    //console.log("randomArray ", _worker0Secret[0]);
//     //
//     //
//     //    // we add a new model
//     //    learnTaskToTest.addVerificationParameters(workerAdd0,_worker0Secret,_worker0Model);
//     //    // see if adding was correct
//     //    Assert.equal(learnTaskToTest.getAddressToEncModelLen(), uint256(1), "Len not good");
//     //}
//     // function checkWinningProposal () public {
//     //     console.log("Running checkWinningProposal");
//     //     ballotToTest.vote(0);
//     //     Assert.equal(ballotToTest.winningProposal(), uint(0), "proposal at index 0 should be the winning proposal");
//     //     Assert.equal(ballotToTest.winnerName(), bytes32("candidate1"), "candidate1 should be the winner name");
//     // }
//     //
//     // function checkWinninProposalWithReturnValue () public view returns (bool) {
//     //     return ballotToTest.winningProposal() == 0;
//     // }
// }
