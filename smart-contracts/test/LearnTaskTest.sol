// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
// import "remix_tests.sol"; // this import is automatically injected by Remix.
// import "hardhat/console.sol";
import "../federatedLearning/taskFinder.sol";

//contract BallotTest {
//
//    bytes32[] proposalNames;
//
//    Ballot ballotToTest;
//    function beforeAll () public {
//        proposalNames.push(bytes32("candidate1"));
//        ballotToTest = new Ballot(proposalNames);
//    }
//
//    function checkWinningProposal () public {
//        console.log("Running checkWinningProposal");
//        ballotToTest.vote(0);
//        Assert.equal(ballotToTest.winningProposal(), uint(0), "proposal at index 0 should be the winning proposal");
//        Assert.equal(ballotToTest.winnerName(), bytes32("candidate1"), "candidate1 should be the winner name");
//    }
//
//    function checkWinninProposalWithReturnValue () public view returns (bool) {
//        return ballotToTest.winningProposal() == 0;
//    }
//}
contract LearnTaskTest {
    int256 currentModel = 5;
    uint256 batchIndex = 1;
    uint256 thresholdForBestModel = 2;
    uint256 thresholdMaxNumberReceivedModels = 5;

    LearnTask learnTaskToTest;

    function beforeAll() public {
        //proposalNames.push(bytes32("candidate1"));
        learnTaskToTest = new LearnTask(
            currentModel,
            batchIndex,
            thresholdForBestModel,
            thresholdMaxNumberReceivedModels
        );
    }

    function checkWinningProposal() public {
        //console.log("Running checkWinningProposal");
        // Assert.equal(
        //     learnTaskToTest.getAddressToEncModelLen(),
        //     uint256(0),
        //     "Len not good"
        // );
        //Assert.equal(ballotToTest.winningProposal(), uint(0), "proposal at index 0 should be the winning proposal");
        //Assert.equal(ballotToTest.winnerName(), bytes32("candidate1"), "candidate1 should be the winner name");
    }
    // function checkWinningProposal () public {
    //     console.log("Running checkWinningProposal");
    //     ballotToTest.vote(0);
    //     Assert.equal(ballotToTest.winningProposal(), uint(0), "proposal at index 0 should be the winning proposal");
    //     Assert.equal(ballotToTest.winnerName(), bytes32("candidate1"), "candidate1 should be the winner name");
    // }
    //
    // function checkWinninProposalWithReturnValue () public view returns (bool) {
    //     return ballotToTest.winningProposal() == 0;
    // }
}
