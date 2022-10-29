# ml-on-blockchain

## Simple behavior

### One server multiple workers

Goal of this first milestone is to deploy a smart contract on a local quorum blockchain.
The smart contract consists of a counter that can be incremented.
Once the smart contract is deployed, a worker willing to join the learning process should call this smart contract and
increment the counter by one (this will later on be used in order to add a worker to set of workers).

#### algorithm assumptions

In order to define a simple behavior, we assume that the learning server only send new model weights to a worker if this
one has already give its optimization result, or if it just registered to learning.
