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


## Centralized federated learning

We will have one node (the learning server) which will be handling the learning process (maintain the learning model
states, aggregate results of workers, decide which worker should be working on learning). Every node (worker) of the
process will have to send its result to the learning server.

### assumptions

Every workers make correct computations and send correct data to the learning server (we will maybe work
 on a bizantine resilient system later.)
